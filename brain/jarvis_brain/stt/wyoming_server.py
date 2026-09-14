"""A Wyoming STT endpoint that fans one audio stream to two decoders.

HA's pipeline takes exactly one STT engine, so the brain exposes itself as that engine and
does the fan-out internally. It keeps the audio hash and both transcripts for the replay
log and returns whichever transcript the agreement rules allow.

The conversation step arrives milliseconds later with identical text, so the brain pairs
the two on text and recency. If the pairing is ever ambiguous it drops to the Whisper-only
rules rather than guessing which utterance it is looking at.

Wyoming is JSON lines plus audio chunks over TCP; the ``wyoming`` package provides the
server and client classes. This is glue, not a subsystem.
"""

from __future__ import annotations

from ..turn import Transcript


class BrainSttServer:
    """Serves the Wyoming STT protocol and fans audio to Whisper and the grammar decoder."""

    async def start(self, host: str, port: int) -> None:
        raise NotImplementedError("build order step 6")

    async def handle_utterance(self, pcm: bytes) -> list[Transcript]:
        """Run both decoders on the same audio and return every opinion.

        Both run concurrently. The grammar decoder normally finishes first — HA quotes
        speech-to-phrase at under a second on a Pi 4, so tens of milliseconds is expected on
        the i5, to be measured — but the result waits for both, because the agreement rule
        needs both and tier is not known yet at this point in the pipeline.
        """
        raise NotImplementedError("build order step 6")
