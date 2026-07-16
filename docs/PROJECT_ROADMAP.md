# DomoticsAI — Project Roadmap

- Versione roadmap: `2.0`
- Aggiornata: `2026-07-16`
- Stato corrente: `Sprint 11.5A`

## Visione

DomoticsAI è una piattaforma locale e self-hosted per osservare, comprendere e controllare la casa.

Lo stack deve funzionare senza cloud obbligatorio, licenze commerciali o abbonamenti.

Componenti principali:

- App Android
- Core Engine
- Digital Twin persistente
- Gateway Node-RED separato
- Broker MQTT locale e broker di produzione
- Protocollo MQTT applicativo versionato
- Knowledge Engine e Decision Engine

## Stato sintetico

| Area | Stato |
|---|---|
| Fondazioni architetturali | Completate |
| Core Engine e Digital Twin | Operativi |
| Energy e Climate read-only | Operativi con dati reali |
| Protocollo MQTT e ADR | Definiti |
| Comandi reali verso la casa | Da avviare in Sprint 12 |
| AI generativa domestica | Fase futura |

## Fase 1 — Fondazioni

Stato: `COMPLETATA`

- Analisi del progetto Node-RED esistente
- Architettura Gateway / Core Engine / Android
- Gateway separato dal Node-RED di produzione
- Digital Twin persistente
- Command Manager e storico comandi
- Knowledge Engine e Decision Engine
- Pipeline Energy
- Pipeline Lights
- Pipeline Climate con dati reali
- Endpoint REST aggregati
- Protocollo MQTT applicativo
- Architecture Decision Records
- Validatore del contratto e dei capture MQTT

## Sprint 11 — Consolidamento e contratto di produzione

### Sprint 11.3

- Ingestione Climate dal namespace applicativo
- Confronto con le sorgenti legacy
- Promozione controllata della sorgente Climate primaria
- Endpoint `/api/v1/climate`
- Pipeline Android Climate
- Dati Climate reali nella Home

### Sprint 11.4A

- Protocollo ufficiale `DOMOTICSAI_PROTOCOL.md`
- Coppia `set/state` per comandi e stato confermato
- Nuovi payload applicativi JSON
- Contratto `system/set` e `system/state`
- ADR-013 — ADR-017

### Sprint 11.4B

- Compatibilità temporanea con payload legacy
- Classificazione `compatible / legacy-compatible / incompatible`
- Report e test del validatore MQTT

### Sprint 11.5

Stato: `COMPLETATA`

Deliverable:

- roadmap delle fasi future approvata
- convenzione dei tag Git definita
- criteri di chiusura delle Sprint di produzione definiti
- architettura congelata prima dei comandi reali

### Sprint 11.5A

Stato: `IN CORSO`

Deliverable:

- creazione di questo documento
- collegamento della roadmap al Project Index
- tag della milestone di fine fondazioni

## Fase 2 — Integrazione con la casa

### Sprint 12.0 — Gateway Production Bridge

Obiettivo: validare il percorso completo e sicuro dei comandi.

```text
Android
  → Core Engine
  → Gateway
  → zara/android/domotica/...
  → broker 192.168.1.20
  → Node-RED
  → dispositivo reale
```

Vincoli:

- Android non accede direttamente al broker reale
- il Gateway usa allowlist esplicite
- ogni comando viene registrato
- ogni azione richiede uno stato di conferma
- il sistema di produzione esistente resta operativo durante la migrazione

### Sprint 12.1 — Luci reali

- comando singolo dispositivo
- stato confermato
- scene
- ACK e timeout
- prima luce reale comandata end-to-end

### Sprint 12.2 — Climate reale

- switch gestione climatica automatica
- `system/set` con payload JSON
- `system/state` retained
- termostati
- VMC
- climatizzatore / pompa di calore
- caminetto e impianto termico

### Sprint 12.3 — Stato applicazione e diagnostica

- indicatori Wi-Fi / rete mobile
- stato broker MQTT
- stato Core Engine
- contatori messaggi RX/TX
- pannello espandibile con swipe
- host, porta, prefisso e credenziali mascherate
- log recente

### Sprint 12.4 — Telecamere

- TinyCam locale e remoto
- selezione automatica endpoint
- live stream e fullscreen

### Sprint 12.5 — Energy completa

- fotovoltaico
- consumi casa
- Powerwall
- rete elettrica
- storico e grafici

## Fase 3 — Domotica completa

- cancelli e ingressi
- impianti termici
- sensori temperatura e umidità
- humidex
- piscina
- sicurezza e allarmi
- automazioni e parametri avanzati

## Fase 4 — Assistente domestico AI

- domande in linguaggio naturale
- spiegazioni basate sul Digital Twin
- grafici generati dai dati storici
- suggerimenti consultivi
- comandi condizionali IF / THEN / ELSE
- esecuzione controllata con conferma e audit

## Decisioni permanenti

- Android non comunica direttamente con il broker reale.
- Il Gateway è l’unico bridge verso Node-RED di produzione.
- Il prefisso applicativo è configurabile; il valore predefinito è `zara/android/domotica`.
- I nuovi comandi e stati usano payload JSON.
- `.../set` esprime una richiesta; `.../state` esprime lo stato reale confermato.
- La UI non considera concluso un comando prima della conferma.
- Il Core Engine è la fonte applicativa autorevole per Android.
- Node-RED e il broker reale restano autorevoli per il funzionamento fisico degli impianti.
- Ogni modifica del protocollo richiede aggiornamento di documentazione, contratto e test.
- Tutto lo stack deve essere locale, gratuito e privo di abbonamenti obbligatori.

## Criteri di chiusura delle Sprint di produzione

Ogni Sprint 12.x e successiva deve superare:

1. test funzionale
2. controllo di sicurezza
3. test di regressione
4. aggiornamento documentale
5. verifica del rollback
6. commit e tag Git

## Convenzione dei tag Git

Tag di inizio e fine Sprint:

```text
s12.0-start
s12.0-end
s12.1-start
s12.1-end
```

Milestone principali:

```text
m1-foundation-complete
m2-production-bridge
m3-first-real-device
m4-ai-foundation
```

## Prossimo passo

Completare Sprint 11.5A e aprire Sprint 12.0 — Gateway Production Bridge.
