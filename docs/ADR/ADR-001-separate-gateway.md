# ADR-001 — Gateway Node-RED separato

- Stato: Accettato
- Data: 2026-07-13

## Contesto

Il progetto Node-RED attuale controlla dispositivi reali ed è già operativo.

## Decisione

Creare un progetto Node-RED separato dedicato a:

- normalizzazione dei topic;
- interfaccia verso l'app;
- logging;
- diagnostica;
- simulazione;
- futura integrazione AI.

## Conseguenze

- Il sistema di produzione resta invariato.
- Il gateway può essere arrestato senza compromettere la casa.
- I test diventano più sicuri e ripetibili.
