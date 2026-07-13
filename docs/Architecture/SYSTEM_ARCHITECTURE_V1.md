# DomoticsAI — System Architecture v1

## 1. Obiettivo

Costruire una piattaforma domotica composta da:

- app Android nativa;
- Gateway Node-RED separato;
- protocollo MQTT stabile e versionato;
- logging strutturato;
- integrazione TinyCam;
- simulatore MQTT;
- futura AI generativa;
- futuro motore di regole IF–THEN–ELSE.

## 2. Principio fondamentale

Il progetto Node-RED di produzione resta invariato durante lo sviluppo iniziale.

```text
Android App
    |
    | MQTT
    v
DomoticsAI Gateway
    |
    | MQTT legacy / API esplicite
    v
Node-RED Produzione
    |
    v
Dispositivi reali
```

## 3. Componenti

### Android App

Responsabilità:

- UI moderna;
- connessione locale/remota automatica;
- visualizzazione realtime;
- invio comandi;
- configurazione;
- log;
- telecamere;
- cache locale;
- futura interfaccia AI.

### DomoticsAI Gateway

Responsabilità:

- adattamento topic legacy;
- namespace MQTT versionato;
- validazione payload;
- acknowledgment comandi;
- stato confermato;
- logging;
- audit;
- availability;
- simulazione;
- eventi strutturati;
- confine di sicurezza per AI.

### Node-RED Produzione

Responsabilità:

- controllo reale dispositivi;
- logiche attuali;
- automazioni esistenti;
- gestione clima;
- VMC;
- energia;
- sensori.

### MQTT Broker

Responsabilità:

- trasporto messaggi;
- retained state;
- QoS;
- disponibilità locale/remota.

### TinyCam

Responsabilità:

- live view HTTP;
- eventuali snapshot;
- eventuale PTZ;
- accesso locale/remoto.

## 4. Namespace target

```text
domoticsai/v1/state/...
domoticsai/v1/cmd/...
domoticsai/v1/config/...
domoticsai/v1/event/...
domoticsai/v1/availability/...
domoticsai/v1/log/...
domoticsai/v1/ack/...
```

## 5. Domini applicativi

```text
energy
climate
vmc
environment
thermostats
lights
thermal
pool
presence
cameras
system
rules
ai
```

## 6. Stato e comandi

Ogni comando deve avere:

- `commandId`;
- timestamp;
- source;
- entity;
- requested value;
- stato lifecycle;
- eventuale errore;
- stato fisico confermato.

## 7. Persistenza

### Android

- DataStore per preferenze;
- Room per log, cache e layout;
- Android Keystore per segreti.

### Gateway

- context persistente per configurazioni non sensibili;
- file o database per audit ed eventi;
- nessuna password nel flow JSON.

## 8. AI futura

La AI generativa non pubblica direttamente comandi hardware.

Flusso previsto:

```text
Utente
  -> Intent parser
  -> Knowledge Layer
  -> Action Schema
  -> Validation Layer
  -> Confirmation Policy
  -> Rule Engine / Gateway
  -> Audit Log
```

## 9. Motore regole

Le regole saranno rappresentate in JSON strutturato:

```json
{
  "id": "rule-001",
  "enabled": true,
  "name": "Disabilita clima quando assente",
  "when": {
    "all": [
      {
        "entity": "presence.home",
        "operator": "eq",
        "value": false
      }
    ]
  },
  "then": [
    {
      "action": "climate.enabled.set",
      "value": false
    }
  ],
  "else": []
}
```

## 10. Strategia di sviluppo

1. Gateway Core
2. Energy adapter
3. Climate adapter
4. VMC adapter
5. Android connection layer
6. Android Home MVP
7. TinyCam
8. Logs
9. Simulator
10. AI foundation
