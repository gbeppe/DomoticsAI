let baseTopic = global.get("app_base_topic") || "zara/android/domotica";

let regexVmc = new RegExp(`^${baseTopic}/vmc/([^/]+)/set$`);
let match = msg.topic.match(regexVmc);

if (!match || !match[1]) return null;

let cmdType = match[1];

if (cmdType === "speed") {
    let speed = parseInt(msg.payload);
    
    if (isNaN(speed) || speed < 1 || speed > 4) {
        node.warn("Comando VMC scartato. Valore non valido: " + msg.payload);
        return null;
    }
    
    return {
        topic: "/esp8266/brink/fanspeed",
        payload: speed
    };
}

return null;