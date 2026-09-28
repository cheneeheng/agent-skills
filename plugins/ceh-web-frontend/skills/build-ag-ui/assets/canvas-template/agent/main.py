"""Mock AG-UI agent: no LLM, deterministic, so the canvas can be exercised end to end.

- `<tool-name> <json-args>` where <tool-name> is a frontend tool the UI sent -> calls that tool.
- A tool result as the last message -> acknowledges it.
- Anything else -> echoes the text back.

Replace this file with a real agent; the canvas only depends on the AG-UI event stream.
"""

import json
import uuid
from collections.abc import AsyncIterator

from ag_ui.core import (
    BaseEvent,
    RunAgentInput,
    RunFinishedEvent,
    RunStartedEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
    TextMessageStartEvent,
    ToolCallArgsEvent,
    ToolCallEndEvent,
    ToolCallStartEvent,
)
from ag_ui.encoder import EventEncoder
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()


def say(text: str) -> list[BaseEvent]:
    message_id = str(uuid.uuid4())
    return [
        TextMessageStartEvent(message_id=message_id, role="assistant"),
        TextMessageContentEvent(message_id=message_id, delta=text),
        TextMessageEndEvent(message_id=message_id),
    ]


def call_tool(name: str, args: str) -> list[BaseEvent]:
    call_id = str(uuid.uuid4())
    return [
        ToolCallStartEvent(tool_call_id=call_id, tool_call_name=name),
        ToolCallArgsEvent(tool_call_id=call_id, delta=args),
        ToolCallEndEvent(tool_call_id=call_id),
    ]


def respond(run: RunAgentInput) -> list[BaseEvent]:
    last = run.messages[-1] if run.messages else None
    if last is None:
        return say("Say something.")
    if last.role == "tool":
        return say("Rendered on the canvas.")
    text = last.content if isinstance(last.content, str) else ""
    name, _, args = text.strip().partition(" ")
    if name in {tool.name for tool in run.tools or []}:
        try:
            json.loads(args or "{}")
        except json.JSONDecodeError:
            return say(f"Arguments for {name} must be a JSON object.")
        return call_tool(name, args or "{}")
    return say(f"You said: {text}")


@app.post("/agent")
async def agent(run: RunAgentInput, request: Request) -> StreamingResponse:
    encoder = EventEncoder(accept=request.headers.get("accept"))

    async def stream() -> AsyncIterator[str]:
        yield encoder.encode(RunStartedEvent(thread_id=run.thread_id, run_id=run.run_id))
        for event in respond(run):
            yield encoder.encode(event)
        yield encoder.encode(RunFinishedEvent(thread_id=run.thread_id, run_id=run.run_id))

    return StreamingResponse(stream(), media_type=encoder.get_content_type())
