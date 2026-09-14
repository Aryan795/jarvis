"""When two remembered commands may be merged. The answer is: almost never automatically.

The rule, from review 2.7: a merge requires an identical ``(intent, polarity, entity, slot)``
tuple. Similarity may only add a pair to the review list.

v1 merged anything above 0.92 cosine, which is the 0.85 defect wearing a different hat, and
would have quietly merged "bedroom light on" with "bedroom light off" — putting the defect
into the memory layer, where it survives being fixed in the router.
"""

from __future__ import annotations

from ..turn import Candidate


def may_merge(left: Candidate, right: Candidate) -> bool:
    """True only for an exact tuple match. Similarity is not an input to this function."""
    raise NotImplementedError("build order step 3")


def propose_for_review(left_id: int, right_id: int, similarity: float) -> None:
    """Record a similar pair for a human to look at. Does not merge anything."""
    raise NotImplementedError("build order step 3")
