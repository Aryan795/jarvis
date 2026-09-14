"""FastAPI entry point. The brain is the pipeline's only conversation agent.

Two surfaces:

* ``POST /conversation`` — called by the Jarvis custom component on the Pi with the text,
  ``device_id``, ``satellite_id`` and ``conversation_id`` of every turn.
* A Wyoming STT server on its own TCP port (see ``stt.wyoming_server``), which HA's
  pipeline points at as its single STT engine. The brain fans the audio to both decoders
  and returns whichever transcript the agreement rules allow (review 2.2).

Home Assistant's own matcher never runs: "Prefer handling commands locally" stays off and
hassil runs in-process here instead, because HA's built-in agent has no dry-run mode and
would execute rather than match (review 2.1).
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .config import Config
from .turn import TurnInput

app = FastAPI(title="Jarvis brain", version="0.1.0")


class ConversationRequest(BaseModel):
    text: str
    conversation_id: str | None = None
    device_id: str | None = None
    satellite_id: str | None = None
    language: str = "en"


class ConversationResponse(BaseModel):
    speech: str
    continue_conversation: bool = False
    conversation_id: str | None = None


@app.post("/conversation", response_model=ConversationResponse)
async def conversation(req: ConversationRequest) -> ConversationResponse:
    """Run one turn through the cascade and return what to say.

    The cascade, in order: pair the text with the transcripts the STT stage kept, resolve
    the device to an area, race hassil against the retriever, calibrate, run the guard
    chain, execute over the WebSocket, verify state, log the turn.
    """
    raise NotImplementedError("build order step 2")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


def run() -> None:
    """Start the HTTP app and the Wyoming STT server together."""
    raise NotImplementedError("build order step 1")
