"""Wyoming clients for the two decoders. Both are local containers on the i5."""

from __future__ import annotations

from ..turn import Transcript


class WhisperDecoder:
    """wyoming-faster-whisper running ``distil-small.en`` int8, roughly 1 GB.

    No ``initial_prompt`` is ever sent: distil models were distilled without previous-text
    conditioning, and wyoming-faster-whisper warns at startup when a prompt is combined with
    one (review 2.3). Entity spelling is fixed by hassil's fuzzy matching and by the grammar
    decoder instead, which is where it belongs — Whisper only ever sees out-of-grammar
    speech once the grammar decoder is in place, and that is where entity biasing matters
    least.
    """

    async def transcribe(self, pcm: bytes) -> Transcript:
        raise NotImplementedError("build order step 1")


class GrammarDecoder:
    """speech-to-phrase, ~0.3 GB. Its language model is built from the exposed entities.

    Rebuilt whenever the exposed-entity set changes, so its vocabulary and the brain's stay
    the same set.
    """

    async def transcribe(self, pcm: bytes) -> Transcript:
        raise NotImplementedError("build order step 6")

    async def rebuild_language_model(self, entities: list[str], areas: list[str]) -> None:
        raise NotImplementedError("build order step 6")
