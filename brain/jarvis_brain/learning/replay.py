"""Replay the audit log against a changed threshold or a new fit before shipping it.

The question this answers: of the turns already logged, which decisions would change, and
would any of them have been wrong? A change that would have flipped a tier C action or a
polarity is rejected regardless of what it improves on average.
"""

from __future__ import annotations

import dataclasses


@dataclasses.dataclass(slots=True)
class ReplayResult:
    n_turns: int
    changed: int
    newly_correct: int
    newly_wrong: int
    polarity_flips: int
    """Must be zero. Any flip rejects the change outright."""

    tier_c_changes: int
    """Must be zero for the same reason."""


class ReplayHarness:
    def run(self, since: str | None = None) -> ReplayResult:
        raise NotImplementedError("build order step 5")
