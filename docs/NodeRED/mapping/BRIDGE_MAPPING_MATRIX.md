# DomoticsAI — Matrice di mapping del bridge v2

- Flow sorgente: `docs/NodeRED/source/android-app-bridge-current.json`
- Contratto: `config/mqtt/application-contract-v1.json`
- Righe di mapping: `144`

## Mapping

| Dominio | Ruolo | Topic corrente | Topic DomoticsAI proposto | Migrazione | Nel contratto | Occorrenze |
|---|---|---|---|---|---|---|
| climate | COMMAND | casa/clima/cmnd/AI_climate_enabling | ${baseTopic}/system/set | MIGRATE_TO_JSON | yes | 3 |
| climate | COMMAND | casa/clima/cmnd/vmc_max_notte | ${baseTopic}/vmc/maxNightSpeed/set | KEEP_AS_COMMAND | yes | 1 |
| climate | COMMAND | zara/android/domotica/system/ac_auto/set | ${baseTopic}/system/ac_auto/set | CURRENT_APP_NAMESPACE | no | 1 |
| climate | READ_ONLY | ${APP_BASE}/env/humidexBedroom | ${baseTopic}/env/humidexBedroom | CURRENT_APP_NAMESPACE | yes | 1 |
| climate | READ_ONLY | ${APP_BASE}/env/humidexLiving | ${baseTopic}/env/humidexLiving | CURRENT_APP_NAMESPACE | yes | 1 |
| climate | READ_ONLY | /thermostat/ | — | MANUAL_REVIEW | no | 1 |
| climate | READ_ONLY | ^${baseTopic}/thermostat/([^/]+)/target/set$ | — | REGEX_ROUTE | no | 1 |
| climate | READ_ONLY | emon/cameraMatrimoniale/humidex | ${baseTopic}/env/humidexBedroom | LEGACY_MAP | yes | 2 |
| climate | READ_ONLY | emon/cameraMatrimoniale/humidity | ${baseTopic}/env/humBedroom | LEGACY_MAP | yes | 1 |
| climate | READ_ONLY | emon/cameraMatrimoniale/temperature | ${baseTopic}/env/tempBedroom | LEGACY_MAP | yes | 1 |
| climate | READ_ONLY | emon/emonth5/humidex | ${baseTopic}/env/humidexLiving | LEGACY_MAP | yes | 2 |
| climate | READ_ONLY | emon/emonth5/humidity | ${baseTopic}/env/humLiving | LEGACY_MAP | yes | 2 |
| climate | READ_ONLY | emon/emonth5/temperature_calibrated | ${baseTopic}/env/tempLiving | LEGACY_MAP | yes | 2 |
| climate | READ_ONLY | zara/android/domotica/env/humidexBedroom | ${baseTopic}/env/humidexBedroom | CURRENT_APP_NAMESPACE | yes | 1 |
| climate | READ_ONLY | zara/android/domotica/env/humidexLiving | ${baseTopic}/env/humidexLiving | CURRENT_APP_NAMESPACE | yes | 1 |
| climate | READ_ONLY | zara/android/domotica/thermostat/([^/]+ | ${baseTopic}/thermostat/([^/]+ | CURRENT_APP_NAMESPACE | no | 1 |
| climate | READ_ONLY | zara/domotics/ACAuto | ${baseTopic}/system/ac_auto/state | DISTINCT_SEMANTICS | yes | 3 |
| climate | STATE | casa/clima/stat/vmc_max_notte | ${baseTopic}/vmc/maxNightSpeed/state | KEEP_AS_STATE | no | 2 |
| climate | STATE | casa/clima/stato_completo | ${baseTopic}/casa/clima/stato_completo | READ_ONLY_PRIMARY | yes | 4 |
| climate | STATE | zara/android/domotica/system/ac_auto/state | ${baseTopic}/system/ac_auto/state | CURRENT_APP_NAMESPACE | yes | 1 |
| climate | STATE | zara/android/domotica/thermostat/${targetRoom}/target/state | ${baseTopic}/thermostat/${targetRoom}/target/state | CURRENT_APP_NAMESPACE | no | 1 |
| energy | READ_ONLY | ${APP_BASE}/energy/battery | ${baseTopic}/energy/battery | CURRENT_APP_NAMESPACE | yes | 1 |
| energy | READ_ONLY | ${APP_BASE}/energy/consumption | ${baseTopic}/energy/consumption | CURRENT_APP_NAMESPACE | yes | 1 |
| energy | READ_ONLY | ${APP_BASE}/energy/grid | ${baseTopic}/energy/grid | CURRENT_APP_NAMESPACE | yes | 1 |
| energy | READ_ONLY | ${APP_BASE}/energy/production | ${baseTopic}/energy/production | CURRENT_APP_NAMESPACE | yes | 1 |
| energy | READ_ONLY | ${APP_BASE}/energy/surplus | ${baseTopic}/energy/surplus | CURRENT_APP_NAMESPACE | yes | 1 |
| energy | READ_ONLY | TeslaPowerwall/SOE | ${baseTopic}/energy/battery | LEGACY_MAP | yes | 2 |
| energy | READ_ONLY | TeslaPowerwall/load_instant_power | ${baseTopic}/energy/consumption | LEGACY_MAP | yes | 2 |
| energy | READ_ONLY | TeslaPowerwall/site_instant_power | ${baseTopic}/energy/grid | LEGACY_MAP | yes | 2 |
| energy | READ_ONLY | TeslaPowerwall/solar_instant_power | ${baseTopic}/energy/production | LEGACY_MAP | yes | 2 |
| energy | READ_ONLY | zara/android/domotica/energy/battery | ${baseTopic}/energy/battery | CURRENT_APP_NAMESPACE | yes | 1 |
| energy | READ_ONLY | zara/android/domotica/energy/consumption | ${baseTopic}/energy/consumption | CURRENT_APP_NAMESPACE | yes | 1 |
| energy | READ_ONLY | zara/android/domotica/energy/grid | ${baseTopic}/energy/grid | CURRENT_APP_NAMESPACE | yes | 1 |
| energy | READ_ONLY | zara/android/domotica/energy/production | ${baseTopic}/energy/production | CURRENT_APP_NAMESPACE | yes | 1 |
| energy | READ_ONLY | zara/android/domotica/energy/surplus | ${baseTopic}/energy/surplus | CURRENT_APP_NAMESPACE | yes | 1 |
| fireplace | COMMAND | /command | — | MANUAL_REVIEW | no | 1 |
| fireplace | COMMAND | alexa/caminetto/command | — | MANUAL_REVIEW | no | 1 |
| fireplace | READ_ONLY | / | — | DYNAMIC_TOPIC | no | 1 |
| fireplace | READ_ONLY | /esp8266/palazzetti | — | MANUAL_REVIEW | no | 1 |
| fireplace | READ_ONLY | /getstatus | — | MANUAL_REVIEW | no | 1 |
| fireplace | READ_ONLY | /hello | — | MANUAL_REVIEW | no | 1 |
| fireplace | READ_ONLY | /log/message | — | MANUAL_REVIEW | no | 1 |
| fireplace | READ_ONLY | /power | — | MANUAL_REVIEW | no | 1 |
| fireplace | READ_ONLY | alexa/caminetto | — | MANUAL_REVIEW | no | 2 |
| fireplace | READ_ONLY | alexa/caminetto/power | — | MANUAL_REVIEW | no | 1 |
| fireplace | READ_ONLY | emon/focolare/powerraw | ${baseTopic}/casa/stufa/stat/potenza | LEGACY_MAP | yes | 2 |
| fireplace | READ_ONLY | zara/android/domotica | — | DYNAMIC_TOPIC | no | 1 |
| fireplace | READ_ONLY | zara/domotics/palazzetti/ | — | MANUAL_REVIEW | no | 1 |
| fireplace | READ_ONLY | zara/domotics/palazzetti/# | ${baseTopic}/casa/stufa/stat/# | LEGACY_MAP | no | 1 |
| fireplace | READ_ONLY | zara/domotics/palazzetti/set/modalita | ${baseTopic}/casa/stufa/stat/modalita | LEGACY_MAP | yes | 1 |
| fireplace | STATE | zara/android/domotica/casa/stufa/stat/acceso | ${baseTopic}/casa/stufa/stat/acceso | CURRENT_APP_NAMESPACE | yes | 1 |
| fireplace | STATE | zara/android/domotica/casa/stufa/stat/modalita | ${baseTopic}/casa/stufa/stat/modalita | CURRENT_APP_NAMESPACE | yes | 1 |
| fireplace | STATE | zara/android/domotica/casa/stufa/stat/potenza | ${baseTopic}/casa/stufa/stat/potenza | CURRENT_APP_NAMESPACE | yes | 1 |
| history | READ_ONLY | /history/ac/request | — | LOCAL_SERVICE | no | 1 |
| history | READ_ONLY | zara/android/domotica/history/ac/response | ${baseTopic}/history/ac/response | CURRENT_APP_NAMESPACE | no | 1 |
| lights | COMMAND | /scene/set | — | MANUAL_REVIEW | no | 1 |
| lights | COMMAND | /set | — | MANUAL_REVIEW | no | 1 |
| lights | COMMAND | shellies/shelly1-esterno/relay/0/command | — | OBSOLETE | no | 1 |
| lights | COMMAND | zara/android/domotica/scene/set | ${baseTopic}/scene/set | CURRENT_APP_NAMESPACE | no | 1 |
| lights | COMMAND | zara/android/domotica/system/luci_eco/set | ${baseTopic}/system/luci_eco/set | CURRENT_APP_NAMESPACE | no | 1 |
| lights | COMMAND | zara/android/domotica/system/luci_piscina_auto/set | ${baseTopic}/system/luci_piscina_auto/set | CURRENT_APP_NAMESPACE | yes | 1 |
| lights | COMMAND | zigbee2mqtt/Luce_Cucina/set | — | OBSOLETE | no | 1 |
| lights | READ_ONLY | /light/ | — | MANUAL_REVIEW | no | 2 |
| lights | READ_ONLY | /scene/ | — | MANUAL_REVIEW | no | 1 |
| lights | READ_ONLY | ^${baseTopic}/light/([^/]+)/set$ | — | REGEX_ROUTE | no | 1 |
| lights | READ_ONLY | shellies/shelly1-771284/relay/0 | — | PHYSICAL_TOPIC | no | 1 |
| lights | READ_ONLY | shellies/shelly1-B8C284/relay/0 | — | PHYSICAL_TOPIC | no | 1 |
| lights | READ_ONLY | shellies/shelly1-B92AF0/relay/0 | — | PHYSICAL_TOPIC | no | 1 |
| lights | READ_ONLY | shellies/shelly1-esterno | — | OBSOLETE | no | 1 |
| lights | READ_ONLY | zara/android/domotica | — | DYNAMIC_TOPIC | no | 2 |
| lights | READ_ONLY | zara/android/domotica/light/([^/]+ | ${baseTopic}/light/([^/]+ | CURRENT_APP_NAMESPACE | no | 1 |
| lights | READ_ONLY | zara/domotics/lights/livinglamp | ${baseTopic}/light/sala/state | LEGACY_MAP | no | 2 |
| lights | READ_ONLY | zara/domotics/lights/poolfloor | ${baseTopic}/light/luciPedanaPiscina/state | LEGACY_MAP | no | 2 |
| lights | READ_ONLY | zara/domotics/lights/poollight | ${baseTopic}/light/luciPiscina/state | LEGACY_MAP | no | 2 |
| lights | READ_ONLY | zara/domotics/lights/poolpump | ${baseTopic}/light/pompaPiscina/state | LEGACY_MAP | no | 2 |
| lights | READ_ONLY | zara/domotics/lights/poolskimmer | ${baseTopic}/light/skimmerPiscina/state | LEGACY_MAP | no | 2 |
| lights | READ_ONLY | zara/domotics/lights/readinglight | ${baseTopic}/light/tavolinoLettura/state | LEGACY_MAP | no | 2 |
| lights | READ_ONLY | zara/domotics/lights/shelflamp | ${baseTopic}/light/libreria/state | LEGACY_MAP | no | 2 |
| lights | READ_ONLY | zara/domotics/lights/tvlamp | ${baseTopic}/light/televisione/state | LEGACY_MAP | no | 2 |
| lights | READ_ONLY | zara/domotics/luciECO | ${baseTopic}/system/luci_eco/state | LEGACY_MAP | no | 3 |
| lights | READ_ONLY | zara/domotics/luciPiscinaAuto | ${baseTopic}/system/luci_piscina_auto/state | LEGACY_MAP | no | 3 |
| lights | READ_ONLY | zigbee2mqtt/Luce_Cucina | — | OBSOLETE | no | 1 |
| lights | READ_ONLY | zigbee2mqtt/Luce_Libreria | — | PHYSICAL_TOPIC | no | 1 |
| lights | STATE | zara/android/domotica/light/${targetDevice}/state | ${baseTopic}/light/${targetDevice}/state | CURRENT_APP_NAMESPACE | no | 1 |
| lights | STATE | zara/android/domotica/system/luci_eco/state | ${baseTopic}/system/luci_eco/state | CURRENT_APP_NAMESPACE | no | 1 |
| lights | STATE | zara/android/domotica/system/luci_piscina_auto/state | ${baseTopic}/system/luci_piscina_auto/state | CURRENT_APP_NAMESPACE | no | 1 |
| system | COMMAND | zara/android/domotica/system/holiday/set | ${baseTopic}/system/holiday/set | CURRENT_APP_NAMESPACE | no | 1 |
| system | COMMAND | zara/android/domotica/system/sensore_portico/set | ${baseTopic}/system/sensore_portico/set | CURRENT_APP_NAMESPACE | yes | 1 |
| system | COMMAND | zara/android/domotica/system/set | ${baseTopic}/system/set | CURRENT_APP_NAMESPACE | yes | 1 |
| system | COMMAND | zara/android/domotica/system/time_range/set | ${baseTopic}/system/time_range/set | CURRENT_APP_NAMESPACE | no | 1 |
| system | READ_ONLY | zara/domotics/porch_sensor | ${baseTopic}/system/sensore_portico/state | LEGACY_MAP | no | 3 |
| system | READ_ONLY | zara/domotics/time_range | ${baseTopic}/system/time_range/state | LEGACY_MAP | no | 2 |
| system | STATE | zara/android/domotica/system/enabled/state | ${baseTopic}/system/enabled/state | CURRENT_APP_NAMESPACE | no | 1 |
| system | STATE | zara/android/domotica/system/holiday/state | ${baseTopic}/system/holiday/state | CURRENT_APP_NAMESPACE | no | 1 |
| system | STATE | zara/android/domotica/system/sensore_portico/state | ${baseTopic}/system/sensore_portico/state | CURRENT_APP_NAMESPACE | no | 1 |
| system | STATE | zara/android/domotica/system/time_range/state | ${baseTopic}/system/time_range/state | CURRENT_APP_NAMESPACE | no | 1 |
| unclassified | COMMAND | /maxNightSpeed/set | — | MANUAL_REVIEW | no | 1 |
| unclassified | COMMAND | zara/domotics/AC/command | — | MANUAL_REVIEW | no | 1 |
| unclassified | COMMAND | zigbee2mqtt/Termostato_Bagnetto/set | — | PHYSICAL_TOPIC | no | 1 |
| unclassified | COMMAND | zigbee2mqtt/Termostato_Bagno/set | — | PHYSICAL_TOPIC | no | 1 |
| unclassified | READ_ONLY | <dinamico> | — | DYNAMIC_TOPIC | no | 7 |
| unclassified | READ_ONLY | ${APP_BASE}/acsPufferTemp | ${baseTopic}/acsPufferTemp | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | ${APP_BASE}/env/humBedroom | ${baseTopic}/env/humBedroom | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | ${APP_BASE}/env/humLiving | ${baseTopic}/env/humLiving | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | ${APP_BASE}/env/humOutdoor | ${baseTopic}/env/humOutdoor | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | ${APP_BASE}/env/tempBedroom | ${baseTopic}/env/tempBedroom | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | ${APP_BASE}/env/tempLiving | ${baseTopic}/env/tempLiving | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | ${APP_BASE}/env/tempOutdoor | ${baseTopic}/env/tempOutdoor | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | ${APP_BASE}/pufferAltoTemp | ${baseTopic}/pufferAltoTemp | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | ${APP_BASE}/pufferBassoTemp | ${baseTopic}/pufferBassoTemp | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | /# | — | MANUAL_REVIEW | no | 1 |
| unclassified | READ_ONLY | emon/resolDL2/sensor1 | — | MANUAL_REVIEW | no | 1 |
| unclassified | READ_ONLY | emon/resolDL2/sensor2 | ${baseTopic}/pufferBassoTemp | LEGACY_MAP | yes | 2 |
| unclassified | READ_ONLY | emon/resolDL2/sensor3 | ${baseTopic}/pufferAltoTemp | LEGACY_MAP | yes | 2 |
| unclassified | READ_ONLY | emon/shellyACS/tempACS | ${baseTopic}/acsPufferTemp | LEGACY_MAP | yes | 2 |
| unclassified | READ_ONLY | shellies/shelly1-771284/relay/0 | — | PHYSICAL_TOPIC | no | 1 |
| unclassified | READ_ONLY | shellies/shelly1-B8C284/relay/0 | — | PHYSICAL_TOPIC | no | 1 |
| unclassified | READ_ONLY | shellies/shelly1-B92AF0/relay/0 | — | PHYSICAL_TOPIC | no | 1 |
| unclassified | READ_ONLY | zara/android/domotica | — | DYNAMIC_TOPIC | no | 11 |
| unclassified | READ_ONLY | zara/android/domotica/acsPufferTemp | ${baseTopic}/acsPufferTemp | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | zara/android/domotica/env/humBedroom | ${baseTopic}/env/humBedroom | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | zara/android/domotica/env/humLiving | ${baseTopic}/env/humLiving | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | zara/android/domotica/env/humOutdoor | ${baseTopic}/env/humOutdoor | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | zara/android/domotica/env/tempBedroom | ${baseTopic}/env/tempBedroom | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | zara/android/domotica/env/tempLiving | ${baseTopic}/env/tempLiving | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | zara/android/domotica/env/tempOutdoor | ${baseTopic}/env/tempOutdoor | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | zara/android/domotica/pufferAltoTemp | ${baseTopic}/pufferAltoTemp | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | zara/android/domotica/pufferBassoTemp | ${baseTopic}/pufferBassoTemp | CURRENT_APP_NAMESPACE | yes | 1 |
| unclassified | READ_ONLY | zara/domotics/modalitavacanza | ${baseTopic}/system/holiday/state | LEGACY_MAP | no | 3 |
| unclassified | READ_ONLY | zigbee2mqtt/+ | — | PHYSICAL_TOPIC | no | 1 |
| unclassified | READ_ONLY | zigbee2mqtt/Sonoff AirGuard TH camera matrimoniale | — | PHYSICAL_TOPIC | no | 2 |
| unclassified | READ_ONLY | zigbee2mqtt/Sonoff AirGuard TH esterno cucina | — | PHYSICAL_TOPIC | no | 2 |
| unclassified | READ_ONLY | zigbee2mqtt/TU-cucinaEsterno | — | PHYSICAL_TOPIC | no | 1 |
| unclassified | STATE | zigbee2mqtt/Termostato_Bagnetto | — | PHYSICAL_TOPIC | no | 1 |
| unclassified | STATE | zigbee2mqtt/Termostato_Bagno | — | PHYSICAL_TOPIC | no | 1 |
| vmc | COMMAND | zara/android/domotica/vmc/maxNightSpeed/set | ${baseTopic}/vmc/maxNightSpeed/set | CURRENT_APP_NAMESPACE | yes | 1 |
| vmc | READ_ONLY | /esp8266/brink/fanspeed | — | MANUAL_REVIEW | no | 1 |
| vmc | READ_ONLY | /vmc/ | — | MANUAL_REVIEW | no | 1 |
| vmc | READ_ONLY | ^${baseTopic}/vmc/([^/]+)/set$ | — | REGEX_ROUTE | no | 1 |
| vmc | READ_ONLY | alexa/vmc | ${baseTopic}/vmc/speed/state | LEGACY_MAP | yes | 2 |
| vmc | READ_ONLY | zara/android/domotica | — | DYNAMIC_TOPIC | no | 2 |
| vmc | READ_ONLY | zara/android/domotica/vmc/([^/]+ | ${baseTopic}/vmc/([^/]+ | CURRENT_APP_NAMESPACE | no | 1 |
| vmc | STATE | zara/android/domotica/vmc/maxNightSpeed/state | ${baseTopic}/vmc/maxNightSpeed/state | CURRENT_APP_NAMESPACE | no | 1 |
| vmc | STATE | zara/android/domotica/vmc/speed/state | ${baseTopic}/vmc/speed/state | CURRENT_APP_NAMESPACE | yes | 1 |

## Principi applicati

- Il bridge storico resta invariato.
- Il bridge v2 sarà inizialmente read-only.
- I topic fisici non vengono esposti direttamente ad Android.
- `system/set` è comando JSON non retained.
- `system/state` è stato confermato retained.
- I dispositivi obsoleti vengono esclusi.
