# Android ↔ Gateway Contract v0.1

## Stato semplice

Topic:

```text
domoticsai/v1/state/energy/solar_power_w
```

Payload:

```json
{
  "value": 2450,
  "unit": "W",
  "ts": "2026-07-13T15:00:00+02:00",
  "quality": "good"
}
```

## Stato aggregato

Topic:

```text
domoticsai/v1/state/climate/summary
```

Payload:

```json
{
  "enabled": true,
  "mode": "COOLING_ON",
  "season": "SUMMER",
  "setpointC": 23,
  "livingTemperatureC": 24.6,
  "bedroomTemperatureC": 25.1,
  "livingHumidex": 30.2,
  "bedroomHumidex": 29.8,
  "acPowerW": 710,
  "decisionReason": "SOLAR_SURPLUS",
  "ts": "2026-07-13T15:00:00+02:00"
}
```

## Comando

Topic:

```text
domoticsai/v1/cmd/climate/enabled
```

Payload:

```json
{
  "commandId": "uuid",
  "value": false,
  "source": "android",
  "ts": "ISO-8601"
}
```

## Ack

Topic:

```text
domoticsai/v1/ack/<commandId>
```

Payload:

```json
{
  "commandId": "uuid",
  "status": "accepted",
  "message": "",
  "ts": "ISO-8601"
}
```

## Stato confermato

Il Gateway pubblica lo stato aggiornato sul relativo topic retained.

## Errori standard

```text
INVALID_PAYLOAD
OUT_OF_RANGE
UNAUTHORIZED
LEGACY_TARGET_UNAVAILABLE
TIMEOUT
NOT_CONFIRMED
INTERNAL_ERROR
```
