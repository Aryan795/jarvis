"""The two-decoder agreement rule (review 2.2).

The polarity guard reads the transcript, so if STT itself flips "off" to "on" the guard
cannot see the error. A second, independent decoder is what closes that hole.
"""

from __future__ import annotations

import dataclasses

from ..turn import Transcript


@dataclasses.dataclass(slots=True)
class Agreement:
    polarity_agrees: bool
    entity_agrees: bool
    quantity_agrees: bool

    @property
    def ok(self) -> bool:
        return self.polarity_agrees and self.entity_agrees and self.quantity_agrees


def compare(transcripts: list[Transcript]) -> Agreement:
    """Compare decoders on the three things that change which action fires.

    Wording differences are ignored. "Turn the bedroom light off" and "bedroom light off"
    agree. "Turn the bedroom light on" and "bedroom light off" do not, and that turn becomes
    a clarify turn rather than an announcement.

    With fewer than two transcripts every field is True: there is nothing to disagree with,
    and the Whisper-only rules apply from there.
    """
    raise NotImplementedError("build order step 6")
