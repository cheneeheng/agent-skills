# ceh-ag-ui

Generative-UI canvases for agents that speak the [AG-UI](https://docs.ag-ui.com) protocol. The
user types; the agent answers by placing components from a **catalogue fixed at build time**,
styled only by the theme (Tidewater by default, from `ceh-web-frontend:ui-design`). The agent picks
the component and fills in the content — it can never change how anything looks.

All five skills are **build-time**: Claude Code loads one while writing your app, and none runs
inside the running app. Worked examples, prompt by prompt:
[examples/ceh-ag-ui](https://github.com/cheneeheng/agent-skills/tree/main/examples/ceh-ag-ui).

Depends on `ceh-web-frontend` for the theme contract (`ui-design`) the canvas and every catalogue
component are built against.

## Skills (auto-trigger)

| Skill | Invoke | Triggers when |
|-------|--------|---------------|
| Build AG-UI | `/ceh-ag-ui:build-ag-ui` | Starting a generative-UI canvas for an AG-UI agent — uses the user's own template or copies the bundled one (React + Vite + `@ag-ui/client`, seven Tidewater-styled catalogue components, a deterministic mock agent), installs the theme, and enforces the three-layer styling lock |
| Add Canvas Component | `/ceh-ag-ui:add-canvas-component` | Adding or changing a catalogue component — the tool name and agent-facing description, a content-only zod schema (no styling props), the example that doubles as a fixture, a theme-only component, and verification against the mock |
| Build AG-UI Agent | `/ceh-ag-ui:build-ag-ui-agent` | Building the agent server behind the canvas — a bundled FastAPI + Claude server that keeps the model's own append-only transcript per thread, ends the run on a frontend tool call, and holds backend results until the canvas answers |
| Add Live State Panel | `/ceh-ag-ui:add-live-state-panel` | The canvas needs a live value the agent updates as it works — `STATE_SNAPSHOT` / `STATE_DELTA` (JSON Patch), one writer per key, a fixed validated state panel, UI-to-agent state |
| Add Human Approval | `/ceh-ag-ui:add-human-approval` | The agent must get the user's decision before acting — AG-UI 1.0 interrupts: interrupt outcome, a fixed approval card, one `resume` covering every open interrupt, cancel-on-type, single-use approvals |

## Bundled assets

| Path | What it is |
|------|------------|
| `skills/build-ag-ui/assets/canvas-template/` | The default canvas (`web/`) and the no-LLM mock agent (`agent/`) |
| `skills/build-ag-ui-agent/assets/agent-server/` | The Claude-backed AG-UI server (`main.py`, `pyproject.toml`) |
