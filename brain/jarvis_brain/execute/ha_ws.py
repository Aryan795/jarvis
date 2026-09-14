"""One long-lived WebSocket to Home Assistant. Not the REST API.

v1 drew the REST API, which means a connection per call and no state stream. The brain
needs the stream anyway: it subscribes to ``state_changed`` to verify its own actions, and
to the satellite's ``event`` entity to keep the audit log whole (review 2.4).

One connection, used for four things: pulling the exposed-entity, area and floor registries
for hassil's slot lists, calling actions, watching state, and receiving satellite events.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any


class HomeAssistantWS:
    async def connect(self) -> None:
        raise NotImplementedError("build order step 2")

    async def call_action(self, domain: str, action: str, data: dict[str, Any]) -> None:
        """Call an action. Only ever reached through a Decision from the guard chain."""
        raise NotImplementedError("build order step 2")

    async def get_exposed_entities(self) -> list[dict[str, Any]]:
        """Entities exposed to Assist, with their areas. The vocabulary and the blast radius."""
        raise NotImplementedError("build order step 2")

    async def area_for_device(self, device_id: str) -> str | None:
        """Resolve the satellite's device id to an area. This is the context injector."""
        raise NotImplementedError("build order step 2")

    async def subscribe_events(self, event_type: str) -> AsyncIterator[dict[str, Any]]:
        """Stream events. Used for ``state_changed`` and for the satellite's audit events."""
        raise NotImplementedError("build order step 2")
        yield {}  # pragma: no cover
