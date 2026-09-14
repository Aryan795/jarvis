"""Tier 1: semantic retrieval over remembered commands. Proposes, never decides.

bge-small as ONNX on CPU, vectors in the same SQLite file through sqlite-vec. In practice
this only matters when hassil misses or matches fuzzily — the race is a cascade with one
exception, and this is the exception (review 2.5).

This is the module the v1 defect lived in. It returns candidates with a raw score and
nothing else; the guard chain decides. Cosine cannot see polarity, and "turn on X" and
"turn off X" sit near 0.94, so a similarity number never reaches an action from here.
"""

from __future__ import annotations

from ..turn import Candidate


class Retriever:
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError("build order step 3")

    def search(self, text: str, top_k: int = 5) -> list[Candidate]:
        """Return the top k remembered commands as candidates with raw cosine scores.

        Callers must not read ``raw_score`` for any purpose other than handing it to the
        calibrator.
        """
        raise NotImplementedError("build order step 3")
