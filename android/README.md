# DomoticsAI Android v0.1.0

Prima applicazione Android nativa del progetto DomoticsAI.

## Funzioni incluse

- Jetpack Compose + Material 3;
- Home con dial FV e consumo;
- barra Powerwall;
- card clima e VMC;
- connessione MQTT al Gateway;
- modalità AUTO / LOCAL_ONLY / REMOTE_ONLY;
- log MQTT RX e connessione;
- impostazioni host e porta con DataStore;
- namespace `domoticsai/v1/#`.

## Endpoint predefinito

```text
192.168.1.40:1883
```

È il broker di test sul PC Linux, non il Raspberry di produzione.

## Sicurezza

Le credenziali non vengono ancora persistite. Il prossimo incremento userà Android Keystore.
L'app non si collega direttamente ai broker 192.168.1.20 o 192.168.1.15.

## Requisiti build

- Android Studio Quail 1 | 2026.1.1 o successivo;
- JDK 17;
- Android SDK 37;
- Gradle 9.4.1;
- AGP 9.2.1.

## Primo avvio

Aprire la cartella `android` del repository in Android Studio e attendere il Gradle Sync.
