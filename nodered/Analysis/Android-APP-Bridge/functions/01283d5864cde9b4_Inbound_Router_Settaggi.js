let baseTopic = global.get("app_base_topic", "file") || "zara/android/domotica";
let inTopic = msg.topic;
let rawPayload = msg.payload.toString().trim(); 

function parseBoolean(val) {
    if (val === "1" || val.toLowerCase() === "true") return true;
    if (val === "0" || val.toLowerCase() === "false") return false;
    return null;
}

let targetTopic = "";
let targetPayload = "";

switch (inTopic) {
    // AGGIUNTA: Gestione Range Temporale Periodo di Grazia
    case `${baseTopic}/system/time_range/set`:
        // Validazione regex: accetta formati come "8-16" o "08-16"
        if (/^\d{1,2}-\d{1,2}$/.test(rawPayload)) {
            global.set("grace_period_time_range", rawPayload, "file");
            targetTopic = "time_range";
            targetPayload = rawPayload;
        } else {
            node.warn("Time range ignorato: formato errato " + rawPayload);
        }
        break;

    case `${baseTopic}/system/enabled/state`:
        let sysEnabled = parseBoolean(rawPayload);
        if (sysEnabled !== null) {
            targetTopic = "system";
            targetPayload = sysEnabled;
        }
        break;

    case `${baseTopic}/system/holiday/set`:
        let holidayMode = parseBoolean(rawPayload);
        if (holidayMode !== null) {
            targetTopic = "holiday";
            targetPayload = holidayMode;
        }
        break;

    case `${baseTopic}/system/ac_auto/set`:
        let acAuto = parseBoolean(rawPayload);
        if (acAuto !== null) {
            targetTopic = "ACAUTO";
            targetPayload = acAuto;
        }
        break;

    case `${baseTopic}/system/luci_eco/set`:
        let ecoLights = parseBoolean(rawPayload);
        if (ecoLights !== null) {
            targetTopic = "luciECO";
            targetPayload = ecoLights;
        }
        break;

    case `${baseTopic}/system/luci_piscina_auto/set`:
        let poolAuto = parseBoolean(rawPayload);
        if (poolAuto !== null) {
            targetTopic = "luciPiscinaAUTO";
            targetPayload = poolAuto;
        }
        break;
        
    case `${baseTopic}/system/sensore_portico/set`:
        let porch_sensor = parseBoolean(rawPayload);
        if (porch_sensor !== null) {
            targetTopic = "porch_sensor";
            targetPayload = porch_sensor;
        }
        break;

    case `${baseTopic}/vmc/maxNightSpeed/state`:
        let maxSpeed = parseInt(rawPayload);
        if (!isNaN(maxSpeed) && maxSpeed >= 1 && maxSpeed <= 4) {
            targetTopic = "vmc_night_limit";
            targetPayload = maxSpeed;
        }
        break;

    default:
        return null;
}

if (targetTopic !== "") {
    return { topic: targetTopic, payload: targetPayload };
}

return null;