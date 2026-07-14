# Lights Command Path v1

```text
Android
  ↓ REST
Core Engine
  ↓ MQTT locale, non retained
domoticsai/v1/cmd/lights/<area>/<deviceId>
  ↓
Gateway simulator
  ↓
domoticsai/v1/ack/lights/<area>/<deviceId>/<requestId>
```

Sicurezza:

- allowlist degli 11 dispositivi attivi;
- ON/OFF tipizzati;
- request ID univoco;
- scadenza comando;
- messaggi non retained;
- prefissi MQTT consentiti;
- simulazione obbligatoria;
- nessun output verso produzione.

Stati:

```text
accepted
rejected
simulated
confirmed
timeout
failed
```
