"""The guard chain. Candidates in, one Decision out.

Order matters and is fixed. Cheap deterministic checks that can refuse outright run before
anything that costs time, and confidence is the last thing consulted, never the first.

1. **Agreement** — do the two decoders agree on polarity, entity and quantity? (2.2)
2. **Polarity** — does the candidate contradict the raw transcript?
3. **Quantity** — does every numeric slot appear in what was said? (2.6)
4. **Exposure** — is the entity actually exposed to Assist? Fails closed.
5. **Fitted** — has this matcher's calibration been fitted on real turns?
6. **Confidence** — is P(correct) over the threshold, and is the runner-up far enough back?
7. **Tier** — act, announce then act, or confirm first.

A refusal is never silence. Every branch ends in speech, and an uncertain turn ends in a
question with the microphone reopened.
"""

from __future__ import annotations

from ..turn import Candidate, Decision, TurnInput


class GuardChain:
    def evaluate(self, turn: TurnInput, candidates: list[Candidate]) -> Decision:
        """Run the chain and return the decision, including what to say.

        Never raises on an unrecognised input. An unreadable turn is a clarify turn.
        """
        raise NotImplementedError("build order step 2")
