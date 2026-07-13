# Gateway Modules — Draft v0.1

## Tab Node-RED proposti

```text
00 Core
01 Availability
02 Energy
03 Climate
04 VMC
05 Environment Sensors
06 Thermostats
07 Lights
08 Thermal Systems
09 Pool
10 Presence
11 Cameras
12 Logs and Events
13 Rules
14 Simulator
```

## Core

- configurazione namespace;
- connessione broker;
- timestamp;
- validazione payload;
- correlation ID;
- error handling;
- audit log.

## Modulo di dominio

Ogni modulo deve avere:

- adapter input legacy;
- stato normalizzato;
- adapter comando;
- validazione;
- acknowledgment;
- timeout;
- test fixtures;
- documentazione dei mapping.

## Divieto architetturale

Il nuovo progetto Gateway non deve dipendere da Link node del progetto di produzione.
