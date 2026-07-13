# ADR-003 — Separazione tra AI e controllo fisico

- Stato: Accettato
- Data: 2026-07-13

## Decisione

La futura AI generativa non pubblicherà direttamente comandi hardware arbitrari.

Ogni comando dovrà essere:

1. interpretato;
2. trasformato in un'azione strutturata;
3. validato rispetto a schema, limiti e autorizzazioni;
4. eventualmente confermato dall'utente;
5. eseguito dal gateway o dal motore di regole.

## Motivazione

Ridurre il rischio di comandi errati o non sicuri.
