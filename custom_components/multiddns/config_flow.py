"""Config flow for Multi-DDNS integration."""

from __future__ import annotations

from typing import Any
import re

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_DOMAINS,
    CONF_DYNU_TOKEN,
    CONF_DUCK_TOKEN,
    CONF_IPV4,
    CONF_IPV6,
    CONF_WILDCARD,
    CONF_UPDATE_INTERVAL,
    DEFAULT_IPV4,
    DEFAULT_IPV6,
    DEFAULT_UPDATE_INTERVAL,
)


class MultiDDNSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Multi-DDNS."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            user_input[CONF_DOMAINS] = [
                d.strip()
                for d in re.split(r"[\n,]+", user_input[CONF_DOMAINS])
                if d.strip()
            ]
            return self.async_create_entry(title="Multi-DDNS", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DOMAINS): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=True)
                ),
                vol.Optional(CONF_DYNU_TOKEN): str,
                vol.Optional(CONF_DUCK_TOKEN): str,
                vol.Optional(CONF_IPV4, default=DEFAULT_IPV4): str,
                vol.Optional(CONF_IPV6, default=DEFAULT_IPV6): str,
                vol.Optional(CONF_WILDCARD, default=False): bool,
                vol.Optional(
                    CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL
                ): int,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return MultiDDNSOptionsFlow(config_entry)


class MultiDDNSOptionsFlow(config_entries.OptionsFlowWithConfigEntry):
    """Handle options for Multi-DDNS."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            user_input[CONF_DOMAINS] = [
                d.strip()
                for d in re.split(r"[\n,]+", user_input[CONF_DOMAINS])
                if d.strip()
            ]
            return self.async_create_entry(data=user_input)

        data = {**self.config_entry.data, **self.config_entry.options}
        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_DOMAINS,
                    default=", ".join(data.get(CONF_DOMAINS, [])),
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=True)
                ),
                vol.Optional(
                    CONF_DYNU_TOKEN, default=data.get(CONF_DYNU_TOKEN, "")
                ): str,
                vol.Optional(
                    CONF_DUCK_TOKEN, default=data.get(CONF_DUCK_TOKEN, "")
                ): str,
                vol.Optional(CONF_IPV4, default=data.get(CONF_IPV4, DEFAULT_IPV4)): str,
                vol.Optional(CONF_IPV6, default=data.get(CONF_IPV6, DEFAULT_IPV6)): str,
                vol.Optional(CONF_WILDCARD, default=data.get(CONF_WILDCARD, False)): bool,
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
                ): int,
            }
        )
        return self.async_show_form(step_id="init", data_schema=data_schema)
