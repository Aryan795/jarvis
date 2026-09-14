"""Config flow: the brain's URL, and a connection check before the entry is created."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import CONF_BRAIN_URL, DEFAULT_BRAIN_URL, DOMAIN


class JarvisConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {vol.Required(CONF_BRAIN_URL, default=DEFAULT_BRAIN_URL): str}
                ),
            )
        raise NotImplementedError("build order step 2")
