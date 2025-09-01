# Home Assistant Integration: Multi-DDNS

This repository hosts the **Multi-DDNS** integration for Home Assistant. It provides a simple sensor that shows the current external IP address of your Home Assistant instance.

## Installation

1. Ensure [HACS](https://hacs.xyz) is installed in your Home Assistant instance.
2. Add this repository as a custom repository in HACS.
3. Install the **Multi-DDNS** integration from HACS.
4. Restart Home Assistant.

## Usage

Add the following to your `configuration.yaml` to enable the sensor:

```yaml
sensor:
  - platform: multiddns
```

The sensor `sensor.external_ip` will show your current external IP address and update every five minutes.

## Repository structure

- `custom_components/multiddns/` – Integration source code
- `hacs.json` – HACS metadata

## License

[MIT](LICENSE)
