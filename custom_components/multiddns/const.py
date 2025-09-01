"""Constants for Multi-DDNS integration."""

from __future__ import annotations

from datetime import timedelta

DOMAIN = "multiddns"

CONF_DOMAINS = "domains"
CONF_DYNU_TOKEN = "dynu_token"
CONF_DUCK_TOKEN = "duck_token"
CONF_IPV4 = "ipv4"
CONF_IPV6 = "ipv6"
CONF_WILDCARD = "wildcard_alias"
CONF_UPDATE_INTERVAL = "update_interval"
CONF_CERT_ISSUED = "cert_issued"

DEFAULT_IPV4 = "https://ipv4.text.wtfismyip.com"
DEFAULT_IPV6 = "https://ipv6.text.wtfismyip.com"
DEFAULT_UPDATE_INTERVAL = 5  # minutes
DEFAULT_SCAN_INTERVAL = timedelta(minutes=DEFAULT_UPDATE_INTERVAL)
