# MQTT Topics — classificazione iniziale

> Documento generato automaticamente dallo snapshot Node-RED. La classificazione è una base di lavoro e richiede revisione manuale.

## Riepilogo

- **Sensori ambientali**: 36 topic
- **Luci**: 25 topic
- **Altro / da classificare**: 19 topic
- **Impianti termici**: 12 topic
- **Termostati**: 10 topic
- **Comandi app**: 8 topic
- **Clima**: 8 topic
- **Alexa e voce**: 5 topic
- **Powerwall**: 4 topic
- **VMC**: 3 topic
- **Presenza**: 3 topic
- **Energia e fotovoltaico**: 3 topic
- **Diagnostica**: 3 topic
- **Telecamere**: 2 topic
- **Piscina**: 2 topic
- **Irrigazione**: 1 topic

## Catalogo

### Clima

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `casa/clima/cmnd/emergency_humidex_away` | SUB(1) | domopi mqtt | 1 | — | AI climate |
| `casa/clima/cmnd/target_humidex` | SUB(1) | domopi mqtt | 1 | — | AI climate |
| `casa/clima/stato_completo` | SUB(3) + PUB(1) | domopi mqtt | 1 | 2 | — | AI climate | Android APP Bridge |
| `emon/AC/command` | SUB(1) + PUB(2) | emoncms mqtt | 2 | true | AI climate |
| `emon/AC/emeter_power` | SUB(1) | emoncms mqtt | 2 | — | AI climate |
| `zara/domotics/AC/command` | SUB(2) + PUB(1) | domopi mqtt | 2 | — | AI climate | Dashboard Android App |
| `zara/domotics/BedroomHumidex` | SUB(1) | emoncms mqtt | 2 | — | AI climate |
| `zara/domotics/LivingHumidex` | SUB(1) | emoncms mqtt | 2 | — | AI climate |

### VMC

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `/esp8266/brink/fanspeed` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `casa/clima/cmnd/vmc_max_notte` | SUB(1) + PUB(2) | domopi mqtt | 1 | true | AI climate | Android APP Bridge |
| `casa/clima/stat/vmc_max_notte` | SUB(2) | domopi mqtt | 2 | — | Android APP Bridge |

### Energia e fotovoltaico

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `PWMController/value` | PUB(1) | domopi mqtt | — | — | Diverter |
| `TeslaPowerwall/solar_instant_power` | SUB(3) | emoncms mqtt | 2 | — | AI climate | Android APP Bridge |
| `emon/emontx3/power1` | SUB(2) | emoncms mqtt | 2 | — | Dashboard Android App | Google Webhook |

### Powerwall

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `TeslaPowerwall/SOE` | SUB(3) | emoncms mqtt | 2 | — | AI climate | Android APP Bridge |
| `TeslaPowerwall/load_instant_power` | SUB(3) | emoncms mqtt | 2 | — | AI climate | Android APP Bridge |
| `TeslaPowerwall/site_instant_power` | SUB(2) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `TeslaPowerwall/site_intant_power` | SUB(1) | emoncms mqtt | 2 | — | Diverter |

### Sensori ambientali

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `emon/bagnoServizio/humidity` | PUB(1) | emoncms mqtt | 2 | true | ZigBee sensors |
| `emon/bagnoServizio/temperature` | SUB(1) + PUB(1) | emoncms mqtt | 2 | true | Dashboard Android App | ZigBee sensors |
| `emon/cameraMatrimoniale/humidity` | SUB(1) + PUB(1) | emoncms mqtt | 2 | true | Dashboard Android App | ZigBee sensors |
| `emon/cameraMatrimoniale/temperature` | SUB(2) + PUB(1) | emoncms mqtt | 2 | true | AI climate | Dashboard Android App | ZigBee sensors |
| `emon/cameretta/humidity` | PUB(1) | emoncms mqtt | 2 | true | ZigBee sensors |
| `emon/cameretta/temperature` | PUB(1) | emoncms mqtt | 2 | true | ZigBee sensors |
| `emon/centraleTermica/humidity` | PUB(1) | emoncms mqtt | 2 | true | ZigBee sensors |
| `emon/centraleTermica/temperature` | PUB(1) | emoncms mqtt | 2 | true | ZigBee sensors |
| `emon/emonth5/humidex` | SUB(1) + PUB(1) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `emon/emonth5/humidity` | SUB(3) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `emon/emonth5/temperature_calibrated` | SUB(5) | emoncms mqtt | 2 | — | AI climate | Android APP Bridge | Dashboard Android App |
| `emon/resolDL2/sensor1` | SUB(3) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `emon/resolDL2/sensor2` | SUB(3) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `emon/resolDL2/sensor3` | SUB(3) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `emon/shellyACS/tempACS` | SUB(3) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `emon/shellyBagnocamera/temperature_calibrated` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `emon/weather/RelativeHumidity` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `emon/weather/extHumidity` | SUB(1) + PUB(1) | emoncms mqtt | 2 | true | Dashboard Android App | ZigBee sensors |
| `emon/weather/extTemp` | SUB(1) + PUB(1) | emoncms mqtt | 2 | true | Dashboard Android App | ZigBee sensors |
| `emon/weather/tomorrowSolarIrradiance` | SUB(1) | emoncms mqtt | 2 | — | start local scripts |
| `tele/tasmotaFrigorifero/SENSOR` | SUB(1) | domopi mqtt | 2 | — | mqtt to emoncms |
| `zara/domotics/porch_sensor` | SUB(2) + PUB(2) | domopi mqtt | 0 | true | Android APP Bridge | Dashboard Android App |
| `zigbee2mqtt/IkeaMotion_cucina_outdoor` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/IkeaMotion_ingresso_principale` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/IkeaMotion_ingresso_secondario` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/IkeaMotion_lavanderia` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/IkeaMotion_pompeiana` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/Sonoff AirGuard TH esterno cucina` | SUB(3) | domopi mqtt | 2 | — | Android APP Bridge | ZigBee sensors |
| `zigbee2mqtt/TU-bagnoServizio` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/TU-cameraMatrimoniale` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/TU-cameretta` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/TU-centraleTermica` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/TU-cucinaEsterno` | SUB(4) | domopi mqtt | 2 | — | AI climate | Android APP Bridge | ZigBee sensors |
| `zigbee2mqtt/bridge/info` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/bridge/response/health_check` | PUB(1) | domopi mqtt | 2 | — | ZigBee sensors |
| `zigbee2mqtt/bridge/state` | SUB(1) | domopi mqtt | 2 | — | ZigBee sensors |

### Termostati

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `cmnd/SmallBathroomThermostat/TEMPTARGETSET` | SUB(1) + PUB(1) | domopi mqtt | 2 | true | Dashboard Android App |
| `cmnd/SmallBathroomThermostat/THERMOSTATMODESET` | PUB(1) | domopi mqtt | — | true | Dashboard Android App |
| `cmnd/tasmota_F294D7/TEMPTARGETSET` | SUB(1) + PUB(1) | domopi mqtt | 2 | true | Dashboard Android App |
| `cmnd/tasmota_F294D7/THERMOSTATMODESET` | PUB(1) | domopi mqtt | — | true | Dashboard Android App |
| `cmnd/tasmota_F32F4F/TEMPTARGETSET` | SUB(1) + PUB(1) | domopi mqtt | 2 | true | Dashboard Android App |
| `cmnd/tasmota_F32F4F/THERMOSTATMODESET` | PUB(1) | domopi mqtt | — | true | Dashboard Android App |
| `emon/TermostatLiving/Switch` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `emon/TermostatMainBathroom/Switch` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `zara/domotics/SmallBathroomThermostatMaxValue` | SUB(1) + PUB(1) | emoncms mqtt | 0 | 2 | true | Dashboard Android App |
| `zara/domotics/SmallBathroomThermostatMinValue` | SUB(1) + PUB(1) | emoncms mqtt | 0 | 2 | true | Dashboard Android App |

### Impianti termici

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `emon/AC/ACstatus` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `emon/OTGcaldaia/flame` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `emon/OTGcaldaia/modulation` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `emon/focolare/powerraw` | SUB(2) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `emon/resolDL2/pump1` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `zara/domotics/attivaACS` | PUB(1) | emoncms mqtt | 1 | true | Amazon Echo |
| `zara/domotics/floorpumpstate` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `zara/domotics/palazzetti/#` | SUB(1) | emoncms mqtt | 0 | — | Android APP Bridge |
| `zara/domotics/palazzetti/acceso` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `zara/domotics/palazzetti/modalita` | SUB(1) + PUB(1) | emoncms mqtt | 0 | 2 | true | Dashboard Android App |
| `zara/domotics/palazzetti/oraavvio` | SUB(1) + PUB(1) | emoncms mqtt | 2 | true | Dashboard Android App |
| `zara/domotics/palazzetti/oraspegnimento` | SUB(1) + PUB(1) | emoncms mqtt | 2 | true | Dashboard Android App |

### Luci

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `/esp8266/lightSensor_1/#` | SUB(1) | domopi mqtt | 2 | — | Light Sensors |
| `LGtv/Toast/` | SUB(1) | domopi mqtt | 0 | — | broadlink lights |
| `LGtv/power/` | SUB(1) | domopi mqtt | 0 | — | broadlink lights |
| `LGtv/power/status` | SUB(1) + PUB(1) | domopi mqtt | 0 | — | broadlink lights |
| `cmnd/tasmota_86AD14/POWER` | PUB(1) | emoncms mqtt | — | true | Dashboard Android App |
| `emon/emontx3/power2` | SUB(3) | emoncms mqtt | 2 | — | Dashboard Android App | Google Webhook | broadlink lights |
| `shellies/shelly1-771284/relay/0` | SUB(4) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `shellies/shelly1-771284/relay/0/command` | PUB(1) | emoncms mqtt | — | true | Amazon Echo |
| `shellies/shelly1-98F4ABF294D7/relay/0` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `shellies/shelly1-98F4ABF294D7/relay/0/command` | PUB(1) | emoncms mqtt | — | true | Amazon Echo |
| `shellies/shelly1-B8B350/relay/0` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `shellies/shelly1-B8B350/relay/0/command` | PUB(1) | emoncms mqtt | — | true | Amazon Echo |
| `shellies/shelly1-B8C284/relay/0` | SUB(3) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `shellies/shelly1-B8C284/relay/0/command` | PUB(1) | emoncms mqtt | — | true | Amazon Echo |
| `shellies/shelly1-B92AF0/relay/0` | SUB(3) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `shellies/shelly1-B92AF0/relay/0/command` | PUB(1) | emoncms mqtt | — | true | Amazon Echo |
| `zara/domotics/lights/bedroomlight` | PUB(1) | domopi mqtt | — | true | broadlink lights |
| `zara/domotics/lights/livinglamp` | SUB(3) + PUB(1) | domopi mqtt | 2 | true | Android APP Bridge | Dashboard Android App | broadlink lights |
| `zara/domotics/lights/poolfloor` | SUB(3) + PUB(1) | domopi mqtt | 2 | true | Android APP Bridge | Dashboard Android App | broadlink lights |
| `zara/domotics/lights/poollight` | SUB(3) + PUB(1) | domopi mqtt | 2 | true | Android APP Bridge | Dashboard Android App | broadlink lights |
| `zara/domotics/lights/poolpump` | SUB(4) + PUB(1) | domopi mqtt | 2 | true | Android APP Bridge | Dashboard Android App | broadlink lights |
| `zara/domotics/lights/prolunga` | SUB(1) + PUB(1) | domopi mqtt | 2 | true | Dashboard Android App | broadlink lights |
| `zara/domotics/lights/readinglight` | SUB(2) + PUB(1) | domopi mqtt | 2 | true | Android APP Bridge | Dashboard Android App | broadlink lights |
| `zara/domotics/lights/shelflamp` | SUB(3) + PUB(1) | domopi mqtt | 2 | true | Android APP Bridge | Dashboard Android App | broadlink lights |
| `zara/domotics/lights/tvlamp` | SUB(3) + PUB(1) | domopi mqtt | 2 | true | Android APP Bridge | Dashboard Android App | broadlink lights |

### Piscina

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `zara/domotics/lights/poolskimmer` | SUB(4) + PUB(1) | domopi mqtt | 2 | true | Android APP Bridge | Dashboard Android App | broadlink lights |
| `zara/domotics/luciPiscinaAuto` | SUB(3) + PUB(3) | domopi mqtt | 0 | 2 | true | Android APP Bridge | Dashboard Android App |

### Presenza

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `GiuseppeHomePresence` | SUB(1) + PUB(2) | domopi mqtt | emoncms mqtt | 0 | 2 | true | OwnTracks | broadlink lights |
| `owntracks/#` | SUB(1) | domopi mqtt | 2 | — | OwnTracks |
| `owntracks/zaradomo/giuseppe/event` | SUB(1) | domopi mqtt | 2 | — | OwnTracks |

### Telecamere

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `emon/cameraMatrimoniale/humidex` | SUB(1) + PUB(1) | emoncms mqtt | 2 | — | Android APP Bridge | Dashboard Android App |
| `zigbee2mqtt/Sonoff AirGuard TH camera matrimoniale` | SUB(3) | domopi mqtt | emoncms mqtt | 2 | — | Android APP Bridge | ZigBee sensors |

### Comandi app

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `casa/clima/cmnd/+` | SUB(1) | domopi mqtt | 2 | — | AI climate |
| `casa/clima/cmnd/AI_climate_enabling` | SUB(3) + PUB(2) | domopi mqtt | 2 | — | AI climate | Android APP Bridge |
| `casa/clima/cmnd/deficit_tolerance_time` | SUB(1) | domopi mqtt | 1 | — | AI climate |
| `casa/clima/cmnd/grace_mode_solar` | SUB(1) | domopi mqtt | 1 | — | AI climate |
| `casa/clima/cmnd/min_off_time` | SUB(1) | domopi mqtt | 1 | — | AI climate |
| `casa/clima/cmnd/min_run_time` | SUB(1) | domopi mqtt | 1 | — | AI climate |
| `zara/android/domotica/#` | SUB(1) | domopi mqtt | 2 | — | Android APP Bridge |
| `zara/android/domotica/scene/set` | SUB(2) | domopi mqtt | 2 | — | Android APP Bridge |

### Diagnostica

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `casa/clima/log_eventi` | SUB(1) | domopi mqtt | 2 | — | AI climate |
| `emon/AC/HPstatus` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `zara/domotics/clima_log_eventi` | SUB(1) + PUB(1) | emoncms mqtt | 2 | — | AI climate |

### Alexa e voce

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `alexa/ac` | PUB(1) | emoncms mqtt | 0 | false | Amazon Echo |
| `alexa/caminetto` | SUB(1) + PUB(1) | emoncms mqtt | 0 | false | Amazon Echo | Android APP Bridge |
| `alexa/heatpump` | PUB(1) | emoncms mqtt | 0 | false | Amazon Echo |
| `alexa/resetCaminetto` | PUB(1) | emoncms mqtt | 0 | false | Amazon Echo |
| `alexa/vmc` | SUB(2) + PUB(2) | emoncms mqtt | 0 | 1 | false | AI climate | Amazon Echo | Android APP Bridge |

### Irrigazione

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `opensprinkler/#` | SUB(1) | domopi mqtt | 2 | — | opensprinkler relay |

### Altro / da classificare

| Topic | Direzione | Broker | QoS | Retain | Flow |
|---|---|---|---|---|---|
| `/esp8266/hitachiAC/command` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `cmnd/tasmotaFrigorifero/PowerOnState` | PUB(1) | domopi mqtt | — | — | mqtt to emoncms |
| `cmnd/tasmota_F32F4F/#` | SUB(1) | domopi mqtt | 2 | — | emoncms devices |
| `emon/bagnoServizio/Switch` | SUB(1) | emoncms mqtt | 2 | — | Dashboard Android App |
| `emon/tasmotaFrigorifero/power` | PUB(1) | emoncms mqtt | 2 | true | mqtt to emoncms |
| `emon/tasmotaFrigorifero/tasmotaCurrent` | PUB(1) | emoncms mqtt | 2 | true | mqtt to emoncms |
| `emon/tasmotaFrigorifero/tasmotaVoltage` | PUB(1) | emoncms mqtt | 2 | true | mqtt to emoncms |
| `homeassistant_voice` | SUB(1) | domopi mqtt | 2 | — | Dashboard Android App |
| `zara/domotics/ACAuto` | SUB(3) + PUB(3) | domopi mqtt | 0 | 2 | true | Android APP Bridge | Dashboard Android App |
| `zara/domotics/HP/abilitata` | SUB(1) + PUB(1) | emoncms mqtt | 2 | true | Dashboard Android App |
| `zara/domotics/HP/solardivertmode` | SUB(1) + PUB(1) | emoncms mqtt | 2 | true | Dashboard Android App |
| `zara/domotics/controlloAutomaticoPotenzaCaminetto` | SUB(1) + PUB(1) | emoncms mqtt | 0 | 2 | true | Dashboard Android App |
| `zara/domotics/livingThemostatMaxValue` | SUB(1) + PUB(1) | emoncms mqtt | 0 | 2 | true | Dashboard Android App |
| `zara/domotics/livingThemostatMinValue` | SUB(1) + PUB(1) | emoncms mqtt | 0 | 2 | true | Dashboard Android App |
| `zara/domotics/luciECO` | SUB(3) + PUB(3) | domopi mqtt | 0 | 2 | true | Android APP Bridge | Dashboard Android App |
| `zara/domotics/modalitavacanza` | SUB(3) + PUB(3) | domopi mqtt | 0 | 2 | true | Android APP Bridge | Dashboard Android App |
| `zara/domotics/pompapavimento/abilitata` | SUB(1) + PUB(1) | emoncms mqtt | 2 | true | Dashboard Android App |
| `zara/domotics/time_range` | PUB(1) | domopi mqtt | — | true | Android APP Bridge |
| `zigbee2mqtt/+` | SUB(2) | domopi mqtt | 1 | — | Android APP Bridge |
