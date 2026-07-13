# Local / Remote Connectivity Strategy

## Obiettivo

L'app deve selezionare automaticamente l'endpoint corretto per:

- MQTT;
- TinyCam.

## MQTT

Profili configurabili:

### Locale

- host predefinito: `192.168.1.20`;
- porta;
- username;
- password;
- TLS opzionale.

### Remoto

- host Tailscale;
- porta;
- username;
- password;
- TLS opzionale.

## Modalità

```text
AUTO
LOCAL_ONLY
REMOTE_ONLY
```

## Algoritmo AUTO

1. verifica disponibilità rete;
2. prova endpoint locale con timeout breve;
3. se disponibile, usa locale;
4. altrimenti prova endpoint remoto;
5. se entrambi falliscono, stato offline;
6. riprova con backoff;
7. registra ogni transizione nel log.

## TinyCam

Stessa strategia:

```text
localBaseUrl
remoteBaseUrl
port = 8083
```

## Nota

La selezione non deve basarsi soltanto sul fatto che il telefono sia connesso al Wi‑Fi.
Deve verificare l'effettiva raggiungibilità dell'endpoint.
