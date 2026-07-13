# Android APP Bridge — Reverse Engineering v0.1

## Ambito

Analisi del tab attivo `Android APP Bridge` (`684cf25501f3e8a6`).

Nel progetto è presente anche un tab omonimo disabilitato. Questo documento riguarda esclusivamente la versione attiva.

## Dimensione

- Nodi complessivi: **99**
- Function node: **18**
- MQTT input: **43**
- MQTT output: **13**
- MQTT output con topic dinamico: **5**
- Link input: **2**
- Link output: **16**
- Nodi disabilitati: **3**

## Ruolo architetturale

Questo flow svolge già molte funzioni tipiche del futuro Gateway:

1. riceve comandi dall'app;
2. normalizza valori e nomi dei dispositivi;
3. traduce i comandi verso topic hardware o Link node;
4. ascolta lo stato reale dei dispositivi;
5. ripubblica stati normalizzati e retained verso l'app;
6. aggrega telemetrie energetiche;
7. espone termostati, VMC, luci e altri domini.

È quindi una base preziosa, ma non ancora una specifica stabile.

## Namespace attuale dell'app

Il prefisso predefinito rilevato è:

```text
zara/android/domotica
```

Il codice usa anche:

```javascript
global.get("app_base_topic") || "zara/android/domotica"
```

Questo rende il prefisso configurabile, ma la configurazione è distribuita nel context globale.

## Pattern individuati

### Stato

```text
zara/android/domotica/<domain>/<entity>/state
```

### Comando

```text
zara/android/domotica/<domain>/<entity>/set
```

### Termostati

```text
zara/android/domotica/thermostat/<room>/target/set
zara/android/domotica/thermostat/<room>/target/state
```

### VMC

```text
zara/android/domotica/vmc/speed/set
zara/android/domotica/vmc/speed/state
```

## Domini già presenti

- Luci
- Termostati
- VMC
- Energia
- Puffer / ACS
- Stufa / caminetto
- Clima
- Piscina e relè collegati

## Punti di forza

- separazione parziale tra topic app e topic hardware;
- normalizzazione dei payload;
- retained state verso l'app;
- uso di router centralizzati;
- supporto a dispositivi controllati tramite Link node;
- prefisso app configurabile.

## Criticità

### 1. Flow già molto esteso

Il Bridge contiene numerosi domini e responsabilità. Nel nuovo Gateway conviene suddividerli in subflow o tab dedicati.

### 2. Dipendenza da Link node del progetto di produzione

Molti comandi non vengono pubblicati direttamente via MQTT ma passano attraverso Link node.
Questo rende il Bridge dipendente dalla struttura interna del progetto corrente.

Il nuovo progetto Node-RED separato non potrà usare direttamente quei Link node.
Dovrà comunicare esclusivamente tramite MQTT o API esplicite.

### 3. Namespace non versionato

`zara/android/domotica` non include una versione del contratto.
Per DomoticsAI proponiamo `domoticsai/v1`.

### 4. Payload non uniformi

Sono presenti stringhe, numeri, booleani e oggetti JSON.
L'app richiederà un contratto di tipo e unità per ogni entità.

### 5. Conferma comando non sempre esplicita

Alcuni comandi producono immediatamente uno stato locale, altri aspettano la telemetria hardware.
Nel nuovo Gateway distingueremo:

- comando richiesto;
- acknowledgment;
- stato fisico confermato;
- timeout o errore.

### 6. Sicurezza e autorizzazioni

Il Bridge non implementa ancora un modello esplicito di autorizzazioni o validazione centralizzata.
Questo sarà necessario per la futura AI generativa.

## Decisione proposta

Non evolvere direttamente questo flow come base definitiva.

Usarlo invece come:

- sorgente di mapping;
- catalogo dei dispositivi;
- riferimento per payload e topic reali;
- base per test di compatibilità.

Il nuovo Gateway verrà costruito separatamente e in modo modulare.
