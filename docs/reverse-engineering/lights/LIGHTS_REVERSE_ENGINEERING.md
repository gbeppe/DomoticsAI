# Reverse engineering — Luci e scenari

Flow analizzato: `/home/giuseppe/AndroidStudioProjects/DomoticsAI/gateway/flows.json`

Nodi rilevanti: **0**
Topic espliciti rilevati: **0**

## Topic MQTT e riferimenti

Nessun topic esplicito rilevato automaticamente.

## Classificazione da completare

| ID logico | Nome UI | Area | Tipo | Topic stato | Topic comando | Dimmer | Note |
|---|---|---|---|---|---|---|---|
| | | interno/esterno/piscina | luce/scenario/gruppo | | | sì/no | |

## Domande funzionali

- Lo stato pubblicato rappresenta il comando o la conferma reale?
- Esistono luci dimmerabili o RGB?
- Quali scenari sono mutuamente esclusivi?
- Gli scenari modificano anche clima, piscina o ingressi?
- Quali comandi richiedono conferma o timeout?
- Esistono automazioni orarie o crepuscolari?
