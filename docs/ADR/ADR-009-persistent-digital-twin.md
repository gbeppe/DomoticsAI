# ADR-009 — Persistenza del Digital Twin su SQLite

- Stato: Accettato
- Data: 2026-07-14

## Decisione

Persistenza dell'ultimo valore noto di ogni entità nella tabella SQLite `twin_state`.

## Motivazioni

- API disponibili immediatamente dopo il riavvio;
- maggiore resilienza;
- preparazione per grafici, regole e AI;
- indipendenza dai retained MQTT.

## Conseguenze

- SQLite diventa parte dello stato runtime;
- il database non viene versionato;
- occorrono backup e migrazioni nelle versioni future.
