# ha-fev-sophamtning

Home Assistant integration for waste collection schedules from Falun Energi & Vatten (FEV).

This project retrieves waste collection dates from the public FEV waste collection service and exposes them as Home Assistant sensors that can be used in dashboards, automations and notifications.

## Features

* Matavfall
* Plastförpackningar
* Restavfall
* Pappersförpackningar

The integration creates one sensor for each waste fraction and automatically converts the dates to local Swedish dates.

---

# How It Works

The solution consists of three parts:

1. A Python script retrieves waste collection dates from the public FEV website.
2. A Home Assistant `command_line` sensor executes the script and stores the returned data.
3. Home Assistant template sensors expose each waste fraction as a separate entity.

The result is four Home Assistant sensors:

```text
sensor.nasta_matavfall
sensor.nasta_plast
sensor.nasta_restavfall
sensor.nasta_papper
```

These sensors can be displayed in dashboards, used in automations or included in notifications.

---

# Prerequisites

Before installing this project you should have:

* Home Assistant installed and running
* Access to edit Home Assistant configuration files
* Access to restart Home Assistant

The instructions have been tested on Home Assistant OS but should also work on other installation methods.

---
## Address Configuration

The FEV service identifies addresses using URL encoded address strings.

Swedish characters must be URL encoded:

| Character | URL Encoded |
|------------|------------|
| å | %C3%A5 |
| ä | %C3%A4 |
| ö | %C3%B6 |
| space | %20 |

Example:

```text
Yttertänger 83
```

becomes:

```text
Yttert%C3%A4nger%2083
```

> [!IMPORTANT]
> FEV expects a space between the street name and house number.
>
> Correct:
>
> ```text
> Yttert%C3%A4nger%2083
> ```
>
> Incorrect:
>
> ```text
> Yttert%C3%A4nger83
> ```
>
> ```text
> Yttertänger83
> ```
>
> ```text
> Yttertänger+83
> ```
>

If all waste fractions return empty values, verify that the configured address matches the URL format expected by FEV.

---
# Installation

## 1. Copy the Python Script

Create the directory:

```text
/config/scripts
```

if it does not already exist.

Copy:

```text
fev_sophamtning.py
```

to:

```text
/config/scripts/fev_sophamtning.py
```

Your Home Assistant configuration should now look similar to:

```text
/config
├── configuration.yaml
├── scripts
│   └── fev_sophamtning.py
└── templates
```

---

## 2. Add the Command Line Sensor

Open:

```text
/configuration.yaml
```

and add:

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

### What does this do?

Every 6 hours (`21600` seconds) Home Assistant executes the Python script.

The script returns JSON data similar to:

```json
{
  "updated": "2026-05-25T21:35:37",
  "matavfall": "2026-05-27",
  "plast": "2026-05-27",
  "restavfall": "2026-06-10",
  "papper": "2026-06-24"
}
```

These values are stored as attributes on the sensor:

```text
sensor.fev_sophamtning
```

---

## 3. Create Template Sensors

Create:

```text
/config/templates/sophamtning.yaml
```

with the following content:

```yaml
- sensor:
    - name: "Nästa matavfall"
      unique_id: nasta_matavfall
      device_class: date
      state: >
        {{ state_attr('sensor.fev_sophamtning', 'matavfall') }}

    - name: "Nästa plast"
      unique_id: nasta_plast
      device_class: date
      state: >
        {{ state_attr('sensor.fev_sophamtning', 'plast') }}

    - name: "Nästa restavfall"
      unique_id: nasta_restavfall
      device_class: date
      state: >
        {{ state_attr('sensor.fev_sophamtning', 'restavfall') }}

    - name: "Nästa papper"
      unique_id: nasta_papper
      device_class: date
      state: >
        {{ state_attr('sensor.fev_sophamtning', 'papper') }}
```

### What does this do?

The command line sensor stores all waste fractions as attributes.

Template sensors expose each fraction as a separate Home Assistant entity, making them easier to use in dashboards and automations.

---

## 4. Include the Templates

Open:

```text
configuration.yaml
```

and ensure the following exists:

```yaml
template: !include_dir_merge_list templates
```

If you already use template includes, adjust accordingly.

---

## 5. Restart Home Assistant

After saving all files:

1. Go to **Settings**
2. Select **System**
3. Click **Restart**
4. Wait for Home Assistant to fully start

---

## 6. Verify Installation

Go to:

```text
Settings → Devices & Services → Entities
```

and verify that the following entities exist:

```text
sensor.nasta_matavfall
sensor.nasta_plast
sensor.nasta_restavfall
sensor.nasta_papper
```

---

# Example Dashboard

A simple Entities card:

```yaml
type: entities
title: Sophämtning
entities:
  - entity: sensor.nasta_matavfall
    name: Matavfall

  - entity: sensor.nasta_plast
    name: Plastförpackningar

  - entity: sensor.nasta_restavfall
    name: Restavfall

  - entity: sensor.nasta_papper
    name: Pappersförpackningar
```

---

# Troubleshooting

## Sensor shows "unknown"

Verify:

* The Python script exists in the correct location.
* The command path is correct.
* Home Assistant has been restarted.

## Attributes are empty

Verify:

* The FEV website is reachable.
* The script returns valid JSON.
* The configured address is correct.

## Dates are one day off

FEV returns dates as UTC timestamps.

This integration converts the timestamps to Swedish local dates before exposing them as Home Assistant sensors.

Make sure you are using the latest version of the script.

---

# Notes

The FEV website stores collection dates as UTC timestamps:

```text
2026-06-09T22:00:00.000Z
```

Without timezone conversion this would appear as:

```text
2026-06-09
```

instead of:

```text
2026-06-10
```

The integration automatically performs this conversion.

---

# Future Improvements

Potential future enhancements include:

* Native Home Assistant integration
* Config Flow
* Multiple addresses
* HACS support
* Calendar entities
* Collection reminders
* Custom waste collection icons

---

# Disclaimer

This project depends on the public FEV website structure.

Changes made by Falun Energi & Vatten to their website may require updates to the scraper.

This project is not affiliated with or endorsed by Falun Energi & Vatten.
