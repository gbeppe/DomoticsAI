# AI Climate — State Machine Draft

```mermaid
stateDiagram-v2
    [*] --> OFF

    OFF --> HEAT_DIURNO: inverno, giorno, surplus sufficiente, temperatura bassa, lockout OFF scaduto
    OFF --> HEAT_SICUREZZA_NOTTE: inverno, notte, temperatura bassa, SOC sufficiente, lockout OFF scaduto
    OFF --> COOLING_ON: estate, giorno, Humidex sopra soglia, energia disponibile, lockout OFF scaduto
    OFF --> NIGHT_DRY: estate, notte, Humidex alto, SOC sufficiente, pausa notturna scaduta

    HEAT_DIURNO --> OFF: fascia notte oppure deficit oppure temperatura raggiunta
    HEAT_SICUREZZA_NOTTE --> OFF: giorno oppure temperatura raggiunta oppure SOC insufficiente
    COOLING_ON --> OFF: comfort raggiunto oppure deficit persistente
    NIGHT_DRY --> OFF: Humidex raggiunto oppure limite temperatura camera oppure SOC insufficiente

    HEAT_DIURNO --> OFF: AI disabilitata
    HEAT_SICUREZZA_NOTTE --> OFF: AI disabilitata
    COOLING_ON --> OFF: AI disabilitata
    NIGHT_DRY --> OFF: AI disabilitata
```

## Guardie globali

Ogni transizione deve rispettare:

- tempo minimo di accensione;
- tempo minimo di spegnimento;
- watchdog di potenza reale;
- abilitazione generale AI;
- limiti energetici;
- vincoli di fascia oraria;
- eventuale modalità di grazia mattutina.
