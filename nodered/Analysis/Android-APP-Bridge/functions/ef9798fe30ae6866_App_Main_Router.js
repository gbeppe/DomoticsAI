let topic = msg.topic;
let baseTopic = global.get("app_base_topic") || "zara/android/domotica";

if (!topic.startsWith(baseTopic)) return null;

let routingPath = topic.substring(baseTopic.length);

let outLuci = null;         
let outTermostati = null;   
let outVmc = null;          
let outSettaggi = null;     

if (routingPath.startsWith("/light/") || routingPath.startsWith("/scene/")) {
    outLuci = msg;
} 
else if (routingPath.startsWith("/thermostat/")) {
    outTermostati = msg;
} 
else if (routingPath.startsWith("/vmc/")) {
    if (routingPath.includes("/maxNightSpeed/set")) {
        outSettaggi = msg;
    } else {
        outVmc = msg;
    }
} 
else {
    outSettaggi = msg;
}

return [outLuci, outTermostati, outVmc, outSettaggi];