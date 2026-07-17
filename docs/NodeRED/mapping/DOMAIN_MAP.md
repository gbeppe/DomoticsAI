# DomoticsAI — Domain Map del bridge v2

## CLIMATE

| Ruolo | Topic corrente | Suffix DomoticsAI | Stato | Occorrenze | Nodi |
|---|---|---|---|---|---|
| COMMAND | casa/clima/cmnd/AI_climate_enabling | system/set | MIGRATE_TO_JSON | 3 | 0af2db132cc8cd0f ; 4b484152120e2d18 ; Outbound Router Settaggi |
| COMMAND | casa/clima/cmnd/vmc_max_notte | vmc/maxNightSpeed/set | KEEP_AS_COMMAND | 1 | 3db3a26c676e583c |
| COMMAND | zara/android/domotica/system/ac_auto/set | system/ac_auto/set | CURRENT_APP_NAMESPACE | 1 | Inbound Router Settaggi |
| READ_ONLY | ${APP_BASE}/env/humidexBedroom | env/humidexBedroom | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | ${APP_BASE}/env/humidexLiving | env/humidexLiving | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | /thermostat/ | — | MANUAL_REVIEW | 1 | App Main Router |
| READ_ONLY | ^${baseTopic}/thermostat/([^/]+)/target/set$ | — | REGEX_ROUTE | 1 | Inbound Router Termostati |
| READ_ONLY | emon/cameraMatrimoniale/humidex | env/humidexBedroom | LEGACY_MAP | 2 | Gateway Ambienti ; f22c31479e1b1d5b |
| READ_ONLY | emon/cameraMatrimoniale/humidity | env/humBedroom | LEGACY_MAP | 1 | Gateway Ambienti |
| READ_ONLY | emon/cameraMatrimoniale/temperature | env/tempBedroom | LEGACY_MAP | 1 | Gateway Ambienti |
| READ_ONLY | emon/emonth5/humidex | env/humidexLiving | LEGACY_MAP | 2 | Gateway Ambienti ; humidex living |
| READ_ONLY | emon/emonth5/humidity | env/humLiving | LEGACY_MAP | 2 | Gateway Ambienti ; MQTT humidity living |
| READ_ONLY | emon/emonth5/temperature_calibrated | env/tempLiving | LEGACY_MAP | 2 | Gateway Ambienti ; MQTT temperatura living |
| READ_ONLY | zara/android/domotica/env/humidexBedroom | env/humidexBedroom | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | zara/android/domotica/env/humidexLiving | env/humidexLiving | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | zara/android/domotica/thermostat/([^/]+ | thermostat/([^/]+ | CURRENT_APP_NAMESPACE | 1 | Inbound Router Termostati |
| READ_ONLY | zara/domotics/ACAuto | system/ac_auto/state | DISTINCT_SEMANTICS | 3 | 6571bf1f8e667903 ; Outbound Router Settaggi ; a40733727fb29c55 |
| STATE | casa/clima/stat/vmc_max_notte | vmc/maxNightSpeed/state | KEEP_AS_STATE | 2 | 6bf7b6d43cfb3fc3 ; Outbound Router Settaggi |
| STATE | casa/clima/stato_completo | casa/clima/stato_completo | READ_ONLY_PRIMARY | 4 | Ascolto Stato AI e TRV ; Outbound Router Termostati ; Outbound Router VMC ; fe21b464ce170529 |
| STATE | zara/android/domotica/system/ac_auto/state | system/ac_auto/state | CURRENT_APP_NAMESPACE | 1 | Outbound Router Settaggi |
| STATE | zara/android/domotica/thermostat/${targetRoom}/target/state | thermostat/${targetRoom}/target/state | CURRENT_APP_NAMESPACE | 1 | Outbound Router Termostati |

## ENERGY

| Ruolo | Topic corrente | Suffix DomoticsAI | Stato | Occorrenze | Nodi |
|---|---|---|---|---|---|
| READ_ONLY | ${APP_BASE}/energy/battery | energy/battery | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | ${APP_BASE}/energy/consumption | energy/consumption | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | ${APP_BASE}/energy/grid | energy/grid | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | ${APP_BASE}/energy/production | energy/production | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | ${APP_BASE}/energy/surplus | energy/surplus | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | TeslaPowerwall/SOE | energy/battery | LEGACY_MAP | 2 | Gateway Energia ; MQTT SOC Batt |
| READ_ONLY | TeslaPowerwall/load_instant_power | energy/consumption | LEGACY_MAP | 2 | Gateway Energia ; MQTT Potenza Casa (Load W) |
| READ_ONLY | TeslaPowerwall/site_instant_power | energy/grid | LEGACY_MAP | 2 | Gateway Energia ; MQTT Potenza Produzione FV (FV W) |
| READ_ONLY | TeslaPowerwall/solar_instant_power | energy/production | LEGACY_MAP | 2 | Gateway Energia ; MQTT Potenza Produzione FV (FV W) |
| READ_ONLY | zara/android/domotica/energy/battery | energy/battery | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | zara/android/domotica/energy/consumption | energy/consumption | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | zara/android/domotica/energy/grid | energy/grid | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | zara/android/domotica/energy/production | energy/production | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | zara/android/domotica/energy/surplus | energy/surplus | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |

## FIREPLACE

| Ruolo | Topic corrente | Suffix DomoticsAI | Stato | Occorrenze | Nodi |
|---|---|---|---|---|---|
| COMMAND | /command | — | MANUAL_REVIEW | 1 | Ponte Traduttore Caminetto |
| COMMAND | alexa/caminetto/command | — | MANUAL_REVIEW | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | / | — | DYNAMIC_TOPIC | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | /esp8266/palazzetti | — | MANUAL_REVIEW | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | /getstatus | — | MANUAL_REVIEW | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | /hello | — | MANUAL_REVIEW | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | /log/message | — | MANUAL_REVIEW | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | /power | — | MANUAL_REVIEW | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | alexa/caminetto | — | MANUAL_REVIEW | 2 | Ponte Traduttore Caminetto ; alexa/caminetto |
| READ_ONLY | alexa/caminetto/power | — | MANUAL_REVIEW | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | emon/focolare/powerraw | casa/stufa/stat/potenza | LEGACY_MAP | 2 | 8022e945f076fa2f ; Ponte Traduttore Caminetto |
| READ_ONLY | zara/android/domotica | — | DYNAMIC_TOPIC | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | zara/domotics/palazzetti/ | — | MANUAL_REVIEW | 1 | Ponte Traduttore Caminetto |
| READ_ONLY | zara/domotics/palazzetti/# | casa/stufa/stat/# | LEGACY_MAP | 1 | zara/domotics/palazzetti/# |
| READ_ONLY | zara/domotics/palazzetti/set/modalita | casa/stufa/stat/modalita | LEGACY_MAP | 1 | Ponte Traduttore Caminetto |
| STATE | zara/android/domotica/casa/stufa/stat/acceso | casa/stufa/stat/acceso | CURRENT_APP_NAMESPACE | 1 | Ponte Traduttore Caminetto |
| STATE | zara/android/domotica/casa/stufa/stat/modalita | casa/stufa/stat/modalita | CURRENT_APP_NAMESPACE | 1 | Ponte Traduttore Caminetto |
| STATE | zara/android/domotica/casa/stufa/stat/potenza | casa/stufa/stat/potenza | CURRENT_APP_NAMESPACE | 1 | Ponte Traduttore Caminetto |

## HISTORY

| Ruolo | Topic corrente | Suffix DomoticsAI | Stato | Occorrenze | Nodi |
|---|---|---|---|---|---|
| READ_ONLY | /history/ac/request | — | LOCAL_SERVICE | 1 | function 33 |
| READ_ONLY | zara/android/domotica/history/ac/response | history/ac/response | CURRENT_APP_NAMESPACE | 1 | Formatta Response App |

## LIGHTS

| Ruolo | Topic corrente | Suffix DomoticsAI | Stato | Occorrenze | Nodi |
|---|---|---|---|---|---|
| COMMAND | /scene/set | — | MANUAL_REVIEW | 1 | Inbound Router Luci |
| COMMAND | /set | — | MANUAL_REVIEW | 1 | Inbound Router Luci |
| COMMAND | shellies/shelly1-esterno/relay/0/command | — | OBSOLETE | 1 | Inbound Router Luci |
| COMMAND | zara/android/domotica/scene/set | scene/set | CURRENT_APP_NAMESPACE | 1 | App -> Comando Scene Luci |
| COMMAND | zara/android/domotica/system/luci_eco/set | system/luci_eco/set | CURRENT_APP_NAMESPACE | 1 | Inbound Router Settaggi |
| COMMAND | zara/android/domotica/system/luci_piscina_auto/set | system/luci_piscina_auto/set | CURRENT_APP_NAMESPACE | 1 | Inbound Router Settaggi |
| COMMAND | zigbee2mqtt/Luce_Cucina/set | — | OBSOLETE | 1 | Inbound Router Luci |
| READ_ONLY | /light/ | — | MANUAL_REVIEW | 2 | App Main Router ; Inbound Router Luci |
| READ_ONLY | /scene/ | — | MANUAL_REVIEW | 1 | App Main Router |
| READ_ONLY | ^${baseTopic}/light/([^/]+)/set$ | — | REGEX_ROUTE | 1 | Inbound Router Luci |
| READ_ONLY | shellies/shelly1-771284/relay/0 | — | PHYSICAL_TOPIC | 1 | Outbound Router Luci |
| READ_ONLY | shellies/shelly1-B8C284/relay/0 | — | PHYSICAL_TOPIC | 1 | Outbound Router Luci |
| READ_ONLY | shellies/shelly1-B92AF0/relay/0 | — | PHYSICAL_TOPIC | 1 | Outbound Router Luci |
| READ_ONLY | shellies/shelly1-esterno | — | OBSOLETE | 1 | Outbound Router Luci |
| READ_ONLY | zara/android/domotica | — | DYNAMIC_TOPIC | 2 | Inbound Router Luci ; Outbound Router Luci |
| READ_ONLY | zara/android/domotica/light/([^/]+ | light/([^/]+ | CURRENT_APP_NAMESPACE | 1 | Inbound Router Luci |
| READ_ONLY | zara/domotics/lights/livinglamp | light/sala/state | LEGACY_MAP | 2 | Outbound Router Luci ; b49453f6cdbbab3d |
| READ_ONLY | zara/domotics/lights/poolfloor | light/luciPedanaPiscina/state | LEGACY_MAP | 2 | 3174da2bdd10ea30 ; Outbound Router Luci |
| READ_ONLY | zara/domotics/lights/poollight | light/luciPiscina/state | LEGACY_MAP | 2 | Outbound Router Luci ; c5fbbdc4bdf7fbe0 |
| READ_ONLY | zara/domotics/lights/poolpump | light/pompaPiscina/state | LEGACY_MAP | 2 | 04eee2d096fc8523 ; Outbound Router Luci |
| READ_ONLY | zara/domotics/lights/poolskimmer | light/skimmerPiscina/state | LEGACY_MAP | 2 | 3f8fefa8f0d98ffd ; Outbound Router Luci |
| READ_ONLY | zara/domotics/lights/readinglight | light/tavolinoLettura/state | LEGACY_MAP | 2 | 5d2d6ba3ad4c3262 ; Outbound Router Luci |
| READ_ONLY | zara/domotics/lights/shelflamp | light/libreria/state | LEGACY_MAP | 2 | 8e3fcbfc031083cc ; Outbound Router Luci |
| READ_ONLY | zara/domotics/lights/tvlamp | light/televisione/state | LEGACY_MAP | 2 | Outbound Router Luci ; f169b915a19f8af6 |
| READ_ONLY | zara/domotics/luciECO | system/luci_eco/state | LEGACY_MAP | 3 | Outbound Router Settaggi ; b51bd73002b7f88b ; c698d126b68e11f8 |
| READ_ONLY | zara/domotics/luciPiscinaAuto | system/luci_piscina_auto/state | LEGACY_MAP | 3 | 3bfeb435fb6e3132 ; 5b7675e55cbc4b81 ; Outbound Router Settaggi |
| READ_ONLY | zigbee2mqtt/Luce_Cucina | — | OBSOLETE | 1 | Outbound Router Luci |
| READ_ONLY | zigbee2mqtt/Luce_Libreria | — | PHYSICAL_TOPIC | 1 | Outbound Router Luci |
| STATE | zara/android/domotica/light/${targetDevice}/state | light/${targetDevice}/state | CURRENT_APP_NAMESPACE | 1 | Outbound Router Luci |
| STATE | zara/android/domotica/system/luci_eco/state | system/luci_eco/state | CURRENT_APP_NAMESPACE | 1 | Outbound Router Settaggi |
| STATE | zara/android/domotica/system/luci_piscina_auto/state | system/luci_piscina_auto/state | CURRENT_APP_NAMESPACE | 1 | Outbound Router Settaggi |

## SYSTEM

| Ruolo | Topic corrente | Suffix DomoticsAI | Stato | Occorrenze | Nodi |
|---|---|---|---|---|---|
| COMMAND | zara/android/domotica/system/holiday/set | system/holiday/set | CURRENT_APP_NAMESPACE | 1 | Inbound Router Settaggi |
| COMMAND | zara/android/domotica/system/sensore_portico/set | system/sensore_portico/set | CURRENT_APP_NAMESPACE | 1 | Inbound Router Settaggi |
| COMMAND | zara/android/domotica/system/set | system/set | CURRENT_APP_NAMESPACE | 1 | Outbound Router Settaggi |
| COMMAND | zara/android/domotica/system/time_range/set | system/time_range/set | CURRENT_APP_NAMESPACE | 1 | Inbound Router Settaggi |
| READ_ONLY | zara/domotics/porch_sensor | system/sensore_portico/state | LEGACY_MAP | 3 | Outbound Router Settaggi ; d073880643e29f9e ; fc0ba16b2241adf1 |
| READ_ONLY | zara/domotics/time_range | system/time_range/state | LEGACY_MAP | 2 | 2b99835ee36a758d ; Outbound Router Settaggi |
| STATE | zara/android/domotica/system/enabled/state | system/enabled/state | CURRENT_APP_NAMESPACE | 1 | Inbound Router Settaggi |
| STATE | zara/android/domotica/system/holiday/state | system/holiday/state | CURRENT_APP_NAMESPACE | 1 | Outbound Router Settaggi |
| STATE | zara/android/domotica/system/sensore_portico/state | system/sensore_portico/state | CURRENT_APP_NAMESPACE | 1 | Outbound Router Settaggi |
| STATE | zara/android/domotica/system/time_range/state | system/time_range/state | CURRENT_APP_NAMESPACE | 1 | Outbound Router Settaggi |

## UNCLASSIFIED

| Ruolo | Topic corrente | Suffix DomoticsAI | Stato | Occorrenze | Nodi |
|---|---|---|---|---|---|
| COMMAND | /maxNightSpeed/set | — | MANUAL_REVIEW | 1 | App Main Router |
| COMMAND | zara/domotics/AC/command | — | MANUAL_REVIEW | 1 | Inbound Router Termostati |
| COMMAND | zigbee2mqtt/Termostato_Bagnetto/set | — | PHYSICAL_TOPIC | 1 | Inbound Router Termostati |
| COMMAND | zigbee2mqtt/Termostato_Bagno/set | — | PHYSICAL_TOPIC | 1 | Inbound Router Termostati |
| READ_ONLY | <dinamico> | — | DYNAMIC_TOPIC | 7 | 302a2960a9fdf64f ; 42c039cfb62a43a2 ; 59b830f96fe6bb19 ; Aggiorna Stato App (Retain) ; Esecuzione Hardware ; MQTT Esterno (Alexa) ; MQTT Locale (App & ESP) |
| READ_ONLY | ${APP_BASE}/acsPufferTemp | acsPufferTemp | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | ${APP_BASE}/env/humBedroom | env/humBedroom | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | ${APP_BASE}/env/humLiving | env/humLiving | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | ${APP_BASE}/env/humOutdoor | env/humOutdoor | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | ${APP_BASE}/env/tempBedroom | env/tempBedroom | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | ${APP_BASE}/env/tempLiving | env/tempLiving | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | ${APP_BASE}/env/tempOutdoor | env/tempOutdoor | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | ${APP_BASE}/pufferAltoTemp | pufferAltoTemp | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | ${APP_BASE}/pufferBassoTemp | pufferBassoTemp | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | /# | — | MANUAL_REVIEW | 1 | Configurazione Sottoscrizione Dinamica |
| READ_ONLY | emon/resolDL2/sensor1 | — | MANUAL_REVIEW | 1 | 9ac2eb0ded5a2efd |
| READ_ONLY | emon/resolDL2/sensor2 | pufferBassoTemp | LEGACY_MAP | 2 | Gateway Energia ; efe270ec96f87af7 |
| READ_ONLY | emon/resolDL2/sensor3 | pufferAltoTemp | LEGACY_MAP | 2 | 0b370faa3935fe88 ; Gateway Energia |
| READ_ONLY | emon/shellyACS/tempACS | acsPufferTemp | LEGACY_MAP | 2 | 8c0fe215629e8f46 ; Gateway Energia |
| READ_ONLY | shellies/shelly1-771284/relay/0 | — | PHYSICAL_TOPIC | 1 | 118da562063f2d9a |
| READ_ONLY | shellies/shelly1-B8C284/relay/0 | — | PHYSICAL_TOPIC | 1 | e338f28f56433e4c |
| READ_ONLY | shellies/shelly1-B92AF0/relay/0 | — | PHYSICAL_TOPIC | 1 | 3f0b0e50b51f8568 |
| READ_ONLY | zara/android/domotica | — | DYNAMIC_TOPIC | 11 | App Main Router ; Configurazione Sottoscrizione Dinamica ; Formatta Response App ; Gateway Ambienti ; Gateway Energia ; Inbound Router Settaggi ; Inbound Router Termostati ; Outbound Router Settaggi ; Outbound Router Termostati ; function 29 ; function 33 |
| READ_ONLY | zara/android/domotica/acsPufferTemp | acsPufferTemp | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | zara/android/domotica/env/humBedroom | env/humBedroom | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | zara/android/domotica/env/humLiving | env/humLiving | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | zara/android/domotica/env/humOutdoor | env/humOutdoor | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | zara/android/domotica/env/tempBedroom | env/tempBedroom | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | zara/android/domotica/env/tempLiving | env/tempLiving | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | zara/android/domotica/env/tempOutdoor | env/tempOutdoor | CURRENT_APP_NAMESPACE | 1 | Gateway Ambienti |
| READ_ONLY | zara/android/domotica/pufferAltoTemp | pufferAltoTemp | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | zara/android/domotica/pufferBassoTemp | pufferBassoTemp | CURRENT_APP_NAMESPACE | 1 | Gateway Energia |
| READ_ONLY | zara/domotics/modalitavacanza | system/holiday/state | LEGACY_MAP | 3 | 1d09b533095d68c1 ; 28256464972b2329 ; Outbound Router Settaggi |
| READ_ONLY | zigbee2mqtt/+ | — | PHYSICAL_TOPIC | 1 | Ascolto Hardware Reale |
| READ_ONLY | zigbee2mqtt/Sonoff AirGuard TH camera matrimoniale | — | PHYSICAL_TOPIC | 2 | Gateway Ambienti ; zigbee2mqtt/Sonoff AirGuard TH camera matrimoniale |
| READ_ONLY | zigbee2mqtt/Sonoff AirGuard TH esterno cucina | — | PHYSICAL_TOPIC | 2 | Gateway Ambienti ; MQTT Sonoff AirGuard TH esterno cucina |
| READ_ONLY | zigbee2mqtt/TU-cucinaEsterno | — | PHYSICAL_TOPIC | 1 | cee938eea10f7bd4 |
| STATE | zigbee2mqtt/Termostato_Bagnetto | — | PHYSICAL_TOPIC | 1 | Outbound Router Termostati |
| STATE | zigbee2mqtt/Termostato_Bagno | — | PHYSICAL_TOPIC | 1 | Outbound Router Termostati |

## VMC

| Ruolo | Topic corrente | Suffix DomoticsAI | Stato | Occorrenze | Nodi |
|---|---|---|---|---|---|
| COMMAND | zara/android/domotica/vmc/maxNightSpeed/set | vmc/maxNightSpeed/set | CURRENT_APP_NAMESPACE | 1 | Outbound Router Settaggi |
| READ_ONLY | /esp8266/brink/fanspeed | — | MANUAL_REVIEW | 1 | Inbound Router VMC |
| READ_ONLY | /vmc/ | — | MANUAL_REVIEW | 1 | App Main Router |
| READ_ONLY | ^${baseTopic}/vmc/([^/]+)/set$ | — | REGEX_ROUTE | 1 | Inbound Router VMC |
| READ_ONLY | alexa/vmc | vmc/speed/state | LEGACY_MAP | 2 | App -> Target VMC ; Outbound Router VMC |
| READ_ONLY | zara/android/domotica | — | DYNAMIC_TOPIC | 2 | Inbound Router VMC ; Outbound Router VMC |
| READ_ONLY | zara/android/domotica/vmc/([^/]+ | vmc/([^/]+ | CURRENT_APP_NAMESPACE | 1 | Inbound Router VMC |
| STATE | zara/android/domotica/vmc/maxNightSpeed/state | vmc/maxNightSpeed/state | CURRENT_APP_NAMESPACE | 1 | Inbound Router Settaggi |
| STATE | zara/android/domotica/vmc/speed/state | vmc/speed/state | CURRENT_APP_NAMESPACE | 1 | Outbound Router VMC |
