# Android APP Bridge — Migration Matrix Draft

| Area | Implementazione attuale | Implementazione target |
|---|---|---|
| Prefisso MQTT | `zara/android/domotica` | `domoticsai/v1` |
| Connessione alla produzione | MQTT + Link node | solo MQTT/API esplicite |
| Stato | topic retained non uniformi | stato retained tipizzato |
| Comandi | `/set` con payload eterogenei | comandi validati con schema |
| Conferma | implicita o dipendente dal device | ack + stato confermato |
| Logging | debug Node-RED | audit log strutturato |
| Sicurezza | credenziali broker | ruoli, policy e limiti azione |
| AI futura | non prevista formalmente | action schema + validation layer |
| Test | principalmente live | simulatore MQTT e test replay |
| Versionamento | assente | namespace `/v1/` |

## Strategia

1. documentare tutti i mapping esistenti;
2. creare topic adapter nel Gateway;
3. simulare input e output;
4. verificare compatibilità con il sistema reale;
5. collegare l'app soltanto al namespace DomoticsAI;
6. mantenere il Bridge attuale invariato durante la transizione.
