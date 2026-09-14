"""Runtime configuration. Every threshold here is fitted from the audit log, not guessed.

The defaults below are placeholders that exist so the code runs. Section 5 of the build
order replaces each one with a value measured on real turns. A threshold that has never
been fitted is marked `UNFITTED` and the guard chain refuses to act on tiers B and C
while any threshold it depends on is still unfitted.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

UNFITTED = -1.0


class HomeAssistantConfig(BaseModel):
    url: str = "http://homeassistant.local:8123"
    token: str = ""
    """Long-lived access token. Read from the environment, never committed."""


class SttConfig(BaseModel):
    whisper_uri: str = "tcp://127.0.0.1:10300"
    """wyoming-faster-whisper, distil-small.en int8.

    The review (2.3) establishes that distil models and an entity-name `initial_prompt` are
    incompatible: distil-whisper was distilled without previous-text conditioning, and a
    prompt over ~50 tokens drops the average log-probability under faster-whisper's cutoff,
    so output truncates or loops. Entity names run well past 50 tokens. No prompt is sent.
    """

    grammar_uri: str = "tcp://127.0.0.1:10301"
    """speech-to-phrase, a Kaldi decoder whose LM is built from the exposed entities.

    Answers "which of the phrases I know did you say", which is what tier 0 needs, and its
    output names are guaranteed to be real HA names.
    """

    require_agreement_at_tier: int = 1
    """Tier B and above require both decoders to agree on polarity and entity (2.2).

    Disagreement becomes a clarify turn, never a best guess.
    """

    grammar_alone_allowed: bool = False
    """Whether tier A may act on the grammar decoder's transcript alone.

    Stays False until shadow data shows speech-to-phrase does not force-decode
    out-of-grammar speech into a valid in-grammar sentence. That behaviour is undocumented,
    so it is measured before it is relied on.
    """


class MatcherConfig(BaseModel):
    retriever_model: str = "models/bge-small-en-v1.5.onnx"
    classifier_model: str = "models/intent-slot-distilbert.onnx"
    retriever_top_k: int = 5

    min_calibrated_confidence: float = UNFITTED
    """P(correct) below which the brain asks instead of acting."""

    clarify_margin: float = UNFITTED
    """Minimum gap between the top two candidates. A close pair is a question, not a guess."""


class GuardConfig(BaseModel):
    announce_window_seconds: float = 2.5
    """Tier B: how long the announcement runs before the action fires."""

    require_quantity_match: bool = True
    """Tier B with a setpoint: the candidate's slot value must equal the number in the raw
    transcript. "Set the AC to 18" and "set the AC to 28" differ by one digit and share the
    verb and the entity (review 2.6)."""


class MemoryConfig(BaseModel):
    db_path: str = "data/jarvis.db"
    """One SQLite file with sqlite-vec. The single source of truth.

    v1 had four stores that drifted: two FAISS indexes, a SQLite DB, RAM short-term memory
    and an episodic store. One store, one truth (review, table in section 1).
    """

    merge_requires_identical_tuple: bool = True
    """A memory merge requires an identical (intent, polarity, entity, slot) tuple.

    Similarity may only propose candidates for a human review list. v1 merged at cosine
    above 0.92, which is the 0.85 defect wearing a different hat, and would merge the two
    polarities of the same command into one memory (review 2.7). Do not set this False.
    """


class Config(BaseModel):
    ha: HomeAssistantConfig = Field(default_factory=HomeAssistantConfig)
    stt: SttConfig = Field(default_factory=SttConfig)
    matcher: MatcherConfig = Field(default_factory=MatcherConfig)
    guard: GuardConfig = Field(default_factory=GuardConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)

    shadow_mode: bool = True
    """While True the brain scores and logs but never executes. The starting state."""

    @classmethod
    def load(cls, path: str | None = None) -> "Config":
        """Load from YAML with environment overrides for secrets."""
        raise NotImplementedError("build order step 1")
