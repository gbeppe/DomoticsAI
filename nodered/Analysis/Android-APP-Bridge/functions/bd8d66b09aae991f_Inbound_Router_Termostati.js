let baseTopic = global.get("app_base_topic") || "zara/android/domotica";

let regexThermostat = new RegExp(`^${baseTopic}/thermostat/([^/]+)/target/set$`);
let match = msg.topic.match(regexThermostat);

if (!match || !match[1]) return null;

let room = match[1];
let setpoint = parseFloat(msg.payload);

if (isNaN(setpoint)) {
    node.warn(`Setpoint non valido ricevuto per ${room}: ${msg.payload}`);
    return null;
}

let targetTopic = "";
let targetPayload = null;

switch(room) {
    case "living":
        let gradiInteri = Math.round(setpoint);
        targetTopic = "zara/domotics/AC/command";
        targetPayload = gradiInteri.toString();
        break;
        
    case "bathroom":
        targetTopic = "zigbee2mqtt/Termostato_Bagno/set";
        targetPayload = { current_heating_setpoint: setpoint };
        break;
        
    case "small_bathroom":
        targetTopic = "zigbee2mqtt/Termostato_Bagnetto/set";
        targetPayload = { current_heating_setpoint: setpoint };
        break;
        
    default:
        node.warn("Comando App per termostato non mappato: " + room);
        return null;
}

return {
    topic: targetTopic,
    payload: targetPayload
};