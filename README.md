# DomoticsAI

Piattaforma domotica modulare composta da:

- gateway Node-RED separato dall'impianto di produzione;
- app Android nativa in Kotlin e Jetpack Compose;
- protocollo MQTT normalizzato;
- integrazione TinyCam;
- logging e diagnostica;
- futura modalità AI generativa e motore di regole IF–THEN–ELSE.

## Stato del progetto

Fase 1 — Reverse engineering e documentazione del sistema esistente.

## Principio di sicurezza

Il progetto Node-RED di produzione non viene modificato durante lo sviluppo del gateway e dell'app.  
Ogni nuova funzione deve essere testabile senza intervenire sui dispositivi reali.
