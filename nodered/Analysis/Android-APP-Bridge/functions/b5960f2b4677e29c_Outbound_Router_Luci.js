let inTopic = msg.topic;
let inPayload = msg.payload;
let baseTopic = global.get("app_base_topic") || "zara/android/domotica";

let targetDevice = "";
let deviceState = "OFF";

if (inTopic.includes("zara/domotics/lights/shelflamp")) {
    targetDevice = "libreria";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("shellies/shelly1-B8C284/relay/0")) {
    targetDevice = "lavanderia";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("shellies/shelly1-B92AF0/relay/0")) {
    targetDevice = "ingressoServizio";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("shellies/shelly1-771284/relay/0")) {
    targetDevice = "portico";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("zara/domotics/lights/poolpump")) {
    targetDevice = "pompaPiscina";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("zara/domotics/lights/poolskimmer")) {
    targetDevice = "skimmerPiscina";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("zara/domotics/lights/poolfloor")) {
    targetDevice = "luciPedanaPiscina";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("zara/domotics/lights/poollight")) {
    targetDevice = "luciPiscina";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("zara/domotics/lights/tvlamp")) {
    targetDevice = "televisione";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("zara/domotics/lights/livinglamp")) {
    targetDevice = "sala";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
} 
else if (inTopic.includes("zigbee2mqtt/Luce_Cucina")) {
    targetDevice = "cucina";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("zigbee2mqtt/Luce_Libreria")) {
    targetDevice = "libreria";
    deviceState = (typeof inPayload === 'object') ? inPayload.state : inPayload;
}
else if (inTopic.includes("shellies/shelly1-esterno")) {
    targetDevice = "esterno";
    deviceState = inPayload.toString().toUpperCase();
}
else if (inTopic === "zara/domotics/lights/readinglight") {
    targetDevice = "tavolinoLettura";
    deviceState = inPayload.toString().toUpperCase();
}
else {
    return null; 
}

if (deviceState === "ON" || deviceState === "on" || deviceState === "true") {
    deviceState = "ON";
} else {
    deviceState = "OFF";
}

// Generazione dinamica del topic
return {
    topic: `${baseTopic}/light/${targetDevice}/state`,
    payload: deviceState
};