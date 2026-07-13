const SUPERFICIE_MQ = 34; 
const EFFICIENZA = (0.20 - 0.08); 
const LOSS_FACTOR = 0.85; 

let data;

// 1. GESTIONE SICURA DEGLI ERRORI API
try {
    data = typeof msg.payload === "string" ? JSON.parse(msg.payload) : msg.payload;
} catch (e) {
    node.error("Open-Meteo API Error: Formato risposta non valido. Applico fallback di sicurezza.", msg);
    flow.set("previsione_kwh_domani", 12); // Valore di sicurezza medio
    return null; // Interrompe l'elaborazione dolcemente
}

// 2. ELABORAZIONE DATI METEO
if (data && data.hourly) { 
    let ore = data.hourly.time; 
    let radiazione = data.hourly.shortwave_radiation || data.hourly.direct_radiation || data.hourly.direct_radiation_instant; 
    
    if (!radiazione) { 
        node.error("Open-Meteo non ha restituito dati di radiazione validi."); 
        return null; 
    } 
    
    let domani = new Date(); 
    domani.setDate(domani.getDate() + 1); 
    let stringaDomani = domani.toISOString().split('T')[0]; 
    
    let sommaWh_per_mq = 0; 
    let oreTrovate = 0; 
    
    for (let i = 0; i < ore.length; i++) { 
        if (ore[i] && ore[i].startsWith(stringaDomani)) { 
            sommaWh_per_mq += radiazione[i] || 0; 
            oreTrovate++; 
        } 
    } 
    
    let kwh_per_mq = sommaWh_per_mq / 1000; 
    let kwhStimatiDomani = Math.round(SUPERFICIE_MQ * EFFICIENZA * kwh_per_mq * LOSS_FACTOR); 
    
    // Fallback in caso di giornata anomala
    if (oreTrovate === 0 || isNaN(kwhStimatiDomani) || kwhStimatiDomani < 0) { 
        kwhStimatiDomani = 12; 
    } 
    
    flow.set("previsione_kwh_domani", kwhStimatiDomani); 
    flow.set("previsione_data_domani", stringaDomani); 
    
    msg.payload = { 
        messaggio: "Previsione elaborata", 
        data_previsione: stringaDomani, 
        ore_elaborate: oreTrovate, 
        radiazione_totale_kwh_mq: parseFloat(kwh_per_mq.toFixed(2)), 
        kwh_stimati_impianto_reali: kwhStimatiDomani 
    }; 
    
    msg.topic = "casa/clima/previsione_meteo"; 
    return msg; 
} 

return null;