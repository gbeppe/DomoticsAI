# Android APP Bridge — Compatibility Test Plan

## Obiettivo

Verificare che il nuovo Gateway produca gli stessi effetti del Bridge attuale senza usare Link node interni.

## Test minimi

### Luci

- ON/OFF per ogni dispositivo;
- normalizzazione `true/false`, `1/0`, `ON/OFF`;
- stato retained;
- conferma da telemetria reale.

### Termostati

- setpoint living;
- setpoint bagno;
- valori decimali;
- limiti minimi e massimi;
- stato target confermato.

### VMC

- velocità 1–4;
- rifiuto valori fuori intervallo;
- stato velocità confermato.

### Energia

- produzione FV;
- consumo casa;
- SOC Powerwall;
- filtro anti-rimbalzo;
- unità e segno.

### Clima

- stato aggregato;
- parametri AI;
- comando enable/disable;
- timeout e stato non confermato.

### Stufa e impianti termici

- acceso/spento;
- potenza;
- temperature puffer/ACS;
- modalità.

## Metodo

- replay di messaggi MQTT registrati;
- broker di test;
- confronto tra output Bridge attuale e nuovo Gateway;
- nessun comando a dispositivi reali durante i test automatici.
