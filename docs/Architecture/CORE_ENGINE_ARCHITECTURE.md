# Core Engine Architecture v0.1

Il Core Engine è un servizio Python indipendente.

## Responsabilità

- mantenere il Digital Twin;
- archiviare eventi;
- offrire REST e WebSocket;
- diventare la base per query, grafici, regole e AI.

## Sicurezza iniziale

- read-only;
- nessun endpoint comando;
- nessuna pubblicazione MQTT;
- nessun accesso diretto ai broker di produzione.
