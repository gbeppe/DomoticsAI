# Energy Derived State v0.3

Il Digital Twin mantiene:

```text
energy
energy_derived
```

`energy` contiene valori grezzi provenienti dal Gateway.

`energy_derived` contiene:

```text
grid_direction
battery_direction
grid_import_w
grid_export_w
battery_charge_w
battery_discharge_w
self_consumption_pct
self_sufficiency_pct
balance_error_w
operating_mode
is_grid_importing
is_grid_exporting
is_battery_charging
is_battery_discharging
```

Convenzioni:

```text
grid positivo = import
grid negativo = export
battery positivo = scarica
battery negativo = carica
```

Bilancio atteso:

```text
solar + grid + battery = home_load
```
