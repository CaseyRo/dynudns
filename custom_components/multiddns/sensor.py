"""Sensor and updater for Multi-DDNS."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

import voluptuous as vol
from aiohttp import ClientError

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_SCAN_INTERVAL
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_DOMAINS,
    CONF_DUCK_TOKEN,
    CONF_DYNU_TOKEN,
    CONF_IPV4,
    CONF_IPV6,
    CONF_UPDATE_INTERVAL,
    CONF_WILDCARD,
    DEFAULT_IPV4,
    DEFAULT_IPV6,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_DOMAINS): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_DYNU_TOKEN): cv.string,
        vol.Optional(CONF_DUCK_TOKEN): cv.string,
        vol.Optional(CONF_IPV4, default=DEFAULT_IPV4): cv.string,
        vol.Optional(CONF_IPV6, default=DEFAULT_IPV6): cv.string,
        vol.Optional(CONF_WILDCARD, default=False): cv.boolean,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Multi-DDNS sensor platform."""
    scan_interval: timedelta = config[CONF_SCAN_INTERVAL]
    async_add_entities([MultiDDNSSensor(hass, config, scan_interval)], True)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Multi-DDNS sensor from a config entry."""
    config = {**entry.data, **entry.options}
    interval = timedelta(
        minutes=config.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    )
    async_add_entities([MultiDDNSSensor(hass, config, interval)], True)


class MultiDDNSSensor(SensorEntity):
    """Sensor that reports and updates external IP addresses."""

    _attr_name = "External IP"

    def __init__(self, hass, config: dict[str, Any], scan_interval: timedelta) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self.domains: list[str] = config[CONF_DOMAINS]
        self.dynu_token: str | None = config.get(CONF_DYNU_TOKEN)
        self.duck_token: str | None = config.get(CONF_DUCK_TOKEN)
        self.ipv4_endpoint: str = config[CONF_IPV4]
        self.ipv6_endpoint: str = config[CONF_IPV6]
        self.wildcard: bool = config[CONF_WILDCARD]
        self._domain_ids: dict[str, Any] = {}
        self._attr_native_value = None
        self._attr_should_poll = True
        self._attr_scan_interval = scan_interval

    async def async_update(self) -> None:
        """Fetch the latest external IP and update providers."""
        session = async_get_clientsession(self.hass)
        ipv4 = await self._get_ip(session, self.ipv4_endpoint)
        ipv6 = await self._get_ip(session, self.ipv6_endpoint)

        self._attr_native_value = ipv4 or ipv6

        for domain in self.domains:
            if domain.endswith("duckdns.org") and self.duck_token:
                params = {"domains": domain, "token": self.duck_token}
                if ipv4:
                    params["ip"] = ipv4
                if ipv6:
                    params["ipv6"] = ipv6
                try:
                    await session.get("https://www.duckdns.org/update", params=params)
                except ClientError as err:
                    _LOGGER.debug("DuckDNS update failed for %s: %s", domain, err)
                continue

            if not self.dynu_token:
                continue

            domain_id = self._domain_ids.get(domain)
            if domain_id is None:
                domain_id = await self._get_dynu_domain_id(session, domain)
                if domain_id is None:
                    continue
                self._domain_ids[domain] = domain_id

            data = {
                "name": domain,
                "ipv4Address": ipv4,
                "ipv6Address": ipv6,
                "ipv4WildcardAlias": self.wildcard,
                "ipv6WildcardAlias": self.wildcard,
            }
            try:
                await session.post(
                    f"https://api.dynu.com/v2/dns/{domain_id}",
                    headers={"API-Key": self.dynu_token},
                    json=data,
                )
            except ClientError as err:
                _LOGGER.debug("Dynu update failed for %s: %s", domain, err)

    async def _get_ip(self, session, url: str) -> str | None:
        """Retrieve IP from endpoint."""
        try:
            async with session.get(url) as resp:
                return (await resp.text()).strip()
        except ClientError as err:
            _LOGGER.debug("Failed to fetch IP from %s: %s", url, err)
            return None

    async def _get_dynu_domain_id(self, session, domain: str) -> str | None:
        """Get Dynu domain ID for a given domain."""
        try:
            async with session.get(
                "https://api.dynu.com/v2/dns", headers={"API-Key": self.dynu_token}
            ) as resp:
                data = await resp.json()
        except ClientError as err:
            _LOGGER.debug("Failed to retrieve Dynu domains: %s", err)
            return None

        for item in data.get("domains", []):
            if item.get("name") == domain:
                return item.get("id")
        _LOGGER.debug("Domain %s not found in Dynu account", domain)
        return None

