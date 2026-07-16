# ADR-016 — La UI rappresenta lo stato confermato

- Stato: Accepted
- Data: 2026-07-16

## Contesto

Aggiornare definitivamente uno switch subito dopo il tocco può creare una rappresentazione falsa dello stato dell’impianto.

## Decisione

La posizione autorevole di un controllo deriva dallo stato confermato della casa.

Dopo una richiesta, la UI può mostrare temporaneamente uno stato pending, ma non deve considerare il comando concluso prima della conferma.

## Conseguenze

- Sono necessari stati pending, errore e timeout.
- Il controllo torna allo stato reale se la conferma non arriva.
- L’utente può distinguere chiaramente richiesta e risultato.
