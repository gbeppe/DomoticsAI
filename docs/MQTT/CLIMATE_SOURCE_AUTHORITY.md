'MD'
# DomoticsAI — Climate Source Authority

## Stato

La canary per la promozione della sorgente Climate è stata completata
con esito positivo.

## Sorgente primaria

I seguenti dati sono alimentati dal contratto MQTT applicativo:

| Dato | Topic sorgente | Topic DomoticsAI |
|---|---|---|
| Temperatura living | `env/tempLiving` | `state/climate/living_temperature_c` |
| Humidex living | `env/humidexLiving` | `state/climate/living_humidex` |
| Humidex camera | `env/humidexBedroom` | `state/climate/bedroom_humidex` |
| Velocità VMC | `vmc/speed/state` | `state/vmc/speed` |

Il prefisso applicativo predefinito è:

```text
zara/android/domotica
