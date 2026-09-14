"""The data that flows through one turn. Shared by every stage of the cascade."""

from __future__ import annotations

import dataclasses
import enum
from typing import Any

from .tiers import Tier


class Source(enum.StrEnum):
    """Where a decision came from. Recorded on every turn for the audit log."""

    HASSIL = "hassil"
    """Tier 0. Deterministic template match. Wins every race it enters (review 2.5)."""

    RETRIEVER = "retriever"
    """Tier 1. Proposes only when hassil misses or matches fuzzily."""

    CLASSIFIER = "classifier"
    """Tier 2. DistilBERT intent + slot. Classification, not generation."""

    SATELLITE = "satellite"
    """Decided on the ESP32 by MultiNet. Arrives as an audit event, not a turn (2.4)."""


class Outcome(enum.StrEnum):
    ACTED = "acted"
    ANNOUNCED_THEN_ACTED = "announced_then_acted"
    CONFIRMED_THEN_ACTED = "confirmed_then_acted"
    CLARIFIED = "clarified"
    """Asked a question and reopened the microphone. Never a guess, never silence."""
    REFUSED = "refused"
    SHADOWED = "shadowed"
    """Scored and logged, not executed."""


@dataclasses.dataclass(slots=True)
class Transcript:
    """One decoder's opinion of what was said."""

    text: str
    decoder: str
    confidence: float | None = None


@dataclasses.dataclass(slots=True)
class TurnInput:
    """What Home Assistant hands the conversation agent, plus what the STT stage kept."""

    text: str
    conversation_id: str | None
    device_id: str | None
    """The satellite's HA device id. Resolves to an area — this is the context injector."""
    satellite_id: str | None
    language: str = "en"

    transcripts: list[Transcript] = dataclasses.field(default_factory=list)
    """Every decoder's output for this utterance, paired by text and recency (review 2.2).

    Empty when the turn arrived as text without audio, in which case the agreement rule
    cannot run and the brain falls back to the Whisper-only rules.
    """

    audio_hash: str | None = None
    """Identifies the utterance in the replay log without storing the audio."""


@dataclasses.dataclass(slots=True)
class Candidate:
    """A proposed action. Proposing is all a matcher may do."""

    intent: str
    entity_id: str | None
    slots: dict[str, Any]
    source: Source
    raw_score: float
    """Whatever the matcher produced. Not comparable across matchers — never compared."""

    calibrated: float = 0.0
    """P(correct), from the per-matcher fit. The only score the guard chain reads."""

    @property
    def tier(self) -> Tier:
        from .tiers import Tier as _T, tier_for

        return tier_for(self.entity_id) if self.entity_id else _T.C


@dataclasses.dataclass(slots=True)
class Decision:
    """What the guard chain concluded. The only thing the executor accepts."""

    candidate: Candidate | None
    outcome: Outcome
    speech: str
    continue_conversation: bool = False
    """Set on a clarify turn. HA reopens the satellite's microphone without a wake word."""
    refused_by: str | None = None
    """Name of the guard that stopped it. Written to the audit log."""
