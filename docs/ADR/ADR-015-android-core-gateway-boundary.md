# ADR-015 — Android non accede direttamente al broker reale

- Stato: Accepted
- Data: 2026-07-16

## Contesto

Il broker reale contiene dettagli specifici di Node-RED e degli impianti.
Collegare direttamente Android renderebbe l’app dipendente dall’implementazione fisica della casa.

## Decisione

Android comunica con il Core Engine e con il protocollo interno DomoticsAI.

Soltanto il Gateway traduce fra:

```text
domoticsai/v1/...
```

e:

```text
zara/android/domotica/...
```

Il prefisso di produzione è configurabile nel Gateway.

## Conseguenze

- Android resta indipendente dai topic fisici.
- Il Gateway applica allowlist, mapping e protezioni.
- Il Core Engine mantiene Digital Twin, storico e Command Store.
- Un cambio dei topic Node-RED non richiede necessariamente una nuova app.
