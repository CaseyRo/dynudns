"""Multi-DDNS integration."""

from __future__ import annotations

import logging

import asyncio
from pathlib import Path

from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Multi-DDNS integration."""
    _LOGGER.debug("Setting up Multi-DDNS integration")

    async def issue_certificate(call: ServiceCall) -> None:
        """Generate or renew a certificate using certbot."""
        domains = call.data.get("domain")
        if not domains:
            _LOGGER.error("No domain provided for certificate issuance")
            return
        if isinstance(domains, str):
            domains = [domains]
        email = call.data.get("email")
        cert_dir = Path(call.data.get("cert_dir") or hass.config.path("ssl"))
        cert_dir.mkdir(parents=True, exist_ok=True)

        for domain in domains:
            cmd = [
                "certbot",
                "certonly",
                "--standalone",
                "--non-interactive",
                "--agree-tos",
                f"--email={email}",
                f"-d={domain}",
                f"--config-dir={cert_dir}",
                f"--work-dir={cert_dir}",
                f"--logs-dir={cert_dir}",
            ]
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
            except FileNotFoundError:
                _LOGGER.error("certbot not found. Install certbot to issue certificates")
                return

            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                _LOGGER.error("certbot failed for %s: %s", domain, stderr.decode())
            else:
                _LOGGER.debug(
                    "Certificate generated for %s in %s", domain, cert_dir
                )

    hass.services.async_register(
        "multiddns", "issue_certificate", issue_certificate
    )
    return True
