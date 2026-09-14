"""The phrase bank. Every response is a template with slots, written ahead of time.

Two reasons it is written rather than generated. There is no generative model in this
system by decision, and a fixed bank can be rendered to FLAC at build time and shipped in
the satellite's flash, so an acknowledgement survives the brain being down (review 3.7).

The same Piper voice renders the clips and the server responses, so a clip and a live
response are indistinguishable.

The announcement rules are load-bearing, not cosmetic:

* Tier A acknowledgements **name the action** ("bedroom light off"), never just "done", so a
  wrong polarity is audible immediately.
* Tier B announcements **echo the slot value** ("setting the bedroom AC to 18") so a wrong
  number is caught in the announce window (review 2.6).
* Every failure branch ends in speech. Silence is never a valid outcome.
"""

from __future__ import annotations

PHRASES: dict[str, str] = {
    # Tier A: act, then name what was done.
    "ack.action": "{friendly_name} {polarity}",
    # Tier B: announce with the number, then act after the window.
    "announce.setpoint": "setting the {friendly_name} to {value}{unit}",
    "announce.action": "{verb} the {friendly_name}",
    # Tier C: ask, and wait for a real answer.
    "confirm.tier_c": "confirm: {verb} the {friendly_name}?",
    # Uncertainty. Always a question, never a guess, never silence.
    "clarify.ambiguous_entity": "which {friendly_name}? {options}",
    "clarify.polarity": "on or off?",
    "clarify.disagreement": "did you say {option_a} or {option_b}?",
    "clarify.no_match": "I didn't catch that",
    # Failure. Each of these also exists as a clip in the satellite's flash.
    "error.brain_unreachable": "brain unreachable",
    "error.hub_unreachable": "hub unreachable",
    "error.not_verified": "{friendly_name} did not respond",
    "error.refused": "I won't do that without confirmation",
}


def render(key: str, **slots: object) -> str:
    """Render a phrase. Raises on an unknown key or a missing slot rather than degrading.

    A response with an unfilled slot is a bug that must be loud in testing, not a sentence
    with a hole in it read aloud in the living room.
    """
    raise NotImplementedError("build order step 2")


def clip_id_for(key: str, **slots: object) -> str | None:
    """The embedded clip matching a phrase, if one was rendered at build time.

    Returns None for anything with an open slot value, which the server renders instead.
    """
    raise NotImplementedError("build order step 3")
