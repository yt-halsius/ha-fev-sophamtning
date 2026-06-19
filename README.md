# ha-fev-sophamtning

Home Assistant integration for waste collection schedules from Falun Energi & Vatten (FEV).

This solution retrieves collection dates from the public FEV waste collection service and exposes them as Home Assistant sensors.

## Features

* Matavfall
* Restavfall
* Plastförpackningar
* Pappersförpackningar

## Installation

### 1. Copy Python script

Place the script in:

```text
/config/scripts/fev_sophamtning.py
```

### 2. Add command_line sensor

```yaml
command_line:
  - sensor:
      name: "FEV Sophämtning"
      command: "python3 /config/scripts/fev_sophamtning.py"
      scan_interval: 21600
      value_template: "{{ value_json.updated }}"
      json_attributes:
        - matavfall
        - plast
        - restavfall
        - papper
```

### 3. Create template sensors

Create:

```text
/config/templates/sophamtning.yaml
```

```yaml
- sensor:
    - name: "Nästa matavfall"
      device_class: date
      state: >
        {{ state_attr('sensor.fev_sophamtning', 'matavfall') }}

    - name: "Nästa plast"
      device_class: date
      state: >
        {{ state_attr('sensor.fev_sophamtning', 'plast') }}

    - name: "Nästa restavfall"
      device_class: date
      state: >
        {{ state_attr('sensor.fev_sophamtning', 'restavfall') }}

    - name: "Nästa papper"
      device_class: date
      state: >
        {{ state_attr('sensor.fev_sophamtning', 'papper') }}
```

### 4. Include templates

```yaml
template: !include_dir_merge_list templates
```

### 5. Restart Home Assistant

Verify that:

```text
sensor.nasta_matavfall
sensor.nasta_plast
sensor.nasta_restavfall
sensor.nasta_papper
```

are created.

## Example Dashboard

```yaml
type: entities
title: Sophämtning
entities:
  - entity: sensor.nasta_matavfall
  - entity: sensor.nasta_plast
  - entity: sensor.nasta_restavfall
  - entity: sensor.nasta_papper
```

## Notes

The FEV website stores collection dates in UTC timestamps:

```text
2026-06-09T22:00:00.000Z
```

The integration converts these values to local Swedish dates to avoid one-day offset errors.

## Future Improvements

* Native Home Assistant integration
* Config flow
* Multiple addresses
* HACS support
* Calendar entities
* Waste collection reminders

## Disclaimer

This project depends on the public FEV website structure. Changes to the website may require updates to the scraper.
