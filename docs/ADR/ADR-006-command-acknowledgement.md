# ADR-006 — Acknowledgment esplicito dei comandi

- Stato: Accettato
- Data: 2026-07-13

## Decisione

Ogni comando dell'app avrà un `commandId` e un lifecycle esplicito.

## Stati

```text
accepted
rejected
sent
confirmed
timeout
failed
```

## Motivazione

L'utente deve sapere se un comando è stato soltanto inviato o realmente confermato.
