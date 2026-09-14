"""Jarvis: a conversation agent that forwards every turn to the brain on the i5.

This component deliberately contains no logic. Matching, guarding, executing and
remembering all happen in the brain. If a decision is being made here, it is in the wrong
place — the Pi is a 2 GB box already running 79 automations, and nothing heavy may live on
it.
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: list[Platform] = [Platform.CONVERSATION]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    raise NotImplementedError("build order step 2")


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
