let baseTopic = global.get("app_base_topic", "file") || "zara/android/domotica";

// 1. Dati dalla stufa (ESP8266 -> App)
if (msg.topic.startsWith("zara/domotics/palazzetti/")) {
    let command = msg.topic.split('/').pop();
    let val = msg.payload !== undefined ? msg.payload.toString().toLowerCase() : "";
    let msgApp = null;

    if (command === "acceso") {
        let isOn = (val === "on" || val === "true" || val === "1");
        msgApp = { topic: `${baseTopic}/casa/stufa/stat/acceso`, payload: isOn };
    } else if (command === "modalita") {
        msgApp = { topic: `${baseTopic}/casa/stufa/stat/modalita`, payload: msg.payload };
    }

    if (msgApp) return [msgApp, null];
}

// 2. Comandi dall'App (App -> Stufa/Alexa)
/*
String inTopic_powerset = "/power";
String inTopic_command = "/command";
String inTopic_status = "/getstatus";
String outTopic = "/hello";
String outTopicLog = "/log/message";
String mqtt_client_id = "ESP8266-";
String mqtt_base_topic = "/esp8266/palazzetti";
*/
if (msg.topic.includes("alexa/caminetto")) {
    let command = msg.topic.split('/').pop();
    let val = msg.payload.toString();
    
    let msgLocal = null;
    let msgAlexa = null;
    
    if (command === "command") {
        let payloadAlexa = (val === "true" || val === "on") ? "on" : "off";
        msgAlexa = { topic: "alexa/caminetto/command", payload: payloadAlexa };
        msgLocal = { topic: `${baseTopic}/casa/stufa/stat/acceso`, payload: (payloadAlexa === "on") };
    } 
    else if (command === "power") {
        msgAlexa = { topic: "alexa/caminetto/power", payload: parseInt(val) };
        msgLocal = { topic: `${baseTopic}/casa/stufa/stat/potenza`, payload: parseInt(val) };
    } 
    else if (command === "modalita") {
        msgLocal = [
            // NOTA: Controlla che questo topic sia corretto per cambiare modalità nell'ESP8266
            { topic: "zara/domotics/palazzetti/set/modalita", payload: val }, 
            { topic: `${baseTopic}/casa/stufa/stat/modalita`, payload: val }
        ];
    }
    
    return [msgLocal, msgAlexa];
}

if (msg.topic.includes("emon/focolare/powerraw")) {
    let val = msg.payload.toString();
    let msgLocal = null;
    msgLocal = { topic: `${baseTopic}/casa/stufa/stat/potenza`, payload: parseInt(val) };
    return [msgLocal, null];
}

return null;