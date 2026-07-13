// Recupera il prefisso dinamico dalla memoria
let baseTopic = global.get("app_base_topic", "file") || "zara/android/domotica";

// Costruisce il topic esatto per la richiesta dello storico
let topicRichiesta = baseTopic + "/history/ac/request";

// Crea il payload formattato per dire al nodo MQTT di iscriversi
let msgg = {
    action: "subscribe",
    topic: topicRichiesta,
    qos: 2
};

node.warn("Boot: In attesa di richieste storico su: " + topicRichiesta);

return msgg;