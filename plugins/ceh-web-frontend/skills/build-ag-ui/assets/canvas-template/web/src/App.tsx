import { useState, type FormEvent } from "react";
import { registry } from "./registry";
import { useAgent } from "./useAgent";

export function App() {
  const { messages, blocks, running, error, send, abort } = useAgent(registry);
  const [draft, setDraft] = useState("");

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    const text = draft.trim();
    if (!text || running) return;
    setDraft("");
    void send(text);
  }

  return (
    <div className="shell">
      <main className="canvas" aria-label="Canvas">
        {blocks.length === 0 ? (
          <p className="empty">The canvas is empty. Components the agent renders appear here.</p>
        ) : (
          blocks.map((block) => {
            const Component = registry.find((r) => r.name === block.name)?.Component;
            return Component ? <Component key={block.id} {...block.props} /> : null;
          })
        )}
      </main>

      <aside className="chat" aria-label="Conversation">
        <ol className="messages" aria-live="polite">
          {messages
            .filter((m) => (m.role === "user" || m.role === "assistant") && typeof m.content === "string" && m.content)
            .map((m) => (
              <li key={m.id} className={m.role}>
                {m.content as string}
              </li>
            ))}
        </ol>
        {error && <p role="alert" className="error">{error}</p>}
        <form onSubmit={onSubmit}>
          <label htmlFor="prompt" className="visually-hidden">Message the agent</label>
          <input id="prompt" value={draft} onChange={(e) => setDraft(e.target.value)} autoComplete="off" />
          {running ? (
            <button type="button" onClick={abort}>Stop</button>
          ) : (
            <button type="submit">Send</button>
          )}
        </form>
      </aside>
    </div>
  );
}
