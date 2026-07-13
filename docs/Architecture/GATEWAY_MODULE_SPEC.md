# Gateway Module Specification

## 00 Core

- base topic;
- timestamp;
- correlation ID;
- validation;
- error handling;
- shared config;
- log bus.

## 01 Availability

Topic:

```text
domoticsai/v1/availability/gateway
domoticsai/v1/availability/production
```

Payload:

```json
{
  "status": "online",
  "ts": "ISO-8601",
  "version": "0.1.0"
}
```

## 02 Energy

Ingressi legacy:

```text
TeslaPowerwall/solar_instant_power
TeslaPowerwall/load_instant_power
TeslaPowerwall/SOE
```

Uscite target:

```text
domoticsai/v1/state/energy/solar_power_w
domoticsai/v1/state/energy/home_load_w
domoticsai/v1/state/energy/powerwall_soc_pct
domoticsai/v1/state/energy/summary
```

## 03 Climate

Ingressi legacy:

```text
casa/clima/stato_completo
zara/domotics/LivingHumidex
zara/domotics/BedroomHumidex
emon/emonth5/temperature_calibrated
emon/cameraMatrimoniale/temperature
emon/AC/emeter_power
```

Uscite target:

```text
domoticsai/v1/state/climate/summary
domoticsai/v1/state/climate/living_temperature_c
domoticsai/v1/state/climate/bedroom_temperature_c
domoticsai/v1/state/climate/living_humidex
domoticsai/v1/state/climate/bedroom_humidex
domoticsai/v1/state/climate/ac_power_w
```

## 04 VMC

Uscite target:

```text
domoticsai/v1/state/vmc/speed
domoticsai/v1/state/vmc/reason
domoticsai/v1/cmd/vmc/speed
```

## 05 Logs

Topic:

```text
domoticsai/v1/log/gateway
domoticsai/v1/log/mqtt
domoticsai/v1/log/command
domoticsai/v1/event/climate
```

## 06 Simulator

Profili:

- summer-day;
- summer-night;
- winter-day;
- winter-night;
- cloud-deficit;
- powerwall-low;
- sensor-stale;
- mqtt-disconnect.
