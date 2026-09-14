"""The dedup rule. The v1 defect's other hiding place (review 2.7)."""

from jarvis_brain.memory import dedup
from jarvis_brain.turn import Candidate, Source


def _cmd(polarity: str) -> Candidate:
    return Candidate(
        intent="HassTurnOn" if polarity == "on" else "HassTurnOff",
        entity_id="light.bedroom",
        slots={},
        source=Source.RETRIEVER,
        raw_score=0.94,
    )


def test_opposite_polarities_never_merge():
    """These sit at ~0.94 cosine. v1 would have merged them at its 0.92 threshold."""
    assert not dedup.may_merge(_cmd("on"), _cmd("off"))


def test_identical_tuple_merges():
    assert dedup.may_merge(_cmd("on"), _cmd("on"))


def test_different_slots_never_merge():
    left, right = _cmd("on"), _cmd("on")
    left.slots, right.slots = {"temperature": 18}, {"temperature": 28}
    assert not dedup.may_merge(left, right)
