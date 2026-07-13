# Build e avvio

## Copia nel repository

La cartella di questo pacchetto deve diventare:

```text
/home/giuseppe/AndroidStudioProjects/DomoticsAI/android
```

## Gradle wrapper

Se il repository non dispone ancora del wrapper:

```bash
cd /home/giuseppe/AndroidStudioProjects/DomoticsAI/android
gradle wrapper --gradle-version 9.4.1
```

In alternativa Android Studio può eseguire il primo sync usando il Gradle configurato nell'IDE.

## Build

```bash
cd /home/giuseppe/AndroidStudioProjects/DomoticsAI/android
./gradlew assembleDebug
```

## Connessione dal telefono

Mosquitto sul PC deve ascoltare anche sull'interfaccia LAN `192.168.1.40`.
La semplice configurazione localhost usata nei test da terminale non è sufficiente per il telefono.

Non modificare ancora Mosquitto finché non viene fornita la configurazione di rete e sicurezza dedicata.
