# DomoticsAI — Protocollo applicativo

- Versione: `1.0.0-draft`
- Stato: `draft`
- Base topic predefinito: `zara/android/domotica`
- Base topic configurabile: sì

## Architettura

```text
Android → Core Engine → Gateway → Node-RED → impianti reali
```

L’app Android non comunica direttamente con il broker reale.

## Convenzione comando/stato

```text
${baseTopic}/<dominio>/set
${baseTopic}/<dominio>/state
```

`set` rappresenta una richiesta; `state` rappresenta lo stato reale confermato.

## Gestione climatica automatica

Comando:

```text
${baseTopic}/system/set
```

```json
{"automaticClimate":true,"origin":"android"}
```

Stato confermato:

```text
${baseTopic}/system/state
```

```json
{"automaticClimate":true,"mode":"AUTO","source":"node-red","updatedAt":"2026-07-16T15:30:01Z"}
```

`system/set` non deve essere retained.
`system/state` dovrebbe essere retained.

La UI mostra lo stato definitivo soltanto dopo la conferma su `system/state`.

## Compatibilità

I nuovi payload applicativi usano JSON UTF-8.
I payload scalari storici saranno supportati solo durante la migrazione.

## Sicurezza

- Il Gateway usa una allowlist dei topic pubblicabili.
- Le credenziali non devono essere versionate.
- Android non mostra password in chiaro.
