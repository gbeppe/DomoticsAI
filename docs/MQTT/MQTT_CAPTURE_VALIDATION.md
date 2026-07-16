# DomoticsAI — MQTT Capture Validation

Generato automaticamente: `2026-07-16T01:24:10.649156+00:00`

- Capture: `/home/giuseppe/AndroidStudioProjects/DomoticsAI/.captures/mqtt-production/android-namespace-20260716-025421.log`
- Contratto: `/home/giuseppe/AndroidStudioProjects/DomoticsAI/config/mqtt/application-contract-v1.json`
- Base topic: `zara/android/domotica`

## Riepilogo

- Messaggi totali: `195`
- Messaggi coperti dal contratto: `184`
- Topic unici coperti: `43`
- Topic unici non coperti: `11`
- Topic fuori namespace: `0`
- Topic ambigui: `1`
- Topic con payload incompatibili: `0`

## Topic coperti

| Topic relativo | Pattern | Dominio | Entità | Messaggi | Payload osservati |
|---|---|---|---|---:|---|
| `ac_auto/set` | `ac_auto/set` | `climate_automation` | `legacy_ac_auto_parameter` | 1 | boolean_or_number: 1 |
| `acsPufferTemp` | `acsPufferTemp` | `thermal` | `dhw_buffer_temperature` | 8 | number: 8 |
| `casa/clima/stato_completo` | `casa/clima/stato_completo` | `climate` | `complete_climate_snapshot` | 32 | json_object: 32 |
| `casa/stufa/stat/acceso` | `casa/stufa/stat/acceso` | `fireplace` | `fireplace_powered` | 1 | boolean: 1 |
| `casa/stufa/stat/modalita` | `casa/stufa/stat/modalita` | `fireplace` | `fireplace_mode` | 1 | string: 1 |
| `casa/stufa/stat/potenza` | `casa/stufa/stat/potenza` | `fireplace` | `fireplace_power_level` | 1 | number: 1 |
| `controlli/minOffCompressore` | `controlli/{name}` | `controls` | `{name}` | 1 | number: 1 |
| `controlli/minOnCompressore` | `controlli/{name}` | `controls` | `{name}` | 1 | number: 1 |
| `controlli/velocitaMaxVmcNotte` | `controlli/{name}` | `controls` | `{name}` | 1 | number: 1 |
| `energy/battery` | `energy/battery` | `energy` | `battery_soc` | 7 | number: 7 |
| `energy/consumption` | `energy/consumption` | `energy` | `house_consumption` | 2 | number: 2 |
| `energy/grid` | `energy/grid` | `energy` | `grid_power` | 7 | boolean_or_number: 7 |
| `energy/production` | `energy/production` | `energy` | `solar_production` | 1 | number: 1 |
| `energy/surplus` | `energy/surplus` | `energy` | `energy_surplus` | 32 | number: 32 |
| `env/humBedroom` | `env/humBedroom` | `environment` | `bedroom_humidity` | 1 | number: 1 |
| `env/humLiving` | `env/humLiving` | `environment` | `living_humidity` | 3 | number: 3 |
| `env/humOutdoor` | `env/humOutdoor` | `environment` | `outdoor_humidity` | 1 | number: 1 |
| `env/humidexBedroom` | `env/humidexBedroom` | `environment` | `bedroom_humidex` | 5 | number: 5 |
| `env/humidexLiving` | `env/humidexLiving` | `environment` | `living_humidex` | 5 | number: 5 |
| `env/tempBedroom` | `env/tempBedroom` | `environment` | `bedroom_temperature` | 1 | number: 1 |
| `env/tempLiving` | `env/tempLiving` | `environment` | `living_temperature` | 3 | number: 3 |
| `env/tempOutdoor` | `env/tempOutdoor` | `environment` | `outdoor_temperature` | 1 | number: 1 |
| `light/ingressoServizio/state` | `light/{device}/state` | `lights` | `{device}` | 5 | boolean: 5 |
| `light/lavanderia/state` | `light/{device}/state` | `lights` | `{device}` | 5 | boolean: 5 |
| `light/libreria/state` | `light/{device}/state` | `lights` | `{device}` | 1 | boolean: 1 |
| `light/luciPedanaPiscina/state` | `light/{device}/state` | `lights` | `{device}` | 1 | boolean: 1 |
| `light/luciPiscina/state` | `light/{device}/state` | `lights` | `{device}` | 1 | boolean: 1 |
| `light/pompaPiscina/state` | `light/{device}/state` | `lights` | `{device}` | 1 | boolean: 1 |
| `light/portico/state` | `light/{device}/state` | `lights` | `{device}` | 5 | boolean: 5 |
| `light/sala/state` | `light/{device}/state` | `lights` | `{device}` | 1 | boolean: 1 |
| `light/skimmerPiscina/state` | `light/{device}/state` | `lights` | `{device}` | 1 | boolean: 1 |
| `light/tavolinoLettura/state` | `light/{device}/state` | `lights` | `{device}` | 1 | boolean: 1 |
| `light/televisione/state` | `light/{device}/state` | `lights` | `{device}` | 1 | boolean: 1 |
| `pufferAltoTemp` | `pufferAltoTemp` | `thermal` | `buffer_upper_temperature` | 3 | number: 3 |
| `pufferBassoTemp` | `pufferBassoTemp` | `thermal` | `buffer_lower_temperature` | 3 | number: 3 |
| `system/ac_auto/state` | `system/ac_auto/state` | `system` | `system_ac_auto_parameter` | 1 | boolean_or_number: 1 |
| `system/eco_lights/state` | `system/{name}/state` | `system` | `{name}` | 1 | boolean_or_number: 1 |
| `system/holiday/state` | `system/{name}/state` | `system` | `{name}` | 1 | boolean_or_number: 1 |
| `system/luci_eco/state` | `system/{name}/state` | `system` | `{name}` | 1 | boolean_or_number: 1 |
| `system/luci_piscina_auto/state` | `system/{name}/state` | `system` | `{name}` | 1 | boolean_or_number: 1 |
| `system/sensore_portico/state` | `system/{name}/state` | `system` | `{name}` | 1 | boolean_or_number: 1 |
| `thermostat/living/target/state` | `thermostat/living/target/state` | `climate` | `living_target_temperature` | 32 | number: 32 |
| `vmc/speed/state` | `vmc/speed/state` | `ventilation` | `vmc_speed` | 1 | boolean_or_number: 1 |

## Topic non coperti

- `eco_lights/set` — `1` messaggi
- `eco_lights/state` — `1` messaggi
- `holiday/set` — `1` messaggi
- `holiday/state` — `1` messaggi
- `maxNightSpeed/set` — `1` messaggi
- `pool_lights_auto/set` — `1` messaggi
- `porch_sensor/set` — `1` messaggi
- `system/luci_piscina_auto/set` — `1` messaggi
- `system/sensore_portico/set` — `1` messaggi
- `system/set` — `1` messaggi
- `vmc/maxNightSpeed/set` — `1` messaggi

## Pattern del contratto non osservati

- Tutti i pattern di lettura sono stati osservati.

## Payload incompatibili

- Nessuna incompatibilità rilevata.

## Topic ambigui

- `system/ac_auto/state` — `1` messaggi

## Topic fuori namespace

- Nessun topic fuori dal base topic.

## Interpretazione

- Un topic coperto può essere usato nelle successive fasi read-only.
- Un topic non coperto deve essere analizzato prima di essere importato.
- Un pattern non osservato non è necessariamente errato: può trattarsi di un comando o di uno stato raro.
- Nessun risultato di questo report abilita automaticamente la scrittura.
