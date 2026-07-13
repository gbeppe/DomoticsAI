# MQTT Gateway Namespace — Draft v0.1

## Principio

L'app Android non deve dipendere direttamente dai topic storici dell'impianto.
Il Gateway traduce i topic di produzione in un namespace stabile e versionato.

## Base topic proposto

```text
domoticsai/v1
```

## Convenzioni

```text
domoticsai/v1/state/<domain>/<entity>
domoticsai/v1/cmd/<domain>/<entity>
domoticsai/v1/config/<domain>/<parameter>/set
domoticsai/v1/config/<domain>/<parameter>/state
domoticsai/v1/event/<domain>
domoticsai/v1/availability/<component>
domoticsai/v1/log/<component>
```

## Esempi

```text
domoticsai/v1/state/energy/solar_power_w
domoticsai/v1/state/energy/home_load_w
domoticsai/v1/state/energy/powerwall_soc_pct

domoticsai/v1/state/climate/living_temperature_c
domoticsai/v1/state/climate/living_humidex
domoticsai/v1/state/vmc/fan_speed

domoticsai/v1/config/climate/min_run_minutes/set
domoticsai/v1/config/climate/min_run_minutes/state

domoticsai/v1/cmd/climate/enable
domoticsai/v1/cmd/vmc/fan_speed

domoticsai/v1/event/climate
domoticsai/v1/availability/gateway
```

## Payload

Per valori semplici:

```json
23.6
```

Per eventi e stati aggregati:

```json
{
  "ts": "2026-07-13T15:30:00+02:00",
  "source": "node-red-production",
  "value": 23.6,
  "unit": "°C",
  "quality": "good"
}
```

## Regole

- QoS 1 per comandi, configurazioni ed eventi.
- Retain `true` per stato corrente e configurazioni.
- Retain `false` per eventi e log.
- Ogni comando deve produrre un topic di stato o acknowledgment.
- Le credenziali non devono comparire nei payload.
- I topic originali restano invariati nel sistema di produzione.
