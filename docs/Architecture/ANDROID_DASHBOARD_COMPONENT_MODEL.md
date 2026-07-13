# Android Dashboard Component Model Draft

## Card types

### EnergyDialCard

Campi:

```json
{
  "id": "solar-production",
  "title": "Produzione FV",
  "value": 2800,
  "unit": "W",
  "min": 0,
  "max": 6000,
  "status": "GOOD"
}
```

### BatteryBarCard

```json
{
  "id": "powerwall-soc",
  "title": "Powerwall",
  "percentage": 84,
  "powerW": -1200,
  "status": "CHARGING"
}
```

### ClimateStatusCard

```json
{
  "id": "climate-main",
  "mode": "COOLING_ON",
  "temperatureC": 24.2,
  "humidex": 30.1,
  "setpointC": 23,
  "reason": "SURPLUS_SOLAR"
}
```

### SensorCard

```json
{
  "id": "living-temperature",
  "title": "Living",
  "primary": 24.2,
  "secondary": 52,
  "primaryUnit": "°C",
  "secondaryUnit": "%"
}
```

### ActionCard

```json
{
  "id": "vmc-speed",
  "title": "VMC",
  "value": 2,
  "allowedValues": [1,2,3,4],
  "confirmationRequired": false
}
```

## Layout

Ogni card avrà:

- posizione;
- larghezza;
- altezza;
- visibilità;
- ordine;
- modalità compatta/estesa.

Le preferenze saranno salvate localmente con Room/DataStore.
