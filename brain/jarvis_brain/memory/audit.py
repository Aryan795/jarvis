"""The audit log, including turns the brain never saw.

The moment MultiNet handles the hot set on the satellite, the brain stops seeing the
majority of turns — which is exactly the population the thresholds were meant to be fitted
on. So the satellite emits a compact event for every on-device decision (command id, top
two probabilities, timestamp) through the ESPHome native API as an ``event`` entity, and
the brain, already subscribed to HA's event stream, logs it as a turn with its own tier
label (review 2.4).

When the brain is down those events are lost. That is accepted: the state changes are still
in HA's recorder, and the population that matters for fitting is the steady state.
"""

from __future__ import annotations

from typing import Any


class AuditLog:
    async def watch_satellite_events(self) -> None:
        """Subscribe to the satellite's event entity and log every on-device decision."""
        raise NotImplementedError("build order step 4")

    def log_satellite_decision(self, event: dict[str, Any]) -> None:
        raise NotImplementedError("build order step 4")

    def pair_with_brain_decision(self, event_id: int) -> None:
        """During shadow the audio is streamed anyway, so every on-device prediction has a
        paired brain decision for the same utterance to be scored against."""
        raise NotImplementedError("build order step 4")
