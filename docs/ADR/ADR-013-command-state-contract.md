# ADR-013 — Separazione fra comando e stato

- Stato: Accepted
- Data: 2026-07-16

## Contesto

Un controllo grafico può mostrare come conclusa un’azione che l’impianto non ha ancora ricevuto o applicato.

## Decisione

Ogni nuova funzione comandabile usa due canali distinti:

```text
.../set
.../state
```

`set` esprime una richiesta.
`state` comunica lo stato reale osservato e confermato.

## Conseguenze

- La UI deve prevedere uno stato di attesa.
- Il sistema deve gestire timeout ed errori.
- Node-RED deve pubblicare lo stato dopo l’applicazione.
- Il Command Manager deve correlare richiesta e conferma quando possibile.
