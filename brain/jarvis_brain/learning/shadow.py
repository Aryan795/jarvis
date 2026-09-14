"""Shadow mode: predict, score, do not act.

Everything new enters the system this way — a new matcher, a new threshold, a new on-device
command. The rule from v2 stands: promotion is earned from the audit log, not scheduled.

For the satellite (review 3.5) the bar is explicit. A command is promoted to acting only
when its shadow record shows **zero polarity disagreements** and an agreement rate set from
the data. Commands whose pair confuses acoustically get a phonetically distinct alias for
the safer direction, or come out of the table.
"""

from __future__ import annotations

import dataclasses


@dataclasses.dataclass(slots=True)
class ShadowRecord:
    command_id: str
    n: int
    agreements: int
    polarity_disagreements: int

    @property
    def agreement_rate(self) -> float:
        return self.agreements / self.n if self.n else 0.0


class ShadowEvaluator:
    def record(self, command_id: str, agreed: bool, polarity_agreed: bool) -> None:
        raise NotImplementedError("build order step 4")

    def may_promote(self, command_id: str) -> bool:
        """Zero polarity disagreements, and an agreement rate over the fitted threshold.

        Returns False while the sample is too small. "No evidence against" is not evidence.
        """
        raise NotImplementedError("build order step 5")
