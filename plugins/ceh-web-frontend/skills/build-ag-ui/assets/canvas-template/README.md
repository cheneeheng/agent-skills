# AG-UI canvas template

A blank canvas for an [AG-UI](https://docs.ag-ui.com) agent: an empty component area plus a chat
panel, wired to the agent through `@ag-ui/client`. Components are added in `web/src/registry.ts`;
each one becomes a frontend tool the agent can call to place it on the canvas.

```bash
# terminal 1 — mock agent on :8000 (swap for your real AG-UI endpoint)
cd agent && uv run uvicorn main:app --port 8000

# terminal 2 — canvas on :5173, proxies /agent to :8000 (override with AGENT_ORIGIN)
cd web && bun install && bun run dev
```

The mock agent echoes text, and turns `<tool-name> <json-args>` into a call to that frontend tool,
so every registered component can be tried without an LLM.
