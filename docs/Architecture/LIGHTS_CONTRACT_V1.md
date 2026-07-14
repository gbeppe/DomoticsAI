# Lights Contract v1

## Dispositivi attivi

Interno:

```text
tavolinoLettura
libreria
sala
televisione
lavanderia
ingressoServizio
```

Esterno:

```text
portico
```

Piscina:

```text
luciPiscina
luciPedanaPiscina
skimmerPiscina
pompaPiscina
```

`skimmerPiscina` e `pompaPiscina` sono `relay`.

## Dispositivi esclusi

```text
lampadaHifi
cucina
esterno
```

## Topic legacy di stato

```text
zara/android/domotica/light/<deviceId>/state
```

## Topic normalizzato

```text
domoticsai/v1/state/lights/<area>/<deviceId>
```

## Registry

```text
domoticsai/v1/meta/lights/registry
```

## Scene supportate

```text
ALL_ON
ALL_OFF
TV_MODE
SLEEP_MODE
```

Topic legacy scene:

```text
zara/android/domotica/scene/set
```

La fase v0.1 è read-only.
