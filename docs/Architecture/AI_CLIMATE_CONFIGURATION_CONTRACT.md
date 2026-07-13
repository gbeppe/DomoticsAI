# AI Climate — Configuration Contract Draft

| Parametro logico | Variabile persistente | Topic corrente | Tipo | Uso |
|---|---|---|---|---|
| Abilitazione AI | `AI_climate_enabling` | `casa/clima/cmnd/AI_climate_enabling` | boolean | abilita/disabilita gestione automatica |
| Tempo minimo ON | `user_min_run_time` | `casa/clima/cmnd/min_run_time` | minuti | evita cicli brevi |
| Tempo minimo OFF | `user_min_off_time` | `casa/clima/cmnd/min_off_time` | minuti | protegge il compressore |
| Target Humidex estate | `user_target_humidex_estate` | `casa/clima/cmnd/target_humidex` | numero | soglia comfort |
| VMC massima notte | `user_vmc_max_notte` | `casa/clima/cmnd/vmc_max_notte` | intero | limite acustico |
| Tolleranza deficit | `user_deficit_tolerance_time` | `casa/clima/cmnd/deficit_tolerance_time` | minuti | filtra nuvole e picchi |
| Humidex emergenza away | `user_emergency_humidex_away` | `casa/clima/cmnd/emergency_humidex_away` | numero | soglia emergenza |
| Grace mode solare | `grace_mode_solar` | `casa/clima/cmnd/grace_mode_solar` | boolean | consente uso solo con surplus |
| Fascia grace | `grace_period_time_range` | da definire | stringa `H-H` | intervallo orario |

## Contratto Gateway proposto

Per ciascun parametro:

```text
domoticsai/v1/config/climate/<parameter>/set
domoticsai/v1/config/climate/<parameter>/state
```

Il Gateway deve:

1. validare tipo e intervallo;
2. pubblicare il comando sul topic corrente;
3. attendere o produrre lo stato confermato;
4. registrare utente, timestamp, valore precedente e nuovo valore;
5. non scrivere direttamente nel context di Node-RED produzione.
