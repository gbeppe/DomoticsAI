let inTopic = msg.topic;
let targetRoom = "";
let targetTemp = null;
let baseTopic = global.get("app_base_topic") || "zara/android/domotica";

if (inTopic === "casa/clima/stato_completo") {
    targetRoom = "living";
    targetTemp = msg.payload.stato_condizionatore.temperatura_impostata_c;
    if (targetTemp === 0) return null; 
}
else if (inTopic.includes("zigbee2mqtt/Termostato_Bagno")) {
    targetRoom = "bathroom";
    targetTemp = (typeof msg.payload === 'object') ? msg.payload.current_heating_setpoint : parseFloat(msg.payload);
}
else if (inTopic.includes("zigbee2mqtt/Termostato_Bagnetto")) {
    targetRoom = "small_bathroom";
    targetTemp = (typeof msg.payload === 'object') ? msg.payload.current_heating_setpoint : parseFloat(msg.payload);
}

if (targetRoom !== "" && targetTemp !== null && !isNaN(targetTemp)) {
    return {
        topic: `${baseTopic}/thermostat/${targetRoom}/target/state`,
        payload: targetTemp
    };
}

return null;