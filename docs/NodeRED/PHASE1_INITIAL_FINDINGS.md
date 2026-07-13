# Fase 1 — Inventario iniziale

## Snapshot analizzato

- Nodi totali: **1599**
- Tab/flow: **28**
- Tab abilitati: **19**
- Tab disabilitati: **9**
- Function node: **266**
- MQTT input: **195**
- MQTT output: **95**
- MQTT output con topic dinamico: **10**
- Nodi individualmente disabilitati: **71**
- Broker MQTT configurati: **2**
- Topic statici unici configurati: **144**
- Riferimenti a variabili flow/global rilevati: **549**
- Variabili flow/global uniche rilevate: **78**

## Broker rilevati

- `domopi mqtt` — `192.168.1.20:1883` — TLS: `False`
- `emoncms mqtt` — `192.168.1.15:1883` — TLS: `False`

## Osservazioni immediate

- Il progetto usa due broker distinti; il Gateway dovrà normalizzare chiaramente la provenienza dei dati.
- Molti MQTT output usano `msg.topic`: la sola lettura del campo `topic` del nodo non è sufficiente. Per questo è stato creato anche `MQTT_TOPIC_LITERALS_IN_CODE.csv`.
- QoS 2 è molto diffuso nei dati sensore. Sarà valutato caso per caso, senza modificare la produzione.
- Sono presenti numerosi Function node: il reverse engineering dovrà classificare responsabilità, stato e side effect.

## Nomi di tab duplicati

- **Android APP Bridge**: `4dd176bbb0a9fd30` (disabilitato), `684cf25501f3e8a6` (abilitato)
- **ChatGPT**: `536c2447ed13d27b` (disabilitato), `acb2bb816d7b454b` (disabilitato)

## File prodotti

- `FLOW_INVENTORY.csv`
- `NODE_TYPE_COUNTS.csv`
- `MQTT_NODES.csv`
- `MQTT_STATIC_TOPICS.csv`
- `MQTT_TOPIC_LITERALS_IN_CODE.csv`
- `CONTEXT_VARIABLE_USAGE.csv`
- `CONTEXT_VARIABLE_SUMMARY.csv`

## Limiti dell'estrazione automatica

I topic costruiti concatenando variabili o template possono richiedere revisione manuale.
Anche i payload e i tipi devono essere inferiti dalla logica dei nodi e poi verificati sul broker o in simulazione.
