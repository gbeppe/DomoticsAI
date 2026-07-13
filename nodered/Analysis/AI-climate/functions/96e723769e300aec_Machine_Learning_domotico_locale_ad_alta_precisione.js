// ==================================================
// 1. MEMORIZZAZIONE DEI DATI IN INGRESSO
// ==================================================
if (msg.topic === "system/boot") {
    // Ignora il comando di avvio, serve solo a scatenare il ricalcolo dell'output
}
else if (msg.topic === "TeslaPowerwall/solar_instant_power") {
    flow.set("produzione", parseFloat(msg.payload));
}
else if (msg.topic === "TeslaPowerwall/load_instant_power") {
    flow.set("consumo", parseFloat(msg.payload));
}
else if (msg.topic === "TeslaPowerwall/SOE") {
    flow.set("powerwall_soc", parseFloat(msg.payload));
}
else if (msg.topic === "emon/emonth5/temperature_calibrated") {
    flow.set("temperatura", parseFloat(msg.payload));
}
else if (msg.topic === "zara/domotics/LivingHumidex") {
    flow.set("humidex_giorno", parseFloat(msg.payload));
}
else if (msg.topic === "zara/domotics/BedroomHumidex") {
    flow.set("humidex_notte", parseFloat(msg.payload));
}
else if (msg.topic === "zigbee2mqtt/TU-cucinaEsterno") {
    flow.set("temp_esterno", parseFloat(msg.payload.temperature));
    flow.set("umidita_esterno", parseFloat(msg.payload.humidity));
}
else if (msg.topic === "emon/cameraMatrimoniale/temperature") {
    flow.set("temp_cameraMatrimoniale", parseFloat(msg.payload));
}
else if (msg.topic === "emon/AC/emeter_power") {
    // Applichiamo valore assoluto per intercettare l'assorbimento reale (che arriva negativo dal sensore)
    flow.set("ac_power", Math.abs(parseFloat(msg.payload))); 
}

// DETERMINAZIONE DELLA STAGIONE E FASCIA
let meseAttuale = new Date().getMonth();
let MODALITA_STAGIONE = (meseAttuale >= 4 && meseAttuale <= 8) ? "ESTATE" : "INVERNO";

// ==================================================
// RECUPERO DATI METEO ESTERNI (Sensore Cucina Esterno)
// ==================================================
let tempEsterna = flow.get("temp_esterno");
let umiditaEsterna = flow.get("umidita_esterno");

if (tempEsterna === undefined || umiditaEsterna === undefined) {
    tempEsterna = (MODALITA_STAGIONE === "ESTATE") ? 24 : 8;
    umiditaEsterna = 60;
}

// Calcolo Punto di Rugiada e Humidex Esterno
let aEst = 17.27;
let bEst = 237.7;
let alphaEst = ((aEst * tempEsterna) / (bEst + tempEsterna)) + Math.log(umiditaEsterna / 100);
let dewPointEst = (bEst * alphaEst) / (aEst - alphaEst);
let eEst = 6.11 * Math.exp(5417.7530 * ((1 / 273.15) - (1 / (273.15 + dewPointEst))));
let humidexEsterno = parseFloat((tempEsterna + (5 / 9) * (eEst - 10)).toFixed(1));

// ==================================================
// 2. VARIABILI DI STATO E POTENZA
// ==================================================
let adesso = Date.now();
let statoAttuale = flow.get("condizionatore_stato", "file") || "OFF";

let ultimoAvvio = global.get("ultimo_avvio", "file") || (adesso - 40 * 60 * 1000);
let ultimoSpegnimento = global.get("ultimo_spegnimento", "file") || (adesso - 40 * 60 * 1000);

const MIN_RUN_MINUTI = parseFloat(global.get("user_min_run_time", "file")) || 15;
const MIN_OFF_MINUTI = parseFloat(global.get("user_min_off_time", "file")) || 15;
const DEFICIT_TOLERANCE_MINUTI = parseFloat(global.get("user_deficit_tolerance_time", "file")) || 10; 
const VMC_MAX_NOTTE = parseInt(global.get("user_vmc_max_notte", "file")) || 2;
const TARGET_HUMIDEX_ESTATE = parseFloat(global.get("user_target_humidex_estate", "file")) || 29;
const EMERGENCY_HUMIDEX_AWAY = parseFloat(global.get("user_emergency_humidex_away", "file")) || 33.0;

const MIN_RUN_TIME = MIN_RUN_MINUTI * 60 * 1000;
const MIN_OFF_TIME = MIN_OFF_MINUTI * 60 * 1000;
const DEFICIT_TOLERANCE_TIME = DEFICIT_TOLERANCE_MINUTI * 60 * 1000; 

let tempoPassatoDallAccensione = adesso - ultimoAvvio;
let tempoPassatoDalloSpegnimento = adesso - ultimoSpegnimento;

let minMancantiSpegnimento = tempoPassatoDallAccensione < MIN_RUN_TIME ? Math.ceil((MIN_RUN_TIME - tempoPassatoDallAccensione) / 60000) : 0;
let minMancantiAccensione = tempoPassatoDalloSpegnimento < MIN_OFF_TIME ? Math.ceil((MIN_OFF_TIME - tempoPassatoDalloSpegnimento) / 60000) : 0;
let tempoMancanteMinuti = (statoAttuale === "OFF") ? minMancantiAccensione : minMancantiSpegnimento;

// ==================================================
// 2. RECUPERO DELLE VARIABILI CORRENTI ED EVOLUZIONE STORICA
// ==================================================
let prod = flow.get("produzione") || 0;
let cons = flow.get("consumo") || 0;
let soc = (flow.get("powerwall_soc") !== undefined) ? flow.get("powerwall_soc") : 0;
let temp = flow.get("temperatura") || 19;
let hGiorno = flow.get("humidex_giorno") || 0;
let hNotte = flow.get("humidex_notte") || 0;
let temp_cameraMatrimoniale = flow.get("temp_cameraMatrimoniale") || 0;
let acPower = flow.get("ac_power") || 0;

let vmc_portata = [0, 50, 130, 160, 300];
let oraAttuale = new Date().getHours();
let surplus = prod - cons;

let kwhDomani = flow.get("previsione_kwh_domani") || 12;
let dataDomani = flow.get("previsione_data_domani") || "N/A";
let tutteMedie = flow.get("tutte_medie_storiche") || { ESTATE: { GIORNO: 600, NOTTE: 400 }, INVERNO: { GIORNO: 800, NOTTE: 500 } };
let efficienzaRicaricaTabella = flow.get("efficienza_ricarica_storica") || { ESTATE: 0.45, INVERNO: 0.30 };

let dataOraFormattata = new Intl.DateTimeFormat('it-IT', {
    timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
}).format(new Date(adesso));

let esNotteFascia = (oraAttuale >= 22 || oraAttuale < 8);
let humidex = esNotteFascia ? hNotte : hGiorno;
if (humidex === 0) humidex = (hGiorno !== 0) ? hGiorno : hNotte;

// ==================================================
// CALCOLO PREVISIONE RICARICA BATTERIA (ALGORITMO BILANCIO NETTO)
// ==================================================
const CAPACITA_BATTERIA_KWH = 13.5;
let consumoDiurnoStimatoKwh = (tutteMedie[MODALITA_STAGIONE]["GIORNO"] * 12) / 1000;
if (isNaN(consumoDiurnoStimatoKwh) || consumoDiurnoStimatoKwh < 3) consumoDiurnoStimatoKwh = 7.5;

let energiaDisponibilePerBatteriaKwh = kwhDomani - consumoDiurnoStimatoKwh;
if (energiaDisponibilePerBatteriaKwh < 0) energiaDisponibilePerBatteriaKwh = 0;

let socStimatoMattino = soc - 15;
if (socStimatoMattino < 0) socStimatoMattino = 0;
if (socStimatoMattino > 100) socStimatoMattino = 100; 

let capacitaVuotaKwh = CAPACITA_BATTERIA_KWH * (1 - (socStimatoMattino / 100));
let kwhDestinatiAllaBatteria = 0;
let percentualeRicaricaPrevista = 0;

if (energiaDisponibilePerBatteriaKwh >= capacitaVuotaKwh) {
    kwhDestinatiAllaBatteria = capacitaVuotaKwh;
    percentualeRicaricaPrevista = 100;
} else {
    kwhDestinatiAllaBatteria = energiaDisponibilePerBatteriaKwh;
    let ricaricaAggiuntivaPercentuale = (energiaDisponibilePerBatteriaKwh / CAPACITA_BATTERIA_KWH) * 100;
    percentualeRicaricaPrevista = Math.round(socStimatoMattino + ricaricaAggiuntivaPercentuale);
}

if (percentualeRicaricaPrevista > 100) percentualeRicaricaPrevista = 100;
if (percentualeRicaricaPrevista < 0) percentualeRicaricaPrevista = 0;

let comandoIR = null;
let sogliaAttivazioneLogica = 0;
let socMinimoLogico = 0;
let consumoStoricoAttuale = tutteMedie[MODALITA_STAGIONE][esNotteFascia ? "NOTTE" : "GIORNO"];

// ==================================================
// 3. MASTER SWITCH E LOGICA INTEGRATA
// ==================================================
let aiAbilitata = flow.get("AI_climate_enabling", "file");
if (aiAbilitata === undefined) {
    aiAbilitata = true;
    flow.set("AI_climate_enabling", true, "file");
}
let systemWasDisabled = flow.get("system_was_disabled") || false;

let velocitaVmc = 1;
let motivoVmc = "STANDBY_MINIMO";

if (!aiAbilitata) {
    if (!systemWasDisabled) {
        comandoIR = "OFF"; 
        statoAttuale = "OFF";
        flow.set("condizionatore_stato", "OFF", "file");
        flow.set("system_was_disabled", true);
        global.set("ultimo_spegnimento", adesso, "file");
    } else {
        statoAttuale = "OFF";
    }
    velocitaVmc = 1;
    motivoVmc = "SISTEMA_DISABILITATO";
    tempoMancanteMinuti = 0;

} else {
    if (systemWasDisabled) {
        flow.set("system_was_disabled", false);
    }

    // ==================================================
    // B.1 WATCHDOG ANELLO CHIUSO BIDIREZIONALE GLOBALE
    // ==================================================
    let bypassRoutine = false;

    if (statoAttuale !== "OFF" && acPower >= 10) {
        flow.set("tentativi_riavvio_ac", 0);
    }

    // FALSO OFF
    if (statoAttuale === "OFF" && acPower > 30 && (adesso - ultimoSpegnimento > 3 * 60 * 1000)) {
        comandoIR = "OFF";
        global.set("ultimo_spegnimento", adesso, "file"); 
        ultimoSpegnimento = adesso;                      
        node.warn(`Watchdog: Falso OFF rilevato. Consumo AC: ${acPower}W. Reinoltro OFF.`);
        bypassRoutine = true; 
    }
    // FALSO ON
    else if (statoAttuale !== "OFF" && acPower < 10 && (adesso - ultimoAvvio > 6 * 60 * 1000)) {
        let tentativi = flow.get("tentativi_riavvio_ac") || 0;
        
        if (tentativi < 3) {
            tentativi++;
            flow.set("tentativi_riavvio_ac", tentativi);
            node.warn(`Watchdog: Falso ON rilevato. Consumo ${acPower}W. Tentativo riavvio ${tentativi}/3.`);
            
            statoAttuale = "OFF";
            flow.set("condizionatore_stato", "OFF", "file");
            global.set("ultimo_spegnimento", adesso - MIN_OFF_TIME - 1000, "file");
            tempoMancanteMinuti = 0;
            minMancantiAccensione = 0;
        } else {
            node.error("Watchdog: Falliti 3 tentativi di avvio AC. Sospensione forzata dell'automazione.");
            aiAbilitata = false;
            flow.set("AI_climate_enabling", false, "file");
            flow.set("tentativi_riavvio_ac", 0);
            
            comandoIR = "OFF"; 
            statoAttuale = "OFF";
            flow.set("condizionatore_stato", "OFF", "file");
            global.set("ultimo_spegnimento", adesso, "file");
            bypassRoutine = true;
        }
    }

    // ==================================================
    // B.2 LOGICA CORE CONDIZIONATORE
    // ==================================================
    if (!bypassRoutine && aiAbilitata) {
        if (MODALITA_STAGIONE === "INVERNO") {
            sogliaAttivazioneLogica = esNotteFascia ? 17.0 : 19.0;
            socMinimoLogico = esNotteFascia ? (kwhDomani >= 22 && consumoStoricoAttuale < 700 ? 25 : (kwhDomani <= 8 || consumoStoricoAttuale > 1000 ? 60 : 40)) : 0;

            if (statoAttuale === "OFF") {
                if (!esNotteFascia && surplus > (consumoStoricoAttuale * 0.8) && temp < 19.0) {
                    if (minMancantiAccensione === 0) {
                        statoAttuale = "HEAT_DIURNO"; flow.set("condizionatore_stato", "HEAT_DIURNO", "file"); global.set("ultimo_avvio", adesso, "file"); comandoIR = "eco19heat";
                    }
                }
                else if (esNotteFascia && temp < 17.0 && soc > socMinimoLogico) {
                    if (minMancantiAccensione === 0) {
                        statoAttuale = "HEAT_SICUREZZA_NOTTE"; flow.set("condizionatore_stato", "HEAT_SICUREZZA_NOTTE", "file"); global.set("ultimo_avvio", adesso, "file"); comandoIR = "eco17heat";
                    }
                }
            } else {
                let richiediSpegnimentoInverno = false;
                if (statoAttuale === "HEAT_DIURNO" && (esNotteFascia || surplus < -150 || temp >= 19.5)) richiediSpegnimentoInverno = true;
                if (statoAttuale === "HEAT_SICUREZZA_NOTTE" && (!esNotteFascia || temp >= 17.5 || soc <= socMinimoLogico)) richiediSpegnimentoInverno = true;

                if (richiediSpegnimentoInverno && minMancantiSpegnimento === 0) {
                    statoAttuale = "OFF"; flow.set("condizionatore_stato", "OFF", "file"); global.set("ultimo_spegnimento", adesso, "file"); comandoIR = "OFF";
                }
            }
        }
        else if (MODALITA_STAGIONE === "ESTATE") {
            sogliaAttivazioneLogica = TARGET_HUMIDEX_ESTATE;
            socMinimoLogico = esNotteFascia ? (kwhDomani >= 28 && consumoStoricoAttuale < 450 ? 20 : (kwhDomani <= 12 ? 55 : 35)) : 85;

            // --- 🟢 INIZIO MODIFICA: PERIODO DI GRAZIA MATTUTINO (08:00 - 16:00) ---
            let gracePeriodStr = global.get("grace_period_time_range", "file") || "8-16";
            let graceParts = gracePeriodStr.split("-");
            let graceStart = parseInt(graceParts[0]) || 8;
            let graceEnd = parseInt(graceParts[1]) || 16;

            let isPeriodoDiGrazia = (oraAttuale >= graceStart && oraAttuale < graceEnd);
            //let isPeriodoDiGrazia = (oraAttuale >= 8 && oraAttuale < 16);
            let usaSoloSolare = global.get("grace_mode_solar", "file") === true; // Impostato dalla Dashboard
            // Aggiungi questo subito dopo aver letto "usaSoloSolare"
            //node.warn("Status Switch Grace Mode (SolarOnly): " + global.get("grace_mode_solar", "file"));

            if (isPeriodoDiGrazia) {
                if (!usaSoloSolare) {
                    // Opzione B (Default): Setpoint "Away".
                    // Aumentiamo la soglia di tolleranza di 3 punti Humidex per sfruttare l'inerzia termica.
                    //sogliaAttivazioneLogica = TARGET_HUMIDEX_ESTATE + 3.0;
                    // MODIFICA: In modalità AWAY forziamo la soglia al limite di emergenza. 
                    // Si accenderà SOLO se la casa diventa letteralmente un forno.
                    // Assicurati anche che la tua variabile user_emergency_humidex_away sulla dashboard 
                    // sia impostata a un valore sufficientemente alto(es. 33.0 o 34.0).
                    sogliaAttivazioneLogica = EMERGENCY_HUMIDEX_AWAY;
                }
            }
            // --- 🟢 FINE MODIFICA ---

            let surplusVirtuale = (statoAttuale === "OFF") ? (surplus - 700) : surplus;

            if (statoAttuale === "OFF") {
                let transizionePermessa = false;
                if (oraAttuale >= 18 || oraAttuale < 8) {
                    if (soc > 75 && humidex >= (sogliaAttivazioneLogica + 1.0)) transizionePermessa = true;
                } else {
                    if ((soc >= socMinimoLogico && surplusVirtuale > 150) || humidex >= EMERGENCY_HUMIDEX_AWAY) transizionePermessa = true;
                    // --- 🟢 INIZIO MODIFICA: VINCOLO SOLARE (Opzione C) ---
                    if (isPeriodoDiGrazia && usaSoloSolare) {
                        // Se abbiamo scelto il vincolo energetico solare, blocchiamo l'accensione se il surplus è insufficiente
                        if (surplus < 1000) transizionePermessa = false;
                    }
                    // --- 🟢 FINE MODIFICA ---
                }

                if (!esNotteFascia && transizionePermessa && humidex >= sogliaAttivazioneLogica) {
                    if (minMancantiAccensione === 0) {
                        statoAttuale = "COOLING_ON"; flow.set("condizionatore_stato", "COOLING_ON", "file"); global.set("ultimo_avvio", adesso, "file");
                        if (temp >= 26) comandoIR = "23"; else if (temp >= 25) comandoIR = "24"; else if (temp >= 24) comandoIR = "23"; else if (temp >= 23) comandoIR = "22"; else comandoIR = "26";
                    }
                } else if (esNotteFascia && humidex >= sogliaAttivazioneLogica && soc > socMinimoLogico) {
                    if (minMancantiAccensione === 0) {
                        statoAttuale = "NIGHT_DRY"; flow.set("condizionatore_stato", "NIGHT_DRY", "file"); global.set("ultimo_avvio", adesso, "file"); comandoIR = "25dry";
                    }
                }
            } else {
                let richiediSpegnimento = false;

                // --- GESTIONE SPEGNIMENTO COOLING_ON ---
                if (statoAttuale === "COOLING_ON") {
                    let limiteDeficitSurplus = soc > 95 ? -1500 : -300;

                    // Estensione tolleranza serale A GRADINI (Protezione Batteria Dinamica)
                    if (oraAttuale >= 18) {
                        if (soc > 90) limiteDeficitSurplus = -2000;      
                        else if (soc > 80) limiteDeficitSurplus = -1000; 
                        else if (soc > 70) limiteDeficitSurplus = -400;  
                        else limiteDeficitSurplus = -100;                
                    }

                    // --- 🟢 ISTERESI APPLICATA ALL'OPZIONE SOLARE MATTUTINA ---
                    if (isPeriodoDiGrazia && usaSoloSolare) {
                        // Invece di spegnere subito, alziamo l'asticella del timer.
                        // Se il surplus scende sotto i +500W, parte il cronometro di tolleranza (es. 10 min).
                        limiteDeficitSurplus = 500; 
                    }

                    // 1. Spegnimento immediato per Comfort Raggiunto
                    let sogliaSpegnimentoComfort = 26;

                    // --- 🟢 SPEGNIMENTO AGGRESSIVO IN PERIODO DI GRAZIA ---
                    if (isPeriodoDiGrazia && !usaSoloSolare) {
                        if (humidex > EMERGENCY_HUMIDEX_AWAY) {
                            sogliaSpegnimentoComfort = EMERGENCY_HUMIDEX_AWAY; // Emergenza
                        } else {
                            richiediSpegnimento = true; // Spegni sempre, non siamo in emergenza
                        }
                    } else {
                        // --- 🟢 MODIFICA: ISTERESI AC (Deadband Allargata) ---
                        // Allarghiamo la "buca" in cui l'Humidex deve cadere prima di spegnere la macchina.
                        // Un valore tra 2.5 e 3.5 garantisce cicli lunghi e asciuga i muri.
                        // Il valore 2.5 è un ottimo punto di partenza per bilanciare comfort e risparmio energetico.
                        // Se noti che l'ambiente diventa persino troppo freddo prima di spegnersi, 
                        // puoi scendere a 2.0. Se invece vuoi cicli ancora più lunghi, portalo a 3.0.
                        let ampiezzaIsteresi = 2.5; 
                        
                        sogliaSpegnimentoComfort = sogliaAttivazioneLogica - ampiezzaIsteresi;
                    }

                    if (humidex <= sogliaSpegnimentoComfort) {
                        richiediSpegnimento = true;
                        flow.set("inizio_deficit_surplus", 0);
                    }
                    // ... (resto della logica) ...
                    /*
                    if (isPeriodoDiGrazia && !usaSoloSolare) {
                        sogliaSpegnimentoComfort = sogliaAttivazioneLogica - 1.0; 
                    }
                    
                    if (humidex <= sogliaSpegnimentoComfort) {
                        richiediSpegnimento = true;
                        flow.set("inizio_deficit_surplus", 0); // Azzera eventuale timer
                    }
                    */
                    // 2. Isteresi temporale per picchi di consumo, nuvole o deficit batteria
                    else if (surplus < limiteDeficitSurplus) {
                        let inizioDeficit = flow.get("inizio_deficit_surplus") || 0;
                        if (inizioDeficit === 0) {
                            // La nuvola è appena arrivata: facciamo partire il cronometro
                            flow.set("inizio_deficit_surplus", adesso);
                        } else {
                            // La nuvola c'è ancora: è passato abbastanza tempo?
                            if ((adesso - inizioDeficit) >= DEFICIT_TOLERANCE_TIME) {
                                richiediSpegnimento = true;
                            }
                        }
                    }
                    // 3. Il sole è tornato / Il surplus è nella norma: azzeriamo il timer
                    else {
                        if (flow.get("inizio_deficit_surplus")) {
                            flow.set("inizio_deficit_surplus", 0);
                        }
                    }
                }

                // --- GESTIONE SPEGNIMENTO NIGHT_DRY ---
                // Spegne quando scende di 3 punti sotto il target diurno (es. se target è 28, spegne a 25)
                let sogliaSpegnimentoNotte = TARGET_HUMIDEX_ESTATE - 3.0; 
                if (statoAttuale === "NIGHT_DRY" && (humidex <= sogliaSpegnimentoNotte || soc <= socMinimoLogico)) {
                    richiediSpegnimento = true;
                }

                // --- ESECUZIONE MATERIALE DELLO SPEGNIMENTO ---
                if (richiediSpegnimento && minMancantiSpegnimento === 0) {
                    statoAttuale = "OFF";
                    flow.set("condizionatore_stato", "OFF", "file");
                    global.set("ultimo_spegnimento", adesso, "file");
                    comandoIR = "OFF";
                    flow.set("inizio_deficit_surplus", 0); // Pulizia sicurezza
                }
            }
        }
    }
    // ==================================================
    // B.3 LOGICA VMC (Ottimizzata con Scudo Termico)
    // ==================================================
    if (MODALITA_STAGIONE === "ESTATE") {

        // 1. FREE COOLING: Fuori fa decisamente più fresco. Aiutiamo il condizionatore.
        if (tempEsterna < (temp - 1.5)) {
            velocitaVmc = 3;
            motivoVmc = "FREE_COOLING_ATTIVO";
        }

        // 2. SCUDO TERMICO: Fuori fa più caldo. Sigilliamo la casa per non rovinare il lavoro dell'AC.
        else if (tempEsterna >= (temp + 0.5)) {
            velocitaVmc = 1;
            motivoVmc = "SCUDO_TERMICO_ATTIVO";
        }

        // 3. ESTRAZIONE INTELLIGENTE: Temperature simili. Estraiamo umidità solo se fuori non è un inferno.
        else {
            if (humidex >= 30 && humidexEsterno < (humidex + 2.0)) {
                velocitaVmc = 3;
                motivoVmc = "ESTRAZIONE_UMIDITA_ALTA";
            }
            else if (humidex >= 27 && humidexEsterno < (humidex + 2.0)) {
                velocitaVmc = 2;
                motivoVmc = "ESTRAZIONE_UMIDITA_MEDIA";
            }
            else {
                velocitaVmc = 1;
                motivoVmc = "RICAMBIO_ARIA_BASE";
            }
        }
    }
    // ==================================================
    // B.3 LOGICA VMC INVERNO (Ottimizzata con Scudo Termico)
    // ==================================================
    else {
        let urInterna = esNotteFascia ? flow.get("umidita_bedroom") : flow.get("umidita_living");
        if (urInterna === undefined) urInterna = 50;

        // 1. ANTI-CONDENSA EMERGENZA
        if (urInterna >= 65) { 
            velocitaVmc = 3; 
            motivoVmc = "ANTI_CONDENSA_MASSIMO"; 
        }
        else if (urInterna >= 55) { 
            velocitaVmc = 2; 
            motivoVmc = "ANTI_CONDENSA_MEDIO"; 
        }
        
        // 2. SCUDO TERMICO INVERNALE
        else if (tempEsterna < (temp - 5.0) && urInterna < 50) { 
            velocitaVmc = 1; 
            motivoVmc = "SCUDO_TERMICO_INVERNALE_ATTIVO"; 
        }
        
        // 3. COMFORT BASE
        else { 
            velocitaVmc = 1; 
            motivoVmc = "COMFORT_INVERNALE_BASE"; 
        }
    }

    if (esNotteFascia && velocitaVmc > VMC_MAX_NOTTE) { velocitaVmc = VMC_MAX_NOTTE; motivoVmc = motivoVmc + "_LIMITATO_NOTTE"; }
}
// ==================================================
// 3.5 BLOCCO ANTIRIMBALZO TEMPORALE E MEMORIA (VMC)
// ==================================================
// Recupera il tempo attuale e l'ultimo cambio effettivo
let currentTime = Date.now();
let lastVmcChangeTime = flow.get('vmc_ultimo_cambio_ms') || 0;
let lastVmcSpeed = flow.get("vmc_velocita_inviata") || velocitaVmc; // Usa la variabile flow che avevi già
let cooldownMs = 5 * 60 * 1000; // 5 minuti

// Se la logica ha cambiato idea rispetto all'ultima velocità FISICA inviata alla macchina
if (velocitaVmc !== lastVmcSpeed) {
    // E sono passati meno di 5 minuti
    if (currentTime - lastVmcChangeTime < cooldownMs) {
        // BLOCCO ATTIVO: Forza la variabile temporanea a tornare al valore precedente
        velocitaVmc = lastVmcSpeed;
        
        // Modifichiamo anche il motivo nel log per sapere che l'AI voleva cambiare ma è stata bloccata
        motivoVmc = "BLOCCO_ANTIRIMBALZO_ATTIVO";
        node.warn("Cambio VMC bloccato per evitare rimbalzi. Mantenuta velocità: " + lastVmcSpeed);
    } else {
        // VIA LIBERA: Il tempo è passato. Aggiorniamo il cronometro al momento attuale
        flow.set('vmc_ultimo_cambio_ms', currentTime);
        // La variabile flow.set("vmc_velocita_inviata") verrà aggiornata nel blocco RBE finale
    }
}

flow.set("vmc_fanspeed", velocitaVmc);

// ==================================================
// 4. MAPPATURA E PREPARAZIONE OUTPUT JSON
// ==================================================
if (!aiAbilitata) {
    flow.set("ac_log_temp", 0, "file");
    flow.set("ac_log_mode", "OFF", "file");
} else if (comandoIR) {
    let estrazioneTesto = comandoIR.match(/\d+/);
    let targetImpostato = estrazioneTesto ? parseFloat(estrazioneTesto[0]) : 0;
    
    if (comandoIR === "OFF" || comandoIR === "stop") { 
        flow.set("ac_log_temp", 0, "file"); 
        flow.set("ac_log_mode", "OFF", "file"); 
    }
    else if (comandoIR.includes("dry")) { 
        flow.set("ac_log_temp", targetImpostato || 25.0, "file"); 
        flow.set("ac_log_mode", "Deumidificazione", "file"); 
    }
    else if (comandoIR.includes("heat")) { 
        flow.set("ac_log_temp", targetImpostato || 19.0, "file"); 
        flow.set("ac_log_mode", "Riscaldamento", "file"); 
    }
    else { 
        flow.set("ac_log_temp", targetImpostato || 24.0, "file"); 
        flow.set("ac_log_mode", "Raffrescamento", "file"); 
    }
} else if (statoAttuale === "OFF") {
    flow.set("ac_log_temp", 0, "file"); 
    flow.set("ac_log_mode", "OFF", "file");
}

let tempImpostata = flow.get("ac_log_temp", "file") || 0;
let modalitaAria = flow.get("ac_log_mode", "file") || "OFF";

let datiAndroid = {
    timestamp: adesso,
    data_ora_formattata: dataOraFormattata,
    stagione_attiva: MODALITA_STAGIONE,
    metriche_elettriche: {
        produzione_fv_w: prod,
        consumo_casa_w: cons,
        surplus_w: surplus,
        powerwall_soc_percent: soc,
        consumo_ac_w: acPower,
        consumo_medio_storico_fascia_w: consumoStoricoAttuale
    },
    metriche_ambientali: {
        temp_cameraMatrimoniale: temp_cameraMatrimoniale,
        temperatura_c: temp,
        humidex: humidex,
        humidex_living: hGiorno,
        humidex_bedroom: hNotte
    },
    logica_controllo: {
        vmc_portata_stimata_m3h: vmc_portata[velocitaVmc],
        stanza_rilevamento_vmc: esNotteFascia ? "BEDROOM" : "LIVING",
        soglia_attivazione_applicata: sogliaAttivazioneLogica,
        soc_minimo_applied: socMinimoLogico,
        tempo_mancante_anticiclo_minuti: tempoMancanteMinuti,
        previsione_solare_domani_kwh: kwhDomani,
        previsione_solare_data: dataDomani,
        previsione_ricarica_batteria_percent: percentualeRicaricaPrevista,
        kwh_stimati_in_batteria: parseFloat(kwhDestinatiAllaBatteria.toFixed(1))
    },
    stato_condizionatore: {
        stato_attuale: statoAttuale,
        temperatura_impostata_c: tempImpostata,
        modalita_aria: modalitaAria
    },
    stato_vmc: {
        velocita_attuale: velocitaVmc,
        motivo_logica: motivoVmc,
        humidex_esterno: humidexEsterno,
        temperatura_esterna_c: tempEsterna
    }
};

let msgLog = null;
let precedenteStatoAC = flow.get("log_ultimo_stato_ac") || "OFF";
let precedenteVelocitaVMC = flow.get("log_ultima_vmc") || 1;

if (comandoIR || statoAttuale !== precedenteStatoAC || velocitaVmc !== precedenteVelocitaVMC || motivoVmc === "BLOCCO_ANTIRIMBALZO_ATTIVO") {
    msgLog = {
        payload: {
            timestamp: adesso, data_ora: dataOraFormattata, evento: "CAMBIO_STATO_SISTEMA",
            dettaglio_comandi: {
                comando_ir_inviato: comandoIR || "NESSUNO", stato_ac_precedente: precedenteStatoAC, stato_ac_attuale: statoAttuale,
                vmc_velocita_precedente: precedenteVelocitaVMC, vmc_velocita_attuale: velocitaVmc, motivo_logica: motivoVmc,
                humidex_esterno: humidexEsterno, temperatura_esterna_c: tempEsterna, modalita_aria: modalitaAria, temperatura_impostata_c: tempImpostata
            },
            condizioni_ambientali: { humidex_living: hGiorno, humidex_bedroom: hNotte, temperatura_c: temp, temp_cameraMatrimoniale: temp_cameraMatrimoniale, humidex: humidex, stanza_rilevamento: esNotteFascia ? "BEDROOM" : "LIVING" },
            stato_energia: { produzione_w: prod, consumo_w: cons, surplus_w: surplus, powerwall_soc_percent: soc, consumo_ac_w: acPower, soc_minimo_applied: socMinimoLogico },
            logica_controllo: { previsione_solare_domani_kwh: kwhDomani, previsione_solare_data: dataDomani, previsione_ricarica_batteria_percent: percentualeRicaricaPrevista, kwh_stimati_in_batteria: parseFloat(kwhDestinatiAllaBatteria.toFixed(1)) }
        },
        topic: "casa/clima/log_eventi"
    };
    flow.set("log_ultimo_stato_ac", statoAttuale);
    flow.set("log_ultima_vmc", velocitaVmc);
}

// ==================================================
// RETURN FINALE DEI MESSAGGI
// ==================================================
let msgBroadlink = comandoIR ? { payload: comandoIR, topic: "broadlink/cmd" } : null;
// Recupera il prefisso base dalla memoria (mettiamo un fallback di sicurezza nel caso sia vuoto)
let baseTopic = global.get("app_base_topic", "file") || "zara/android/domotica";

// Costruisce il topic unendo il prefisso al percorso specifico
let msgAndroid = { payload: datiAndroid, topic: `${baseTopic}/casa/clima/stato_completo` };
//let msgAndroid = { payload: datiAndroid, topic: "casa/clima/stato_completo" };

// ==================================================
// C. COSTRUZIONE MESSAGGI DI USCITA E FILTRI RBE
// ==================================================

// 1. Filtro Anti-Spam per la VMC
let ultimaVelocitaInviata = flow.get("vmc_velocita_inviata") || -1;
let msgVmc = null; // Di base, disattiviamo l'uscita 3

// Trasmettiamo il comando materiale all'ESP8266 SOLO se c'è un effettivo cambio fisico
if (velocitaVmc !== ultimaVelocitaInviata) {
    msgVmc = {
        topic: "/esp8266/brink/fanspeed",
        payload: velocitaVmc
    };
    // Salviamo la nuova velocità come stato materiale della macchina
    flow.set("vmc_velocita_inviata", velocitaVmc);
}

return [msgBroadlink, msgAndroid, msgVmc, msgLog];