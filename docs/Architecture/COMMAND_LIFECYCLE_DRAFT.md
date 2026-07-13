# Command Lifecycle — Draft v0.1

```mermaid
sequenceDiagram
    participant App as Android App
    participant Gateway as DomoticsAI Gateway
    participant Broker as MQTT Broker
    participant Prod as Node-RED Produzione
    participant Device as Dispositivo

    App->>Gateway: cmd/<domain>/<entity> + correlationId
    Gateway->>Gateway: valida schema, limiti e autorizzazione
    Gateway-->>App: ack accepted
    Gateway->>Broker: pubblica comando legacy
    Broker->>Prod: consegna comando
    Prod->>Device: esegue
    Device->>Broker: stato fisico
    Broker->>Gateway: telemetria confermata
    Gateway-->>App: state/<domain>/<entity>
    Gateway-->>App: command result = confirmed
```

## Stati comando

- `accepted`
- `rejected`
- `sent`
- `confirmed`
- `timeout`
- `failed`

## Campi minimi

```json
{
  "commandId": "uuid",
  "timestamp": "ISO-8601",
  "domain": "climate",
  "entity": "enabled",
  "requestedValue": true,
  "status": "accepted",
  "source": "android"
}
```
