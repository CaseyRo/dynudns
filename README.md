# Home Assistant Integration: Multi-DDNS

This repository hosts the **Multi-DDNS** integration for Home Assistant. It exposes a sensor that reports the external IP address and, if configured, updates both DuckDNS and Dynu with the latest IPv4/IPv6 values.

## Installation

1. Ensure [HACS](https://hacs.xyz) is installed in your Home Assistant instance.
2. Add this repository as a custom repository in HACS.
3. Install the **Multi-DDNS** integration from HACS.
4. Restart Home Assistant.

## Usage

Configure the integration via the Home Assistant UI:

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Multi-DDNS**.
3. Fill out the form with your domains (one per line), optional Dynu and DuckDNS tokens,
   IP endpoints, wildcard toggle and update interval.
4. After setup, use the **Options** button on the integration to adjust settings later.

The integration creates a sensor `sensor.external_ip` that shows your current
external IP address and updates the configured domains on each interval.

## Certificate management

The integration registers a service `multiddns.issue_certificate` which uses
[certbot](https://certbot.eff.org/) to request or renew Let's Encrypt
certificates. By default certificates are stored in Home Assistant's `ssl`
directory, but a custom path may be supplied.

Example service call:

```yaml
service: multiddns.issue_certificate
data:
  domain: myhome.duckdns.org
  email: user@example.com
  cert_dir: /ssl   # optional
```

## Repository structure

- `custom_components/multiddns/` – Integration source code
- `hacs.json` – HACS metadata

## License

[MIT](LICENSE)
