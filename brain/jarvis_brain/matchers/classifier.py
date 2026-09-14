"""Tier 2: a DistilBERT-class intent and slot classifier as ONNX, CPU.

Classification, not generation. There is no LLM anywhere in this path, by decision. v1's
diagram promised Gemma 3:4B at 200-400 ms on this hardware; the real figure is 5-10 s, and
the cloud fallback it leaned on contradicts the offline requirement outright.

This runs only when tier 0 and tier 1 both come up short, and its output is a candidate
like any other: it goes through the same guard chain.
"""

from __future__ import annotations

from ..turn import Candidate


class IntentSlotClassifier:
    def classify(self, text: str) -> Candidate | None:
        raise NotImplementedError("build order step 4")
