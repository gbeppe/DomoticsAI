# System Architecture

## Obiettivo

Descrivere l'architettura corrente e quella target di DomoticsAI.

## Architettura target

```text
Android App
    |
    | MQTT
    v
Node-RED Gateway separato
    |
    | MQTT
    v
Node-RED di produzione
    |
    v
Dispositivi reali
```

## Componenti previsti

- App Android
- Gateway Node-RED
- Broker MQTT
- TinyCam Web Server
- Event log
- Simulatore MQTT
- Knowledge Layer per AI generativa
- Motore di regole IF–THEN–ELSE
