# ADR-014 — JSON per i nuovi payload applicativi

- Stato: Accepted
- Data: 2026-07-16

## Contesto

I payload booleani o scalari non consentono facilmente di aggiungere origine, timestamp, requestId e altri metadati.

## Decisione

Tutti i nuovi comandi e stati applicativi usano JSON UTF-8.

Esempio:

```json
{"automaticClimate":true,"origin":"android","requestId":"uuid"}
```

## Conseguenze

- I parser devono validare tipi e campi obbligatori.
- I componenti devono ignorare campi opzionali sconosciuti.
- I payload scalari storici restano solo durante la migrazione.
- Le modifiche seguono il versionamento del protocollo.
