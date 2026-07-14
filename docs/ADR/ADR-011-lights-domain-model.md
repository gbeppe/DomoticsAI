# ADR-011 — Modello dominio Luci

- Stato: Accettato
- Data: 2026-07-14

## Decisione

Il Core Engine mantiene un registry tipizzato degli attuatori attivi
e calcola indicatori aggregati per area e tipo.

## Motivazioni

- escludere definitivamente dispositivi obsoleti;
- distinguere luci e relè piscina;
- semplificare Home, UI Luci e AI;
- rilevare dispositivi senza stato;
- centralizzare conteggi e disponibilità.
