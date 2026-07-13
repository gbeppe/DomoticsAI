# Dashboard Android App — Reverse Engineering v0.1

## Ambito

Analisi del tab Node-RED `Dashboard Android App` (`ab4429e1.433be8`).

## Dimensione

- Nodi complessivi: **357**
- Widget UI: **108**
- Function node: **78**
- MQTT input: **66**
- MQTT output: **25**
- Controlli configurabili: **65**
- Elementi di visualizzazione: **35**

## Tipi di widget

- `ui_switch`: 36
- `ui_gauge`: 22
- `ui_slider`: 9
- `ui_button`: 9
- `ui_spacer`: 6
- `ui_numeric`: 6
- `ui_text`: 6
- `ui_chart`: 4
- `ui_text_input`: 4
- `ui_template`: 3
- `ui_audio`: 1
- `ui_dropdown`: 1
- `ui_toast`: 1

## Ruolo del flow

Questo tab combina tre funzioni:

1. visualizzazione realtime;
2. comando diretto di dispositivi;
3. configurazione di parametri che modificano la logica Node-RED.

Non è quindi una dashboard puramente passiva: rappresenta una vera console operativa.

## Aree UI individuate

- **AI managed** — 1 widget — gruppi: AC / Heat Pump
- **Ambienti** — 13 widget — gruppi: Ambiente
- **Energia** — 5 widget — gruppi: Energia | Immissione Rete | Potenza Impegnata
- **Illuminazione** — 15 widget — gruppi: Illuminazione
- **Impianti Termici** — 29 widget — gruppi: Caldaia Gas | Immissione in Rete | Pompa Calore | Pompa Pavimento | Raffrescamento | Riserva Energia | Solare | Termo Focolare
- **Ingressi** — 3 widget — gruppi: Cancello garage
- **Piscina** — 4 widget — gruppi: Piscina
- **Senza tab** — 1 widget — gruppi: 
- **Settaggi** — 6 widget — gruppi: Automatismi
- **Termostati** — 28 widget — gruppi: Bagno Camera | Bagno Servizio | Living
- **VMC** — 2 widget — gruppi: VMC
- **Zooland Sys** — 1 widget — gruppi: hidden_group

## Funzioni da preservare nell'app Android

### Visualizzazione

- produzione FV;
- consumo casa;
- rete;
- Powerwall;
- temperature e umidità;
- stato climatizzatore;
- stato VMC;
- puffer, ACS e impianti termici;
- grafici storici;
- stato luci e dispositivi.

### Controllo

- luci;
- VMC;
- termostati;
- clima;
- modalità;
- relè e impianti collegati.

### Configurazione

- parametri AI clima;
- tempi minimi ON/OFF;
- soglie Humidex;
- limiti VMC;
- modalità grace;
- altri parametri persistenti.

## Criticità

### 1. UI e logica accoppiate

Molti widget inviano direttamente messaggi verso Function node, Link node o MQTT.
Nell'app Android la UI non dovrà conoscere la logica di traduzione hardware.

### 2. Stato non tipizzato

Valori numerici, booleani, stringhe `on/off` e oggetti JSON convivono senza un contratto unico.

### 3. Configurazioni senza lifecycle uniforme

Non tutti i controlli distinguono:

- valore richiesto;
- valore accettato;
- valore persistito;
- valore effettivamente applicato.

### 4. Grafici dipendenti dal flusso realtime

Alcuni grafici Node-RED mantengono uno storico limitato nel browser.
L'app richiederà un'origine dati storica stabile.

### 5. Layout rigido

L'attuale dashboard usa gruppi e ordine statico.
La nuova app dovrà supportare card riposizionabili e preferenze per dispositivo.

## Decisione architetturale

La nuova app non replicherà la struttura Node-RED 1:1.
Userà invece:

- schermate per dominio;
- card modulari;
- modello dati centralizzato;
- controlli con stato confermato;
- grafici alimentati da repository storico;
- layout salvabile;
- diagnostica separata.

## Priorità di migrazione UI

1. Home energia/clima;
2. parametri AI clima;
3. VMC;
4. sensori ambientali;
5. impianti termici;
6. luci;
7. piscina;
8. telecamere;
9. diagnostica e log.
