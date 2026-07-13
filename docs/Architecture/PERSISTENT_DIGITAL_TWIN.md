# Persistent Digital Twin v0.2

## Obiettivo

Mantenere l'ultimo stato noto della casa anche dopo il riavvio del Core Engine.

## Tabelle SQLite

### `mqtt_events`

Storico append-only degli aggiornamenti ricevuti.

### `twin_state`

Una riga per ogni coppia:

```text
domain + entity
```

Contiene:

- valore;
- unità;
- qualità;
- sorgente;
- timestamp;
- topic.

## Avvio

All'avvio il Core Engine:

1. apre SQLite;
2. carica `twin_state`;
3. ricostruisce il Digital Twin;
4. espone immediatamente le API;
5. aggiorna progressivamente i valori con MQTT.

## Proprietà

- aggiornamento atomico tramite UPSERT;
- nessuna dipendenza dai retained MQTT per il ripristino;
- storico eventi preservato;
- database escluso da Git.
