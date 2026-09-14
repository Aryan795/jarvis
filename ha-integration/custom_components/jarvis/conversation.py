"""The conversation entity. One HTTP call per turn, and nothing else.

``ConversationInput`` carries ``device_id`` and ``satellite_id`` on every turn, which is
where the brain's notion of "area" comes from — it resolves the device to an area over its
own WebSocket connection. That is the context injector from the v1 diagram, restored.

``continue_conversation`` on the result is how a clarify turn works: HA reopens the
satellite's microphone without requiring the wake word again. The brain sets it whenever it
would otherwise have to guess.
"""

from __future__ import annotations

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback


class JarvisConversationEntity(conversation.ConversationEntity):
    """Forwards to the brain. Never decides anything locally."""

    _attr_has_entity_name = True
    _attr_name = "Jarvis"

    @property
    def supported_languages(self) -> list[str]:
        return ["en"]

    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        """POST the turn to the brain and speak whatever comes back.

        On timeout or connection failure, speak the failure rather than returning empty.
        The satellite has a clip for this, but a text-only turn needs words too.
        """
        raise NotImplementedError("build order step 2")


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    raise NotImplementedError("build order step 2")
