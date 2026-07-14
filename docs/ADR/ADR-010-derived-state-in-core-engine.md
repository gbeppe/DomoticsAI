# ADR-010 — Derived State nel Core Engine

- Stato: Accettato
- Data: 2026-07-14

Le interpretazioni e i calcoli di dominio vengono eseguiti nel Core Engine, non nell'app Android.

Motivazioni:

- unica fonte della verità;
- riuso da Android, web e AI;
- test indipendenti;
- UI più semplice;
- persistenza centralizzata.
