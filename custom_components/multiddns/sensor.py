"""Sensor platform for Multi-DDNS."""

from __future__ import annotations

from datetime import timedelta
from aiohttp import ClientError

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

SCAN_INTERVAL = timedelta(minutes=5)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Multi-DDNS sensor platform."""
    async_add_entities([ExternalIPSensor()], True)

class ExternalIPSensor(SensorEntity):
    """Sensor that reports the current external IP address."""

    _attr_name = "External IP"

    async def async_update(self) -> None:
        """Fetch the latest external IP address."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get("https://api.ipify.org") as resp:
                self._attr_native_value = await resp.text()
        except ClientError:
            self._attr_native_value = None
