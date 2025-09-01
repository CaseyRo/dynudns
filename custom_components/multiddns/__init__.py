"""Multi-DDNS integration."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Multi-DDNS integration."""
    _LOGGER.debug("Setting up Multi-DDNS integration")
    return True
