# Test LIVE_READ_ONLY

```bash
cd /home/giuseppe/AndroidStudioProjects/DomoticsAI/gateway
npm start
```

Monitor:

```bash
mosquitto_sub -h 127.0.0.1 -p 1883 -t 'domoticsai/v1/#' -v
```

Attesi:

```text
domoticsai/v1/availability/production_mqtt_20
domoticsai/v1/availability/production_mqtt_15
domoticsai/v1/state/energy/solar_power_w
domoticsai/v1/state/energy/home_load_w
domoticsai/v1/state/energy/powerwall_soc_pct
domoticsai/v1/state/climate/living_temperature_c
domoticsai/v1/state/climate/living_humidex
domoticsai/v1/state/climate/bedroom_humidex
domoticsai/v1/state/climate/ac_power_w
domoticsai/v1/state/vmc/speed
```

Il Gateway resta sul PC `192.168.1.40`.
Il Raspberry `192.168.1.20` resta invariato.
