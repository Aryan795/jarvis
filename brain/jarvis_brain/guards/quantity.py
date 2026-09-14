"""The quantity guard. Polarity's twin for anything with a setpoint (review 2.6).

Setpoints have no polarity. "Set the AC to 18" and "set the AC to 28" share the verb and
the entity and differ by one digit, and the AC is tier B. So numbers and units are pulled
from the raw transcript and the candidate's slot value must equal them.

The other half of this rule lives in ``response.phrases``: a tier B announcement echoes the
slot ("setting the bedroom AC to 18") so a wrong number is audible in the announce window,
the same way a wrong polarity is.
"""

from __future__ import annotations

import dataclasses


@dataclasses.dataclass(slots=True)
class Quantity:
    value: float
    unit: str | None


def extract(text: str) -> list[Quantity]:
    """Pull every number and unit from the raw transcript.

    Words as well as digits: "eighteen" and "18" are the same quantity. Whisper writes
    either depending on context, so a digits-only reader would silently pass turns it
    should have checked.
    """
    raise NotImplementedError("build order step 4")


def agrees(transcript: str, slots: dict[str, object]) -> bool:
    """True when every numeric slot on the candidate appears in the transcript.

    A candidate carrying a number the user never said is a disagreement, even when the
    number is plausible — especially then, since a remembered setpoint is exactly the kind
    of plausible wrong answer retrieval produces.
    """
    raise NotImplementedError("build order step 4")
