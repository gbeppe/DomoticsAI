# DomoticsAI — Inventario del bridge Node-RED esistente

- File analizzato: `docs/NodeRED/source/android-app-bridge-current.json`
- Nodi totali: `104`
- Schede/subflow: `1`
- Broker MQTT: `2`
- MQTT in: `43`
- MQTT out: `13`
- Function Node: `18`
- Link Node: `18`

## Broker

| ID | Nome | Host | Porta | TLS | Protocollo |
|---|---|---|---|---|---|
| 3ed6302a.5af928 | domopi mqtt | 192.168.1.20 | 1883 | false | 4 |
| cfd9898e.1367b8 | emoncms mqtt | 192.168.1.15 | 1883 | false | 4 |

## Nodi MQTT

| Direzione | Nodo | Topic | Broker | QoS | Retain | Disabilitato |
|---|---|---|---|---|---|---|
| publish | Esecuzione Hardware | <dinamico> | 192.168.1.20:1883 | 1 | false | true |
| subscribe | Ascolto Hardware Reale | zigbee2mqtt/+ | 192.168.1.20:1883 | 1 |  | false |
| publish | Aggiorna Stato App (Retain) | <dinamico> | 192.168.1.20:1883 | 1 | true | false |
| subscribe | Ascolto Stato AI e TRV | casa/clima/stato_completo | 192.168.1.20:1883 | 1 |  | false |
| subscribe | App -> Target VMC | alexa/vmc | 192.168.1.15:1883 | 1 |  | false |
| subscribe | b49453f6cdbbab3d | zara/domotics/lights/livinglamp | 192.168.1.20:1883 | 2 |  | false |
| subscribe | 8e3fcbfc031083cc | zara/domotics/lights/shelflamp | 192.168.1.20:1883 | 2 |  | false |
| subscribe | f169b915a19f8af6 | zara/domotics/lights/tvlamp | 192.168.1.20:1883 | 2 |  | false |
| subscribe | 118da562063f2d9a | shellies/shelly1-771284/relay/0 | 192.168.1.15:1883 | 2 |  | false |
| subscribe | 3f0b0e50b51f8568 | shellies/shelly1-B92AF0/relay/0 | 192.168.1.15:1883 | 2 |  | false |
| subscribe | e338f28f56433e4c | shellies/shelly1-B8C284/relay/0 | 192.168.1.15:1883 | 2 |  | false |
| subscribe | c5fbbdc4bdf7fbe0 | zara/domotics/lights/poollight | 192.168.1.20:1883 | 2 |  | false |
| subscribe | 3174da2bdd10ea30 | zara/domotics/lights/poolfloor | 192.168.1.20:1883 | 2 |  | false |
| subscribe | 3f8fefa8f0d98ffd | zara/domotics/lights/poolskimmer | 192.168.1.20:1883 | 2 |  | false |
| subscribe | 04eee2d096fc8523 | zara/domotics/lights/poolpump | 192.168.1.20:1883 | 2 |  | false |
| subscribe | App -> Comando Scene Luci | zara/android/domotica/scene/set | 192.168.1.20:1883 | 2 |  | true |
| subscribe | zigbee2mqtt/Sonoff AirGuard TH camera matrimoniale | zigbee2mqtt/Sonoff AirGuard TH camera matrimoniale | 192.168.1.15:1883 | 2 |  | false |
| subscribe | MQTT SOC Batt | TeslaPowerwall/SOE | 192.168.1.15:1883 | 2 |  | false |
| subscribe | MQTT Potenza Casa (Load W) | TeslaPowerwall/load_instant_power | 192.168.1.15:1883 | 2 |  | false |
| subscribe | MQTT Potenza Produzione FV (FV W) | TeslaPowerwall/solar_instant_power | 192.168.1.15:1883 | 2 |  | false |
| subscribe | MQTT temperatura living | emon/emonth5/temperature_calibrated | 192.168.1.15:1883 | 2 |  | false |
| subscribe | cee938eea10f7bd4 | zigbee2mqtt/TU-cucinaEsterno | 192.168.1.20:1883 | 2 |  | false |
| subscribe | efe270ec96f87af7 | emon/resolDL2/sensor2 | 192.168.1.15:1883 | 2 |  | false |
| subscribe | 0b370faa3935fe88 | emon/resolDL2/sensor3 | 192.168.1.15:1883 | 2 |  | false |
| subscribe | 9ac2eb0ded5a2efd | emon/resolDL2/sensor1 | 192.168.1.15:1883 | 2 |  | false |
| subscribe | 8c0fe215629e8f46 | emon/shellyACS/tempACS | 192.168.1.15:1883 | 2 |  | false |
| subscribe | MQTT humidity living | emon/emonth5/humidity | 192.168.1.15:1883 | 2 |  | false |
| subscribe | MQTT Sonoff AirGuard TH esterno cucina | zigbee2mqtt/Sonoff AirGuard TH esterno cucina | 192.168.1.20:1883 | 2 |  | false |
| publish | 1d09b533095d68c1 | zara/domotics/modalitavacanza | 192.168.1.20:1883 | 0 | true | false |
| publish | b51bd73002b7f88b | zara/domotics/luciECO | 192.168.1.20:1883 | 0 | true | false |
| publish | 3bfeb435fb6e3132 | zara/domotics/luciPiscinaAuto | 192.168.1.20:1883 | 0 | true | false |
| subscribe | 42c039cfb62a43a2 | <dinamico> | 192.168.1.20:1883 | 2 |  | false |
| publish | a40733727fb29c55 | zara/domotics/ACAuto | 192.168.1.20:1883 | 0 | true | false |
| publish | 3db3a26c676e583c | casa/clima/cmnd/vmc_max_notte | 192.168.1.20:1883 |  | true | false |
| publish | 0af2db132cc8cd0f | casa/clima/cmnd/AI_climate_enabling | 192.168.1.20:1883 |  |  | false |
| subscribe | 4b484152120e2d18 | casa/clima/cmnd/AI_climate_enabling | 192.168.1.20:1883 | 2 |  | false |
| subscribe | 28256464972b2329 | zara/domotics/modalitavacanza | 192.168.1.20:1883 | 2 |  | false |
| subscribe | c698d126b68e11f8 | zara/domotics/luciECO | 192.168.1.20:1883 | 2 |  | false |
| subscribe | 5b7675e55cbc4b81 | zara/domotics/luciPiscinaAuto | 192.168.1.20:1883 | 2 |  | false |
| subscribe | 6571bf1f8e667903 | zara/domotics/ACAuto | 192.168.1.20:1883 | 2 |  | false |
| subscribe | 6bf7b6d43cfb3fc3 | casa/clima/stat/vmc_max_notte | 192.168.1.20:1883 | 2 |  | false |
| subscribe | fc0ba16b2241adf1 | zara/domotics/porch_sensor | 192.168.1.20:1883 | 0 |  | false |
| publish | d073880643e29f9e | zara/domotics/porch_sensor | 192.168.1.20:1883 |  |  | false |
| subscribe | fe21b464ce170529 | casa/clima/stato_completo | 192.168.1.20:1883 | 2 |  | false |
| subscribe | MQTT Potenza Produzione FV (FV W) | TeslaPowerwall/site_instant_power | 192.168.1.15:1883 | 2 |  | false |
| subscribe | f22c31479e1b1d5b | emon/cameraMatrimoniale/humidex | 192.168.1.15:1883 | 2 |  | false |
| subscribe | humidex living | emon/emonth5/humidex | 192.168.1.15:1883 | 2 |  | false |
| subscribe | zara/domotics/palazzetti/# | zara/domotics/palazzetti/# | 192.168.1.15:1883 | 0 |  | false |
| subscribe | alexa/caminetto | alexa/caminetto | 192.168.1.15:1883 | 0 |  | false |
| publish | MQTT Locale (App & ESP) | <dinamico> | 192.168.1.20:1883 | 1 | true | false |
| publish | MQTT Esterno (Alexa) | <dinamico> | : | 1 | false | true |
| subscribe | 8022e945f076fa2f | emon/focolare/powerraw | 192.168.1.15:1883 | 2 |  | false |
| subscribe | 5d2d6ba3ad4c3262 | zara/domotics/lights/readinglight | 192.168.1.20:1883 | 2 |  | false |
| publish | 2b99835ee36a758d | zara/domotics/time_range | 192.168.1.20:1883 |  | true | false |
| subscribe | 59b830f96fe6bb19 | <dinamico> | 192.168.1.20:1883 | 2 |  | false |
| publish | 302a2960a9fdf64f | <dinamico> | 192.168.1.20:1883 | 1 | false | false |

## Dipendenze Link Node

| Tipo | Nodo | ID collegati | ID esterni/non risolti |
|---|---|---|---|
| link out | libreria lamp | 47f620dc.6ac2c | 47f620dc.6ac2c |
| link out | link out 6 | 24aa1379.deb964 | 24aa1379.deb964 |
| link out | living lamp | 9e5f898e.c59138 | 9e5f898e.c59138 |
| link out | tv lamp | c30ff31.adfb29 | c30ff31.adfb29 |
| link out | pedana piscina | 6df7f7f7.9f7d2 | 6df7f7f7.9f7d2 |
| link out | acqua piscina | fa02d7e9.d1dd98 | fa02d7e9.d1dd98 |
| link out | reading lamp | 1b158ed508bcebe6 | 1b158ed508bcebe6 |
| link out | portico lamp | 80597807.dad32 | 80597807.dad32 |
| link out | lavanderia lamp | 9fb74d0e.eaccd8 | 9fb74d0e.eaccd8 |
| link out | ingresso secondario lamp | fa6ca68b.fc2a1 | fa6ca68b.fc2a1 |
| link out | pompa                  piscina | 22829371.4cbb3c | 22829371.4cbb3c |
| link out | skimmer piscina | d2f096c1.1f989 | d2f096c1.1f989 |
| link out | tv mode | 73a44c65.2cfd94 | 73a44c65.2cfd94 |
| link out | sleep mode | 3d92676c.84cb88 | 3d92676c.84cb88 |
| link out | tutte luci on | a8512076.5af378 | a8512076.5af378 |
| link out | tutte luci off | acff3264.d487c | acff3264.d487c |
| link in | app_base_topic | b2f3fb91a5f30a07 | b2f3fb91a5f30a07 |
| link in | storico 7gg | b2f3fb91a5f30a07,94110e1cdf7ba7a3 | b2f3fb91a5f30a07,94110e1cdf7ba7a3 |

## Anomalie e punti da verificare

- MQTT out verso broker reale: Esecuzione Hardware (topic=<dinamico>, retain=false)
- MQTT out verso broker reale: Aggiorna Stato App (Retain) (topic=<dinamico>, retain=true)
- MQTT out verso broker reale: 1d09b533095d68c1 (topic=zara/domotics/modalitavacanza, retain=true)
- MQTT out verso broker reale: b51bd73002b7f88b (topic=zara/domotics/luciECO, retain=true)
- MQTT out verso broker reale: 3bfeb435fb6e3132 (topic=zara/domotics/luciPiscinaAuto, retain=true)
- MQTT out verso broker reale: a40733727fb29c55 (topic=zara/domotics/ACAuto, retain=true)
- MQTT out verso broker reale: 3db3a26c676e583c (topic=casa/clima/cmnd/vmc_max_notte, retain=true)
- MQTT out verso broker reale: 0af2db132cc8cd0f (topic=casa/clima/cmnd/AI_climate_enabling, retain=)
- MQTT out verso broker reale: d073880643e29f9e (topic=zara/domotics/porch_sensor, retain=)
- MQTT out verso broker reale: MQTT Locale (App & ESP) (topic=<dinamico>, retain=true)
- MQTT out verso broker reale: 2b99835ee36a758d (topic=zara/domotics/time_range, retain=true)
- MQTT out verso broker reale: 302a2960a9fdf64f (topic=<dinamico>, retain=false)
- Outbound Router Settaggi pubblica lo stato su system/set; nel protocollo v2 deve usare system/state.
- Dipendenze Link Node esterne all'export: 18 nodi.

## File generati

- `ANDROID_APP_BRIDGE_NODE_INVENTORY.csv`
- `ANDROID_APP_BRIDGE_MQTT_INVENTORY.csv`
- `ANDROID_APP_BRIDGE_FUNCTION_TOPICS.csv`
- `ANDROID_APP_BRIDGE_LINK_DEPENDENCIES.csv`

## Limiti dell'analisi

- I topic dinamici costruiti da Function Node sono estratti euristicamente.
- I Link Node con destinazioni esterne richiedono gli export delle schede collegate.
- L'inventario non abilita alcun comando verso gli impianti.
