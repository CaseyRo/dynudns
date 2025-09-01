# Home Assistant Integration: Multi-DDNS

This repository hosts the **Multi-DDNS** integration for Home Assistant. It exposes a sensor that reports the external IP address and, if configured, updates both DuckDNS and Dynu with the latest IPv4/IPv6 values.

## Installation

1. Ensure [HACS](https://hacs.xyz) is installed in your Home Assistant instance.
2. Add this repository as a custom repository in HACS.
3. Install the **Multi-DDNS** integration from HACS.
4. Restart Home Assistant.

## Usage

Add the following to your `configuration.yaml` to enable the sensor and configure domain updates:

```yaml
sensor:
  - platform: multiddns
    domains:
      - myhome.duckdns.org
      - example.dynu.net
    duck_token: !secret duckdns_token     # Optional, required for DuckDNS domains
    dynu_token: !secret dynu_api_token    # Optional, required for Dynu domains
    scan_interval: 300                    # Optional, seconds between updates
```

The sensor `sensor.external_ip` will show your current external IP address and update the configured domains on each interval.

## Repository structure

- `custom_components/multiddns/` – Integration source code
- `hacs.json` – HACS metadata

## License

[MIT](LICENSE)
