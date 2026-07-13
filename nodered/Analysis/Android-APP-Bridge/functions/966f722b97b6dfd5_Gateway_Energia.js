// --- GATEWAY TELEMETRIE: ENERGIA E PUFFER ---
let inTopic = msg.topic;
let payload = parseFloat(msg.payload);

if (isNaN(payload)) return null;

const APP_BASE = global.get("app_base_topic", "file") || "zara/android/domotica";
let outTopic = "";
let outPayload = payload;

switch (inTopic) {
       
    case "TeslaPowerwall/solar_instant_power":
        outTopic = `${APP_BASE}/energy/production`;
        outPayload = Math.round(payload); 
        
        let ultProd = flow.get("last_prod") || 0;
        if (Math.abs(outPayload - ultProd) < 15) return null;
        flow.set("last_prod", outPayload);
        break;
        
    case "TeslaPowerwall/load_instant_power":
        outTopic = `${APP_BASE}/energy/consumption`;
        outPayload = Math.round(payload);
        
        let ultCons = flow.get("last_cons") || 0;
        if (Math.abs(outPayload - ultCons) < 15) return null;
        flow.set("last_cons", outPayload);
        break;  
     case "TeslaPowerwall/site_instant_power":
        outTopic = `${APP_BASE}/energy/grid`;
        if (Math.abs(payload) < 20) outPayload = 0;
        else outPayload = payload;
        break;    
    case "TeslaPowerwall/SOE":
        outTopic = `${APP_BASE}/energy/battery`;
        outPayload = Math.round(payload * 10) / 10;
        break;

    case "emon/shellyACS/tempACS": 
        outTopic = `${APP_BASE}/acsPufferTemp`;
        outPayload = Math.round(payload * 10) / 10;
        break;
        
    case "emon/resolDL2/sensor3":
        outTopic = `${APP_BASE}/pufferAltoTemp`;
        outPayload = Math.round(payload * 10) / 10;
        break;
        
    case "surplus":
        outTopic = `${APP_BASE}/energy/surplus`;
        outPayload = msg.payload;
        break;

    case "emon/resolDL2/sensor2":
        outTopic = `${APP_BASE}/pufferBassoTemp`;
        outPayload = Math.round(payload * 10) / 10;
        break;
        
    default:
        return null;
}

return {
    topic: outTopic,
    payload: outPayload.toString()
};