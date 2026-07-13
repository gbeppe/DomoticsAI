let topicParts = msg.topic.split('/');
let command = topicParts[topicParts.length - 1]; 
let valore = msg.payload;

let valoreNumerico = parseFloat(valore);
let salvataggioEffettuato = false;

switch(command) {
    case "grace_mode_solar":
        let isSolar = (valore === true || valore === "true" || valore === "1");
        global.set("grace_mode_solar", isSolar, "file");
        salvataggioEffettuato = true;
        break;

    case "emergency_humidex_away":
        if (!isNaN(valoreNumerico)) {
            global.set("user_emergency_humidex_away", valoreNumerico, "file");
            salvataggioEffettuato = true;
        }
        break;
        
    case "min_run_time":
        if(!isNaN(valoreNumerico)) {
            global.set("user_min_run_time", valoreNumerico, "file");
            salvataggioEffettuato = true;
        }
        break;
        
    case "min_off_time":
        if(!isNaN(valoreNumerico)) {
            global.set("user_min_off_time", valoreNumerico, "file");
            salvataggioEffettuato = true;
        }
        break;
        
    case "target_humidex":
        if(!isNaN(valoreNumerico)) {
            global.set("user_target_humidex_estate", valoreNumerico, "file");
            salvataggioEffettuato = true;
        }
        break;
        
    case "vmc_max_notte":
        if(!isNaN(valoreNumerico)) {
            global.set("user_vmc_max_notte", parseInt(valoreNumerico), "file");
            salvataggioEffettuato = true;
        }
        break;

    // NUOVO BLOCCO: Tolleranza per picchi di consumo (forno, phon)
    case "deficit_tolerance_time":
        if(!isNaN(valoreNumerico)) {
            global.set("user_deficit_tolerance_time", valoreNumerico, "file");
            salvataggioEffettuato = true;
        }
        break;
        
    case "AI_climate_enabling":
    case "ai_enable":
    case "AI_enable":
//        let statoAI = (valore === true || valore === "true" || valore === "1" || valore === 1);
        flow.set("AI_climate_enabling", valore, "file");
//        valore = statoAI; 
        salvataggioEffettuato = true;
//        if (!valore) {
//            flow.set("system_was_disabled", false);
//        }
        break;
        
    default:
        node.warn("Ricevuto comando MQTT non mappato nel Gestore: " + msg.topic);
        return null; 
}

if (salvataggioEffettuato) {
    let msgStat = {
        topic: "casa/clima/stat/" + command,
        payload: valore
    };
    return msgStat;
}

return null;