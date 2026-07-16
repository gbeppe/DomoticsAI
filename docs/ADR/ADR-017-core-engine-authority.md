# ADR-017 — Core Engine come fonte applicativa autorevole

- Stato: Accepted
- Data: 2026-07-16

## Contesto

Android può ricevere dati da REST, MQTT interno, Gateway e fallback.
Senza una gerarchia esplicita possono comparire valori incoerenti.

## Decisione

Il Core Engine e il suo Digital Twin rappresentano la fonte applicativa autorevole per Android.

Il broker reale e Node-RED rimangono autorevoli per il funzionamento fisico degli impianti.
Il Gateway importa e normalizza i loro stati nel Core Engine.

## Conseguenze

- Android preferisce gli endpoint del Core Engine.
- Il fallback MQTT deve essere chiaramente indicato.
- Knowledge Engine e Decision Engine lavorano sul Digital Twin normalizzato.
- Provenienza e timestamp devono essere conservati.
