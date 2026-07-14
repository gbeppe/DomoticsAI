# Energy Power Semantics

## Nuovi topic

```text
domoticsai/v1/state/energy/grid_power_w
domoticsai/v1/state/energy/battery_power_w
```

## Convenzioni da validare

### Rete

```text
positivo = importazione
negativo = esportazione
```

### Batteria

```text
positivo = scarica
negativo = carica
```

## Calcolo batteria

```text
battery = home_load - solar - grid
```

Il calcolo presuppone che `site_instant_power` sia positivo
durante l'importazione dalla rete.

Prima della dashboard Android definitiva, la convenzione
va verificata in un periodo noto di import e uno di export.
