import { HttpAgent, randomUUID, type Message } from "@ag-ui/client";
import { useEffect, useMemo, useState } from "react";
import type { CanvasComponent } from "./registry";

export type Block = { id: string; name: string; props: Record<string, unknown> };

// Stops an agent that keeps calling tools from looping forever.
const MAX_TOOL_ROUNDS = 5;

export function useAgent(registry: CanvasComponent[]) {
  const agent = useMemo(
    () => new HttpAgent({ url: import.meta.env.VITE_AGENT_URL ?? "/agent" }),
    [],
  );
  const [messages, setMessages] = useState<Message[]>([]);
  const [state, setState] = useState<Record<string, unknown>>({});
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const sub = agent.subscribe({
      onMessagesChanged: ({ messages }) => setMessages([...messages]),
      onStateChanged: ({ state }) => setState({ ...state }),
    });
    return () => sub.unsubscribe();
  }, [agent]);

  async function send(text: string) {
    agent.addMessage({ id: randomUUID(), role: "user", content: text });
    setRunning(true);
    setError(null);
    const tools = registry.map(({ name, description, parameters }) => ({ name, description, parameters }));
    try {
      for (let round = 0; round < MAX_TOOL_ROUNDS; round++) {
        const { newMessages } = await agent.runAgent({ tools });
        const calls = newMessages.flatMap((m) => (m.role === "assistant" ? (m.toolCalls ?? []) : []));
        const frontendCalls = calls.filter((c) => registry.some((r) => r.name === c.function.name));
        if (frontendCalls.length === 0) break;
        for (const call of frontendCalls) {
          let content = "rendered";
          try {
            const props = JSON.parse(call.function.arguments || "{}");
            setBlocks((b) => [...b, { id: call.id, name: call.function.name, props }]);
          } catch {
            content = "error: arguments were not valid JSON";
          }
          agent.addMessage({ id: randomUUID(), role: "tool", toolCallId: call.id, content });
        }
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setRunning(false);
    }
  }

  return { messages, state, blocks, running, error, send, abort: () => agent.abortRun() };
}
