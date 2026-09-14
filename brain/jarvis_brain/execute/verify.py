"""Did the action actually happen? Confirm from the state stream, not from the call.

A successful action call means Home Assistant accepted the request, not that the light is
on. Verification watches ``state_changed`` for the entity and records the result on the
turn, which is what makes the audit log worth fitting thresholds on.

This is also the satellite's verification path. The on-device path is fire-and-acknowledge
and cannot verify anything itself, so the brain does it after the fact from the state event
and the audit event (review 3.5).
"""

from __future__ import annotations


class StateVerifier:
    async def expect(self, entity_id: str, expected: str, timeout: float = 3.0) -> bool:
        """Wait for the entity to reach the expected state. False on timeout.

        A timeout is not an error to hide. It means the action did not take, and the user
        is told so rather than being told "done".
        """
        raise NotImplementedError("build order step 2")
