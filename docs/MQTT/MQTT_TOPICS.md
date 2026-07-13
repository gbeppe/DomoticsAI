# Catalogo topic MQTT

Il catalogo sarà generato dal reverse engineering dei flow Node-RED.

| Topic | Direzione | Payload | Retain | QoS | Modulo | Descrizione |
|---|---|---|---:|---:|---|---|
| `casa/clima/stato_completo` | Node-RED → App/Gateway | JSON | Da verificare | Da verificare | Clima | Stato aggregato clima e VMC |
| `TeslaPowerwall/SOE` | Powerwall → Node-RED | Numero | Da verificare | 2 nel flow | Energia | Stato di carica batteria |
| `TeslaPowerwall/solar_instant_power` | Powerwall → Node-RED | Numero W | Da verificare | 2 nel flow | Energia | Produzione FV |
| `TeslaPowerwall/load_instant_power` | Powerwall → Node-RED | Numero W | Da verificare | 2 nel flow | Energia | Consumo casa |
