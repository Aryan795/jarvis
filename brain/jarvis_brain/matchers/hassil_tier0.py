"""Tier 0: hassil, in-process, as a matcher that cannot act (review 2.1).

Home Assistant's built-in agent uses hassil too, but it has no dry-run mode: asking it to
match over the WebSocket would execute. So the library runs here instead, with slot lists
pulled over the WebSocket from the same exposed-entity, area and floor registries Assist
uses. The brain only ever sees exposed entities, exactly as Assist does, so the vocabulary
and the blast radius stay bounded.

Two consequences accepted with this: sentence-trigger automations only fire under local
preference, which is off, so any of the 79 that use them move into the brain's intent set.
"""

from __future__ import annotations

import enum

from ..turn import Candidate


class Bucket(enum.StrEnum):
    """hassil returns a match or nothing. It has no scalar score, so there is no curve to
    fit — what tier 0's "calibration" really is is a per-bucket prior from the audit log
    (review 2.5)."""

    EXACT = "exact"
    """Template matched, every slot resolved. This bucket wins every race it enters."""

    FUZZY = "fuzzy"
    """Matched through fuzzy matching. The retriever is worth consulting here."""

    UNMATCHED_ENTITY = "unmatched_entity"
    """Template matched but the entity did not resolve. Usually a clarify turn."""

    NONE = "none"
    """No match. The retriever is the only proposal."""


class HassilMatcher:
    """Wraps ``hassil`` plus ``home-assistant-intents`` over the exposed-entity slot lists."""

    async def load_slot_lists(self) -> None:
        """Pull exposed entities, areas and floors over the HA WebSocket.

        Called at startup and whenever the exposure set changes. An entity that is not
        exposed to Assist must never enter the slot lists.
        """
        raise NotImplementedError("build order step 2")

    def match(self, text: str, area: str | None) -> tuple[Candidate | None, Bucket]:
        """Match one utterance. Returns the candidate and which bucket it came from.

        The bucket, not a score, is what the calibrator reads.
        """
        raise NotImplementedError("build order step 2")
