# ADR-005 — Nessun Link node tra produzione e Gateway

- Stato: Accettato
- Data: 2026-07-13

## Decisione

Il nuovo progetto Node-RED Gateway non dipenderà da Link node del progetto di produzione.

## Motivazione

- disaccoppiamento;
- deploy indipendente;
- testabilità;
- rollback;
- maggiore chiarezza del contratto.
