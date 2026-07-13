# Test iniziali

## 1. Avviare Mosquitto

```bash
sudo systemctl status mosquitto
```

## 2. Ascoltare il namespace

```bash
mosquitto_sub -h 127.0.0.1 -t 'domoticsai/v1/#' -v
```

## 3. Avviare il Gateway

```bash
npm start
```

## 4. Risultati attesi

Entro pochi secondi devono comparire:

```text
domoticsai/v1/availability/gateway
domoticsai/v1/state/energy/solar_power_w
domoticsai/v1/state/energy/home_load_w
domoticsai/v1/state/energy/powerwall_soc_pct
domoticsai/v1/state/climate/living_temperature_c
domoticsai/v1/state/climate/living_humidex
domoticsai/v1/state/vmc/speed
```

## 5. Test comando simulato

```bash
mosquitto_pub -h 127.0.0.1   -t 'domoticsai/v1/cmd/climate/enabled'   -m '{"commandId":"test-001","value":false,"source":"cli"}'
```

Risultato atteso:

```text
domoticsai/v1/ack/test-001
```

con stato `confirmed` e `simulated: true`.
