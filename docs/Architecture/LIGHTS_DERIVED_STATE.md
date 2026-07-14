# Lights Derived State v0.4

## Domini

```text
lights
lights_derived
```

`lights` contiene lo stato grezzo normalizzato dal Gateway.

`lights_derived` contiene:

```text
devices
lights_on_total
relays_on_total
unknown_total
internal_on
internal_total
external_on
external_total
pool_on
pool_total
any_internal_on
any_external_on
any_pool_on
all_available
```

## Registry logico

Il Core Engine conosce soltanto gli undici dispositivi attivi.

Sono esclusi:

```text
lampadaHifi
cucina
esterno
```

## Classificazione

```text
light:
  tavolinoLettura
  libreria
  sala
  televisione
  lavanderia
  ingressoServizio
  portico
  luciPiscina
  luciPedanaPiscina

relay:
  skimmerPiscina
  pompaPiscina
```

## Persistenza

Lo stato derivato viene salvato in SQLite e ripristinato all'avvio.
