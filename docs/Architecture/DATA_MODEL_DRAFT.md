# Data Model — Draft v0.1

## EnergyState

```json
{
  "solarPowerW": 0,
  "homeLoadW": 0,
  "gridPowerW": 0,
  "powerwallSocPct": 0,
  "batteryPowerW": 0,
  "updatedAt": ""
}
```

## ClimateState

```json
{
  "enabled": true,
  "season": "SUMMER",
  "mode": "OFF",
  "livingTemperatureC": 0,
  "bedroomTemperatureC": 0,
  "outdoorTemperatureC": 0,
  "livingHumidityPct": 0,
  "bedroomHumidityPct": 0,
  "livingHumidex": 0,
  "bedroomHumidex": 0,
  "setpointC": 0,
  "acPowerW": 0,
  "decisionReason": "",
  "updatedAt": ""
}
```

## VmcState

```json
{
  "speed": 1,
  "reason": "BASE_AIR_EXCHANGE",
  "manualOverride": false,
  "updatedAt": ""
}
```

## ClimateConfiguration

```json
{
  "minRunMinutes": 15,
  "minOffMinutes": 15,
  "targetHumidexSummer": 29,
  "maxVmcNight": 2,
  "deficitToleranceMinutes": 10,
  "emergencyHumidexAway": 33,
  "gracePeriod": {
    "startHour": 8,
    "endHour": 16,
    "solarOnly": false
  }
}
```

## ConnectionProfile

```json
{
  "mode": "AUTO",
  "mqttLocal": {
    "host": "192.168.1.20",
    "port": 1883
  },
  "mqttRemote": {
    "host": "",
    "port": 1883
  },
  "tinyCamLocal": {
    "host": "",
    "port": 8083
  },
  "tinyCamRemote": {
    "host": "",
    "port": 8083
  }
}
```

## EventRecord

```json
{
  "id": "",
  "timestamp": "",
  "domain": "CLIMATE",
  "severity": "INFO",
  "action": "AC_ON",
  "reasonCodes": [],
  "metrics": {},
  "source": "gateway"
}
```

## RuleDefinition

```json
{
  "id": "",
  "enabled": true,
  "name": "",
  "when": {
    "all": []
  },
  "then": [],
  "else": []
}
```
