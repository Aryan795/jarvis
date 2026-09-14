"""The polarity guard. Reads the raw transcript, not the candidate's embedding.

This is the guard that exists because of the v1 defect. A candidate that says "turn off"
while the user said "turn on" is refused here, regardless of how confident retrieval was.

Deliberately a lexicon and not a model. It has to be auditable, it has to be testable from
a table of pairs, and it has to fail closed on anything it does not recognise.
"""

from __future__ import annotations

import enum


class Polarity(enum.StrEnum):
    ON = "on"
    OFF = "off"
    OPEN = "open"
    CLOSE = "close"
    LOCK = "lock"
    UNLOCK = "unlock"
    UP = "up"
    DOWN = "down"
    NONE = "none"
    """No polarity in the utterance. Setpoints land here — see ``quantity``."""


#: Surface forms to polarity. Extended from the audit log, never from intuition.
LEXICON: dict[str, Polarity] = {
    "on": Polarity.ON,
    "off": Polarity.OFF,
    "open": Polarity.OPEN,
    "close": Polarity.CLOSE,
    "shut": Polarity.CLOSE,
    "lock": Polarity.LOCK,
    "unlock": Polarity.UNLOCK,
    "up": Polarity.UP,
    "down": Polarity.DOWN,
    "raise": Polarity.UP,
    "lower": Polarity.DOWN,
}

#: Pairs that must never be substituted for one another.
OPPOSITES: dict[Polarity, Polarity] = {
    Polarity.ON: Polarity.OFF,
    Polarity.OFF: Polarity.ON,
    Polarity.OPEN: Polarity.CLOSE,
    Polarity.CLOSE: Polarity.OPEN,
    Polarity.LOCK: Polarity.UNLOCK,
    Polarity.UNLOCK: Polarity.LOCK,
    Polarity.UP: Polarity.DOWN,
    Polarity.DOWN: Polarity.UP,
}


def extract(text: str) -> Polarity:
    """Find the polarity in an utterance, or NONE.

    "Turn off the light" is OFF. "Don't turn on the light" is not ON — negation flips it,
    and an utterance whose polarity cannot be read unambiguously returns NONE, which the
    chain treats as grounds to ask.
    """
    raise NotImplementedError("build order step 2")


def agrees(transcript: str, candidate_polarity: Polarity) -> bool:
    """True when the candidate does not contradict what was actually said.

    NONE in the transcript with a definite polarity in the candidate is a disagreement:
    the candidate invented a direction the user did not give.
    """
    raise NotImplementedError("build order step 2")
