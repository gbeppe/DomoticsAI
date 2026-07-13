# DomoticsAI Node-RED Gateway

Versione iniziale sicura del Gateway Node-RED separato.

## Sicurezza

Questa versione:

- usa `127.0.0.1:1883` come broker predefinito;
- parte in modalità `SIMULATION`;
- non inoltra comandi al sistema legacy;
- non usa Link node del progetto di produzione;
- pubblica soltanto nel namespace `domoticsai/v1`.

## Flow inclusi

- `00 Core`
- `01 Availability`
- `02 Energy`
- `03 Climate`
- `04 VMC`
- `05 Logs`
- `06 Simulator`

## Avvio

```bash
npm install
npm start
```

Editor Node-RED:

```text
http://localhost:1881
```

## Broker MQTT

Per i primi test usa un broker locale sulla stessa macchina:

```bash
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto
```

Test:

```bash
mosquitto_sub -h 127.0.0.1 -t 'domoticsai/v1/#' -v
```

## Importazione alternativa

Puoi importare `flows.json` in un'istanza Node-RED separata.

## Passaggio successivo

Dopo i test in simulazione configureremo un secondo broker connection node in sola lettura verso il broker reale.
I comandi legacy resteranno bloccati fino all'approvazione esplicita.
