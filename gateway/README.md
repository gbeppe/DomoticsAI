# DomoticsAI Node-RED Gateway v0.2.0

Modalità `LIVE_READ_ONLY`.

Broker:
- `127.0.0.1:1883`: test DomoticsAI, lettura/scrittura;
- `192.168.1.20:1883`: produzione, solo MQTT input;
- `192.168.1.15:1883`: EmonCMS, solo MQTT input.

Tutti i nodi MQTT output puntano esclusivamente al broker locale di test.
