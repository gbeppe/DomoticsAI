# AI Climate — Reverse Engineering v0.1

## Ambito

Analisi del tab Node-RED `AI climate` (`2cc001ef3d59afd2`) dello snapshot corrente.

## Dimensione del flow

- Nodi complessivi: **105**
- MQTT input: **22**
- MQTT output: **8**
- Function node: **18**
- UI node: **14**
- Nodo decisionale principale: `61992c8879c11f66`
- Dimensione nodo principale: **647 righe**, **31674 caratteri**
- Uscite dichiarate dal nodo principale: **4**

## Responsabilità principali

Il flow combina più responsabilità:

1. acquisizione delle telemetrie;
2. persistenza dello stato;
3. selezione estate/inverno;
4. decisione climatizzatore;
5. watchdog di coerenza tra stato logico e assorbimento reale;
6. gestione VMC;
7. configurazione da dashboard e Android;
8. pubblicazione dello stato aggregato;
9. registrazione di eventi e consumi;
10. invio dei comandi IR e MQTT.

Questa concentrazione rende il flow funzionante, ma complesso da verificare e testare.

## Ingressi decisionali principali

| Segnale | Topic |
|---|---|
| Produzione fotovoltaica | `TeslaPowerwall/solar_instant_power` |
| Consumo casa | `TeslaPowerwall/load_instant_power` |
| SOC Powerwall | `TeslaPowerwall/SOE` |
| Temperatura living | `emon/emonth5/temperature_calibrated` |
| Temperatura camera | `emon/cameraMatrimoniale/temperature` |
| Humidex living | `zara/domotics/LivingHumidex` |
| Humidex camera | `zara/domotics/BedroomHumidex` |
| Potenza reale climatizzatore | `emon/AC/emeter_power` |
| Meteo esterno | `zigbee2mqtt/TU-cucinaEsterno` |

## Stati logici climatizzatore

- `COOLING_ON`
- `HEAT_DIURNO`
- `HEAT_SICUREZZA_NOTTE`
- `NIGHT_DRY`
- `OFF`

## Comandi IR individuati

- `22`
- `23`
- `24`
- `25dry`
- `26`
- `OFF`
- `eco17heat`
- `eco19heat`

## Motivi VMC individuati

- `ANTI_CONDENSA_MASSIMO`
- `ANTI_CONDENSA_MEDIO`
- `BLOCCO_ANTIRIMBALZO_ATTIVO`
- `COMFORT_INVERNALE_BASE`
- `ESTRAZIONE_UMIDITA_ALTA`
- `ESTRAZIONE_UMIDITA_MEDIA`
- `FREE_COOLING_ATTIVO`
- `RICAMBIO_ARIA_BASE`
- `SCUDO_TERMICO_ATTIVO`
- `SCUDO_TERMICO_INVERNALE_ATTIVO`
- `SISTEMA_DISABILITATO`
- `STANDBY_MINIMO`

## Uscite principali

Il nodo decisionale ha quattro uscite:

1. comando climatizzatore verso il controller IR;
2. stato completo verso `casa/clima/stato_completo` e moduli collegati;
3. comando VMC;
4. dati diagnostici, UI e logging.

La mappatura esatta è documentata nei file CSV e dovrà essere mantenuta nel Gateway senza alterare il flow di produzione.

## Parametri configurabili rilevati

- `user_deficit_tolerance_time`
- `user_emergency_humidex_away`
- `user_min_off_time`
- `user_min_run_time`
- `user_target_humidex_estate`
- `user_vmc_max_notte`

## Variabili di stato interne rilevate

### Flow context

- `AI_climate_enabling`
- `ac_log_mode`
- `ac_log_temp`
- `ac_power`
- `condizionatore_stato`
- `consumo`
- `efficienza_ricarica_storica`
- `humidex_giorno`
- `humidex_notte`
- `inizio_deficit_surplus`
- `log_ultima_vmc`
- `log_ultimo_stato_ac`
- `powerwall_soc`
- `previsione_data_domani`
- `previsione_kwh_domani`
- `produzione`
- `system_was_disabled`
- `temp_cameraMatrimoniale`
- `temp_esterno`
- `temperatura`
- `tentativi_riavvio_ac`
- `tutte_medie_storiche`
- `ultimo_spegnimento_notte`
- `umidita_bedroom`
- `umidita_esterno`
- `umidita_living`
- `vmc_fanspeed`
- `vmc_ultimo_cambio_ms`
- `vmc_velocita_inviata`

### Global context

- `app_base_topic`
- `grace_mode_solar`
- `grace_period_time_range`
- `ultimo_avvio`
- `ultimo_spegnimento`
- `user_deficit_tolerance_time`
- `user_emergency_humidex_away`
- `user_min_off_time`
- `user_min_run_time`
- `user_target_humidex_estate`
- `user_vmc_max_notte`

## Criticità strutturali iniziali

### 1. Nodo monolitico

Il nodo principale supera le 647 righe e gestisce input, stato, decisioni, watchdog, VMC e output.
Questo aumenta il rischio che una modifica locale produca effetti collaterali.

### 2. Copie del motore decisionale

Nel tab sono presenti **4** Function node con lo stesso nome.
Solo il nodo `61992c8879c11f66` risulta collegato operativamente; le altre copie non hanno collegamenti in uscita e sembrano versioni di lavoro o backup.

### 3. Nodi abilitati ma non collegati

Le copie non collegate del motore AI non sono marcate come disabilitate.
Non comandano l'impianto finché restano scollegate, ma creano ambiguità durante manutenzione e reverse engineering.

### 4. Stato distribuito

Il motore usa contemporaneamente:

- `flow` volatile;
- `flow` persistente su file;
- `global` persistente su file.

Serve una matrice formale di ownership per evitare collisioni e scritture inutili.

### 5. Decisioni temporali basate su eventi in ingresso

Il ricalcolo avviene quando arriva un messaggio o al boot.
Occorre verificare se esiste un heartbeat periodico sufficiente per far scadere correttamente timer e condizioni anche quando le telemetrie non cambiano.

### 6. Stagione calcolata dal mese

La stagione viene dedotta dal mese calendario. È semplice e stabile, ma non gestisce mezze stagioni o override manuali.

## Confine architetturale proposto

Il nuovo Gateway non sostituirà inizialmente questa logica.
Dovrà:

- osservare i topic esistenti;
- pubblicare uno stato normalizzato;
- ricevere configurazioni validate;
- mantenere un audit log;
- simulare input in ambiente test;
- predisporre eventi strutturati per la futura AI generativa.

Il refactoring del motore verrà affrontato solo dopo avere test di regressione ripetibili.
