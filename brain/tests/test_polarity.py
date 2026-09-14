"""The polarity guard's test table. This is the regression test for the v1 defect.

Every pair here is one the retriever will happily rank at 0.94 cosine. If any of these
start passing the guard, the system is back to v1 behaviour.
"""

import pytest

from jarvis_brain.guards import polarity
from jarvis_brain.guards.polarity import Polarity

OPPOSITE_PAIRS = [
    ("turn on the bedroom light", Polarity.OFF),
    ("turn off the bedroom light", Polarity.ON),
    ("open the curtains", Polarity.CLOSE),
    ("close the curtains", Polarity.OPEN),
    ("lock the front door", Polarity.UNLOCK),
    ("unlock the front door", Polarity.LOCK),
]


@pytest.mark.parametrize("transcript,candidate_polarity", OPPOSITE_PAIRS)
def test_opposite_polarity_is_refused(transcript, candidate_polarity):
    assert not polarity.agrees(transcript, candidate_polarity)


@pytest.mark.parametrize(
    "transcript,expected",
    [
        ("turn on the bedroom light", Polarity.ON),
        ("turn off the bedroom light", Polarity.OFF),
        ("bedroom light off", Polarity.OFF),
        ("set the ac to 18", Polarity.NONE),
    ],
)
def test_extract(transcript, expected):
    assert polarity.extract(transcript) == expected


def test_negation_flips_polarity():
    assert polarity.extract("don't turn on the light") != Polarity.ON


def test_invented_polarity_is_a_disagreement():
    """The transcript has no direction; the candidate supplies one. That is not agreement."""
    assert not polarity.agrees("the bedroom light", Polarity.ON)
