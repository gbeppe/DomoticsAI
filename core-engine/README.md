# DomoticsAI Core Engine v0.1.0

Servizio backend indipendente per Digital Twin, storico ed evoluzione AI.

## Funzioni

- sottoscrizione MQTT a `domoticsai/v1/#`;
- Digital Twin in memoria;
- storico eventi SQLite;
- API REST;
- WebSocket realtime;
- modalità read-only.

## Endpoint

```text
GET /health
GET /api/v1/twin
GET /api/v1/twin/{domain}
GET /api/v1/events?limit=100
WS  /ws/twin
```

## Porta

```text
192.168.1.40:8090
```
