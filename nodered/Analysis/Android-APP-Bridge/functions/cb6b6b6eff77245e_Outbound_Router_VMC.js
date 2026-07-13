let inTopic = msg.topic;
let speed = null;
let baseTopic = global.get("app_base_topic") || "zara/android/domotica";

if (inTopic === "alexa/vmc") {
    speed = parseInt(msg.payload);
} else if (inTopic === "casa/clima/stato_completo") {
    if (msg.payload && msg.payload.stato_vmc) {
        speed = msg.payload.stato_vmc.velocita_attuale;
    }
}

if (speed !== null && !isNaN(speed)) {
    return {
        topic: `${baseTopic}/vmc/speed/state`,
        payload: speed.toString()
    };
}
return null;