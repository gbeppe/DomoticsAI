# Logging Architecture

## Tipi di log

### Connection Log

- tentativo connessione;
- endpoint selezionato;
- connect/disconnect;
- reconnect;
- timeout;
- errore autenticazione.

### MQTT RX/TX Log

- timestamp;
- direzione;
- topic;
- payload sintetico;
- QoS;
- retain;
- endpoint;
- correlation ID.

### Command Audit

- utente/source;
- comando;
- valore;
- stato precedente;
- stato richiesto;
- risultato;
- conferma;
- errore.

### AI Decision Event

- azione;
- reason codes;
- metriche rilevanti;
- soglie;
- stato precedente;
- stato successivo.

## Retention

### Android

- log tecnico locale limitato;
- rotazione per dimensione;
- filtro e ricerca;
- export futuro.

### Gateway

- audit persistente;
- eventi strutturati;
- rotazione giornaliera o database.

## Privacy

Le password e i token non devono mai comparire nei log.
