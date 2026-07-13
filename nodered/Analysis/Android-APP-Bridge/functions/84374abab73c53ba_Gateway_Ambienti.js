// --- GATEWAY TELEMETRIE: AMBIENTI ---
let inTopic = msg.topic;
let rawPayload = msg.payload;

const APP_BASE = global.get("app_base_topic", "file") || "zara/android/domotica";

let messaggiInUscita = [];

switch (inTopic) {
    case "emon/emonth5/humidex":
        if (!isNaN(parseFloat(rawPayload))) {
            messaggiInUscita.push({ topic: `${APP_BASE}/env/humidexLiving`, payload: parseFloat(rawPayload).toString() });
        }
        break;
    case "emon/cameraMatrimoniale/humidex":
        if (!isNaN(parseFloat(rawPayload))) {
            messaggiInUscita.push({ topic: `${APP_BASE}/env/humidexBedroom`, payload: parseFloat(rawPayload).toString() });
        }
        break;
    case "emon/emonth5/temperature_calibrated":
        if (!isNaN(parseFloat(rawPayload))) {
            messaggiInUscita.push({ topic: `${APP_BASE}/env/tempLiving`, payload: parseFloat(rawPayload).toString() });
        }
        break;
        
    case "emon/emonth5/humidity":
        if (!isNaN(parseFloat(rawPayload))) {
            messaggiInUscita.push({ topic: `${APP_BASE}/env/humLiving`, payload: parseFloat(rawPayload).toString() });
        }
        break;
        
    case "emon/cameraMatrimoniale/temperature":
        if (!isNaN(parseFloat(rawPayload))) {
            messaggiInUscita.push({ topic: `${APP_BASE}/env/tempBedroom`, payload: parseFloat(rawPayload).toString() });
        }
        break;
        
    case "emon/cameraMatrimoniale/humidity":
        if (!isNaN(parseFloat(rawPayload))) {
            messaggiInUscita.push({ topic: `${APP_BASE}/env/humBedroom`, payload: parseFloat(rawPayload).toString() });
        }
        break;

    case "zigbee2mqtt/Sonoff AirGuard TH camera matrimoniale":
        if (typeof rawPayload === 'object') {
            if (rawPayload.temperature !== undefined) {
                messaggiInUscita.push({
                    topic: `${APP_BASE}/env/tempBedroom`,
                    payload: parseFloat(rawPayload.temperature).toString()
                });
            }
            if (rawPayload.humidity !== undefined) {
                messaggiInUscita.push({
                    topic: `${APP_BASE}/env/humBedroom`,
                    payload: rawPayload.humidity.toString()
                });
            }
        }
        break;
    case "zigbee2mqtt/Sonoff AirGuard TH esterno cucina":
        if (typeof rawPayload === 'object') {
            if (rawPayload.temperature !== undefined) {
                messaggiInUscita.push({
                    topic: `${APP_BASE}/env/tempOutdoor`,
                    payload: rawPayload.temperature.toString()
                });
            }
            if (rawPayload.humidity !== undefined) {
                messaggiInUscita.push({
                    topic: `${APP_BASE}/env/humOutdoor`,
                    payload: rawPayload.humidity.toString()
                });
            }
        }
        break;
        
    default:
        return null;
}

if (messaggiInUscita.length === 0) {
    return null; 
}

return [ messaggiInUscita ];