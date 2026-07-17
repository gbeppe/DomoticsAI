# DomoticsAI — Piano Bridge v2 read-only

- Modalità: `READ_ONLY_CANARY`
- Base topic produzione: `zara/android/domotica`
- Base topic canary: `zara/android/domotica/v2`
- Sottoscrizioni read-only: `81`
- Elementi esclusi: `63`

## Regole di sicurezza

- Nessun comando hardware.
- Nessuna sottoscrizione ai topic di comando del namespace canary.
- Pubblicazioni consentite soltanto sotto `zara/android/domotica/v2/...`.
- Stati read-only retained consentiti.
- Comandi retained vietati.
- Topic dinamici esclusi dal primo canary.

## CLIMATE

| Sorgente | Broker | Destinazione canary | Payload | Retain |
|---|---|---|---|---|
| `${APP_BASE}/env/humidexBedroom` | `n/d` | `${canaryBaseTopic}/env/humidexBedroom` | number | true |
| `${APP_BASE}/env/humidexLiving` | `n/d` | `${canaryBaseTopic}/env/humidexLiving` | number | true |
| `casa/clima/stat/vmc_max_notte` | `n/d` | `${canaryBaseTopic}/vmc/maxNightSpeed/state` | normalized_scalar | true |
| `casa/clima/stato_completo` | `192.168.1.20:1883` | `${canaryBaseTopic}/casa/clima/stato_completo` | json_object | true |
| `emon/cameraMatrimoniale/humidex` | `n/d` | `${canaryBaseTopic}/env/humidexBedroom` | number | true |
| `emon/cameraMatrimoniale/humidity` | `n/d` | `${canaryBaseTopic}/env/humBedroom` | number | true |
| `emon/cameraMatrimoniale/temperature` | `n/d` | `${canaryBaseTopic}/env/tempBedroom` | number | true |
| `emon/emonth5/humidex` | `n/d` | `${canaryBaseTopic}/env/humidexLiving` | number | true |
| `emon/emonth5/humidity` | `n/d` | `${canaryBaseTopic}/env/humLiving` | number | true |
| `emon/emonth5/temperature_calibrated` | `192.168.1.15:1883` | `${canaryBaseTopic}/env/tempLiving` | number | true |
| `zara/android/domotica/env/humidexBedroom` | `n/d` | `${canaryBaseTopic}/env/humidexBedroom` | number | true |
| `zara/android/domotica/env/humidexLiving` | `n/d` | `${canaryBaseTopic}/env/humidexLiving` | number | true |
| `zara/android/domotica/system/ac_auto/state` | `n/d` | `${canaryBaseTopic}/system/ac_auto/state` | normalized_scalar | true |
| `zara/android/domotica/thermostat/${targetRoom}/target/state` | `n/d` | `${canaryBaseTopic}/thermostat/${targetRoom}/target/state` | normalized_scalar | true |
| `zara/android/domotica/thermostat/([^/]+` | `n/d` | `${canaryBaseTopic}/thermostat/([^/]+` | unknown | true |

## ENERGY

| Sorgente | Broker | Destinazione canary | Payload | Retain |
|---|---|---|---|---|
| `${APP_BASE}/energy/battery` | `n/d` | `${canaryBaseTopic}/energy/battery` | unknown | true |
| `${APP_BASE}/energy/consumption` | `n/d` | `${canaryBaseTopic}/energy/consumption` | unknown | true |
| `${APP_BASE}/energy/grid` | `n/d` | `${canaryBaseTopic}/energy/grid` | unknown | true |
| `${APP_BASE}/energy/production` | `n/d` | `${canaryBaseTopic}/energy/production` | unknown | true |
| `${APP_BASE}/energy/surplus` | `n/d` | `${canaryBaseTopic}/energy/surplus` | unknown | true |
| `TeslaPowerwall/SOE` | `n/d` | `${canaryBaseTopic}/energy/battery` | number | true |
| `TeslaPowerwall/load_instant_power` | `n/d` | `${canaryBaseTopic}/energy/consumption` | number | true |
| `TeslaPowerwall/site_instant_power` | `n/d` | `${canaryBaseTopic}/energy/grid` | number | true |
| `TeslaPowerwall/solar_instant_power` | `n/d` | `${canaryBaseTopic}/energy/production` | number | true |
| `zara/android/domotica/energy/battery` | `n/d` | `${canaryBaseTopic}/energy/battery` | unknown | true |
| `zara/android/domotica/energy/consumption` | `n/d` | `${canaryBaseTopic}/energy/consumption` | unknown | true |
| `zara/android/domotica/energy/grid` | `n/d` | `${canaryBaseTopic}/energy/grid` | unknown | true |
| `zara/android/domotica/energy/production` | `n/d` | `${canaryBaseTopic}/energy/production` | unknown | true |
| `zara/android/domotica/energy/surplus` | `n/d` | `${canaryBaseTopic}/energy/surplus` | unknown | true |

## FIREPLACE

| Sorgente | Broker | Destinazione canary | Payload | Retain |
|---|---|---|---|---|
| `emon/focolare/powerraw` | `n/d` | `${canaryBaseTopic}/casa/stufa/stat/potenza` | number | true |
| `zara/android/domotica/casa/stufa/stat/acceso` | `n/d` | `${canaryBaseTopic}/casa/stufa/stat/acceso` | normalized_scalar | true |
| `zara/android/domotica/casa/stufa/stat/modalita` | `n/d` | `${canaryBaseTopic}/casa/stufa/stat/modalita` | normalized_scalar | true |
| `zara/android/domotica/casa/stufa/stat/potenza` | `n/d` | `${canaryBaseTopic}/casa/stufa/stat/potenza` | normalized_scalar | true |
| `zara/domotics/palazzetti/#` | `192.168.1.15:1883` | `${canaryBaseTopic}/casa/stufa/stat/#` | unknown | true |

## HISTORY

| Sorgente | Broker | Destinazione canary | Payload | Retain |
|---|---|---|---|---|
| `zara/android/domotica/history/ac/response` | `n/d` | `${canaryBaseTopic}/history/ac/response` | unknown | true |

## LIGHTS

| Sorgente | Broker | Destinazione canary | Payload | Retain |
|---|---|---|---|---|
| `zara/android/domotica/light/${targetDevice}/state` | `n/d` | `${canaryBaseTopic}/light/${targetDevice}/state` | normalized_scalar | true |
| `zara/android/domotica/light/([^/]+` | `n/d` | `${canaryBaseTopic}/light/([^/]+` | unknown | true |
| `zara/android/domotica/system/luci_eco/state` | `n/d` | `${canaryBaseTopic}/system/luci_eco/state` | normalized_scalar | true |
| `zara/android/domotica/system/luci_piscina_auto/state` | `n/d` | `${canaryBaseTopic}/system/luci_piscina_auto/state` | normalized_scalar | true |
| `zara/domotics/lights/livinglamp` | `n/d` | `${canaryBaseTopic}/light/sala/state` | unknown | true |
| `zara/domotics/lights/poolfloor` | `n/d` | `${canaryBaseTopic}/light/luciPedanaPiscina/state` | unknown | true |
| `zara/domotics/lights/poollight` | `n/d` | `${canaryBaseTopic}/light/luciPiscina/state` | unknown | true |
| `zara/domotics/lights/poolpump` | `n/d` | `${canaryBaseTopic}/light/pompaPiscina/state` | unknown | true |
| `zara/domotics/lights/poolskimmer` | `n/d` | `${canaryBaseTopic}/light/skimmerPiscina/state` | unknown | true |
| `zara/domotics/lights/readinglight` | `n/d` | `${canaryBaseTopic}/light/tavolinoLettura/state` | unknown | true |
| `zara/domotics/lights/shelflamp` | `n/d` | `${canaryBaseTopic}/light/libreria/state` | unknown | true |
| `zara/domotics/lights/tvlamp` | `n/d` | `${canaryBaseTopic}/light/televisione/state` | unknown | true |
| `zara/domotics/luciECO` | `192.168.1.20:1883` | `${canaryBaseTopic}/system/luci_eco/state` | unknown | true |
| `zara/domotics/luciPiscinaAuto` | `192.168.1.20:1883` | `${canaryBaseTopic}/system/luci_piscina_auto/state` | unknown | true |

## SYSTEM

| Sorgente | Broker | Destinazione canary | Payload | Retain |
|---|---|---|---|---|
| `zara/android/domotica/system/enabled/state` | `n/d` | `${canaryBaseTopic}/system/enabled/state` | normalized_scalar | true |
| `zara/android/domotica/system/holiday/state` | `n/d` | `${canaryBaseTopic}/system/holiday/state` | normalized_scalar | true |
| `zara/android/domotica/system/sensore_portico/state` | `n/d` | `${canaryBaseTopic}/system/sensore_portico/state` | number | true |
| `zara/android/domotica/system/time_range/state` | `n/d` | `${canaryBaseTopic}/system/time_range/state` | normalized_scalar | true |
| `zara/domotics/porch_sensor` | `n/d` | `${canaryBaseTopic}/system/sensore_portico/state` | number | true |
| `zara/domotics/time_range` | `n/d` | `${canaryBaseTopic}/system/time_range/state` | unknown | true |

## UNCLASSIFIED

| Sorgente | Broker | Destinazione canary | Payload | Retain |
|---|---|---|---|---|
| `${APP_BASE}/acsPufferTemp` | `n/d` | `${canaryBaseTopic}/acsPufferTemp` | unknown | true |
| `${APP_BASE}/env/humBedroom` | `n/d` | `${canaryBaseTopic}/env/humBedroom` | unknown | true |
| `${APP_BASE}/env/humLiving` | `n/d` | `${canaryBaseTopic}/env/humLiving` | unknown | true |
| `${APP_BASE}/env/humOutdoor` | `n/d` | `${canaryBaseTopic}/env/humOutdoor` | unknown | true |
| `${APP_BASE}/env/tempBedroom` | `n/d` | `${canaryBaseTopic}/env/tempBedroom` | unknown | true |
| `${APP_BASE}/env/tempLiving` | `n/d` | `${canaryBaseTopic}/env/tempLiving` | unknown | true |
| `${APP_BASE}/env/tempOutdoor` | `n/d` | `${canaryBaseTopic}/env/tempOutdoor` | unknown | true |
| `${APP_BASE}/pufferAltoTemp` | `n/d` | `${canaryBaseTopic}/pufferAltoTemp` | unknown | true |
| `${APP_BASE}/pufferBassoTemp` | `n/d` | `${canaryBaseTopic}/pufferBassoTemp` | unknown | true |
| `emon/resolDL2/sensor2` | `n/d` | `${canaryBaseTopic}/pufferBassoTemp` | number | true |
| `emon/resolDL2/sensor3` | `n/d` | `${canaryBaseTopic}/pufferAltoTemp` | number | true |
| `emon/shellyACS/tempACS` | `n/d` | `${canaryBaseTopic}/acsPufferTemp` | unknown | true |
| `zara/android/domotica/acsPufferTemp` | `n/d` | `${canaryBaseTopic}/acsPufferTemp` | unknown | true |
| `zara/android/domotica/env/humBedroom` | `n/d` | `${canaryBaseTopic}/env/humBedroom` | unknown | true |
| `zara/android/domotica/env/humLiving` | `n/d` | `${canaryBaseTopic}/env/humLiving` | unknown | true |
| `zara/android/domotica/env/humOutdoor` | `n/d` | `${canaryBaseTopic}/env/humOutdoor` | unknown | true |
| `zara/android/domotica/env/tempBedroom` | `n/d` | `${canaryBaseTopic}/env/tempBedroom` | unknown | true |
| `zara/android/domotica/env/tempLiving` | `n/d` | `${canaryBaseTopic}/env/tempLiving` | unknown | true |
| `zara/android/domotica/env/tempOutdoor` | `n/d` | `${canaryBaseTopic}/env/tempOutdoor` | unknown | true |
| `zara/android/domotica/pufferAltoTemp` | `n/d` | `${canaryBaseTopic}/pufferAltoTemp` | unknown | true |
| `zara/android/domotica/pufferBassoTemp` | `n/d` | `${canaryBaseTopic}/pufferBassoTemp` | unknown | true |
| `zara/domotics/modalitavacanza` | `192.168.1.20:1883` | `${canaryBaseTopic}/system/holiday/state` | unknown | true |

## VMC

| Sorgente | Broker | Destinazione canary | Payload | Retain |
|---|---|---|---|---|
| `alexa/vmc` | `n/d` | `${canaryBaseTopic}/vmc/speed/state` | unknown | true |
| `zara/android/domotica/vmc/([^/]+` | `n/d` | `${canaryBaseTopic}/vmc/([^/]+` | unknown | true |
| `zara/android/domotica/vmc/maxNightSpeed/state` | `n/d` | `${canaryBaseTopic}/vmc/maxNightSpeed/state` | normalized_scalar | true |
| `zara/android/domotica/vmc/speed/state` | `n/d` | `${canaryBaseTopic}/vmc/speed/state` | normalized_scalar | true |

## Esclusioni

- `CURRENT_APP_NAMESPACE`: `9`
- `DISTINCT_SEMANTICS`: `1`
- `DYNAMIC_TOPIC`: `6`
- `KEEP_AS_COMMAND`: `1`
- `LEGACY_MAP`: `1`
- `LOCAL_SERVICE`: `1`
- `MANUAL_REVIEW`: `21`
- `MIGRATE_TO_JSON`: `1`
- `OBSOLETE`: `4`
- `PHYSICAL_TOPIC`: `15`
- `REGEX_ROUTE`: `3`

## Criterio di promozione

Il bridge può passare da `READ_ONLY_CANARY` a `READ_ONLY_PRIMARY` soltanto dopo:

1. almeno 24 ore senza loop MQTT;
2. nessuna pubblicazione fuori dal namespace canary;
3. confronto positivo dei valori con il bridge storico;
4. assenza di errori di payload;
5. conferma manuale per ogni dominio.
