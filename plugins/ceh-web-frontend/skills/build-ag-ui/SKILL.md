---
name: build-ag-ui
description: >-
  Load this skill when building or extending a frontend for an agent that speaks AG-UI (the
  Agent-User Interaction protocol: an agent endpoint streaming RUN_*, TEXT_MESSAGE_*, TOOL_CALL_*
  and STATE_* events over SSE): starting an agent UI from a blank canvas, adding a component the
  agent can place on screen, wiring frontend tools or shared agent state, or pointing the UI at a
  real agent. Trigger on "build a UI with AG-UI", "ag-ui frontend", "generative UI for my agent",
  "let the agent render components", "add a component the agent can show", or any mention of
  @ag-ui/client, HttpAgent, or ag-ui-protocol. Starts from the user's own template when they give
  one, otherwise copies the bundled empty canvas (React + Vite + @ag-ui/client, plus a mock agent).
  Not for building the agent backend itself, and not for CopilotKit-specific components.
compatibility: >-
  The canvas needs Bun (or Node.js 20+) and network access for the first install; react, vite and
  @ag-ui/client arrive as project dependencies. The mock agent needs uv and Python 3.11+, with
  fastapi, uvicorn and ag-ui-protocol installed by uv. Without uv, point the canvas at an existing
  AG-UI endpoint instead. Written against @ag-ui/client and ag-ui-protocol 1.0.
---

# Build a UI on AG-UI

AG-UI is an event protocol, not a component library. The agent streams events. The UI renders
them, and it reaches back to the agent in two ways: **frontend tools**, which the agent calls to put
something on screen, and **shared state**, which the agent snapshots or patches. Building UI here
means adding components the agent can place, not hand-writing screens around a chat box.

## Step 1: pick the canvas

- **The user gave a template** (a path, a repo, or an existing app): build on it. Find its three
  seams, listed below, before writing anything. If a seam is missing, add the smallest version of
  it that matches the template's own style. Do not replace their structure with the default.
- **No template**: copy `${CLAUDE_SKILL_DIR}/assets/canvas-template/` into the project (default:
  `web/` and `agent/` at the repo root, or wherever the user says). Always copy it, and never edit
  the files under the skill directory.

The default canvas is empty on purpose: a component area that says it is empty, a chat panel, and
an empty registry. Its three seams:

| Seam | Default file | Owns |
|------|--------------|------|
| Agent connection | `web/src/useAgent.ts` | One `HttpAgent` per page, the subscription, the tool-call round loop |
| Component registry | `web/src/registry.ts` | `{ name, description, parameters, Component }` per placeable component |
| Canvas render | `web/src/App.tsx` | Looks up each rendered block in the registry, then renders chat, error, and Stop |

Run it before changing anything (commands in the template `README.md`): send `hello` and check
that `You said: hello` streams back. A canvas that never ran end to end hides every later bug.

## Step 2: add components, one registry entry each

For each piece of UI the user wants, add one entry to the registry. The entry **is** the tool
definition: `name`, `description`, and `parameters` (JSON Schema) are sent to the agent as a
frontend tool on every run, and the arguments the agent sends back become the component's props.

```tsx
function MetricCard({ label, value }: { label: string; value: number }) {
  return (
    <section className="card" aria-label={label}>
      <h2>{label}</h2>
      <p>{value.toLocaleString()}</p>
    </section>
  );
}

export const registry: CanvasComponent[] = [
  {
    name: "show_metric",
    description: "Show one headline number with its label. Use for a single KPI, not a series.",
    parameters: {
      type: "object",
      properties: { label: { type: "string" }, value: { type: "number" } },
      required: ["label", "value"],
    },
    Component: MetricCard,
  },
];
```

Rename `registry.ts` to `.tsx` once it holds JSX, or keep components in their own files and import
them. The rules the agent depends on:

- **The description is written for the agent.** Say what the component shows and when to pick it
  over the others. Two components with overlapping descriptions get called interchangeably.
- **Name tools as verbs in snake_case** (`show_metric`, `render_table`). Tool names cross into
  Python and LLM tool APIs, which reject spaces and dots.
- **Treat props as untrusted input.** The agent can omit a required field or send the wrong type.
  Make each component survive that: default or skip missing fields, and validate with a schema
  library if the project already has one. Never pass agent text to `dangerouslySetInnerHTML`.
- **Components stay presentational** (the `react-vite` convention): props in, markup out, no
  `fetch`. Data the component needs arrives as arguments or through shared state.
- **Keep the markup accessible.** A labelled region per card, real headings, and the chat's
  `aria-live` list left as it is.

## Step 3: choose tool call or shared state

| The agent needs to… | Use | In the canvas |
|---------------------|-----|---------------|
| Put a new thing on screen | Frontend tool (a registry entry) | A new block in `blocks` |
| Keep a live value the UI mirrors (progress, a plan, a document) | `STATE_SNAPSHOT` / `STATE_DELTA` | `state` from `useAgent`, rendered by a component that reads it |
| Ask the user something before continuing | A frontend tool whose component collects input | Delay the tool result until the user answers |

`useAgent` already exposes `state` through `onStateChanged`. Render it directly and do not copy it
into a second store. Blocks are UI-owned, so the agent cannot remove one. If it needs to, have it
keep the list in shared state and render from that.

## The loop the canvas runs, and how it breaks

`send()` adds the user message, then calls `runAgent({ tools })`. When the run ends, it looks for
calls to registry tools in `newMessages`. It renders each one, appends a `role: "tool"` message
with the same `toolCallId`, and runs the agent again so the agent can respond. It stops when a run
makes no frontend calls, or after `MAX_TOOL_ROUNDS`.

- **Every frontend tool call needs a tool message before the next run.** An unanswered call makes
  most LLM providers reject the whole conversation on the next turn.
- **`tools` goes out on every run.** The agent is stateless about them, so a registry change
  applies on the next message with no restart.
- **Calls to tools that are not in the registry are left alone.** Those belong to the backend,
  which answers them itself.
- **Create the agent once** (`useMemo`) and unsubscribe in the effect cleanup. Under StrictMode,
  effects run twice in development. A second `HttpAgent` would split the conversation in two.
- **Stop is `abortRun()`.** It does not undo a block that was already rendered.

## Step 4: verify each component, then swap the agent

The mock agent in `agent/main.py` uses no LLM. `<tool-name> <json-args>` becomes a call to that
frontend tool, and anything else is echoed back. For every component you add:

1. Type `show_metric {"label":"Users","value":1200}`. It should render, and the chat should say
   `Rendered on the canvas.`
2. Send it with a required field missing. The component must not crash the page.

Then point the canvas at the real agent. Any server that accepts a `RunAgentInput` POST and
streams AG-UI events works, whatever framework it uses. For a dev proxy, set `AGENT_ORIGIN`: Vite
forwards `/agent` there, so no CORS setup is needed. For a deployed build, set `VITE_AGENT_URL`,
and the agent must then allow the UI's origin. If the real agent serves a path other than `/agent`,
change the proxy key in `vite.config.ts` to match. Delete `agent/` once it is unused.

## Done when

- The canvas starts empty and runs end to end against the mock and against the real agent.
- Every registry entry renders from a mock call and survives missing arguments.
- No frontend tool call is left without a tool message, and no agent text reaches raw HTML.
