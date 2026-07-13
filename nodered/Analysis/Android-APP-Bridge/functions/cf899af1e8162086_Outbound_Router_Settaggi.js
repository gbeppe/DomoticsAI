// ============================================================================
// OUTBOUND ROUTER SETTAGGI
// Formatta i feedback hardware per aggiornare la UI dell'App Android
// ============================================================================

let inTopic = msg.topic;
let baseTopic = global.get("app_base_topic") || "zara/android/domotica";

// Helper per pulire la conversione verso l'app (0 = false, 1 = true)
const parseToBinary = (val) => (val === "true" || val === true || val === 1 || val === "1") ? 1 : 0;

if (inTopic === "zara/domotics/modalitavacanza") {
    return { 
        topic: `${baseTopic}/system/holiday/state`, 
        payload: parseToBinary(msg.payload) 
    };
}
else if (inTopic === "casa/clima/cmnd/AI_climate_enabling") {
    return { 
        topic: `${baseTopic}/system/set`, 
        payload: parseToBinary(msg.payload) 
    };
}
else if (inTopic === "zara/domotics/luciECO") {
    return { 
        topic: `${baseTopic}/system/luci_eco/state`, 
        payload: parseToBinary(msg.payload) 
    };
}
else if (inTopic === "zara/domotics/luciPiscinaAuto") {
    return { 
        topic: `${baseTopic}/system/luci_piscina_auto/state`, 
        payload: parseToBinary(msg.payload) 
    };
}
else if (inTopic === "zara/domotics/ACAuto") {
    return { 
        topic: `${baseTopic}/system/ac_auto/state`, 
        payload: parseToBinary(msg.payload) 
    };
}
else if (inTopic === "zara/domotics/porch_sensor") {
    return { 
        topic: `${baseTopic}/system/sensore_portico/state`, 
        payload: parseToBinary(msg.payload) 
    };
}
else if (inTopic === "casa/clima/stat/vmc_max_notte") {
    return { 
        topic: `${baseTopic}/vmc/maxNightSpeed/set`, 
        payload: msg.payload 
    };
}
else if (inTopic === "zara/domotics/time_range") {
    return { 
        topic: `${baseTopic}/system/time_range/state`, 
        payload: msg.payload 
    };
}

return null;