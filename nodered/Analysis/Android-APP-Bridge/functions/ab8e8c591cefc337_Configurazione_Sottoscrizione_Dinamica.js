// Recupera il topic base dalla configurazione globale o usa il default
let baseTopic = global.get("app_base_topic") || "zara/android/domotica";

// Costruiamo il topic completo per la sottoscrizione (ascolto su tutta la gerarchia)
let subscriptionTopic = baseTopic + "/#";

// Creiamo il messaggio di comando per il nodo MQTT
// Il nodo MQTT con "Dynamic Subscription" accetta msg.action = 'subscribe'
let msg1 = {
    action: "subscribe",
    topic: subscriptionTopic,
    qos: 2
};

// Log per debug nel pannello di Node-RED
node.warn("Boot: Sottoscrizione dinamica attivata su topic: " + subscriptionTopic);

return msg1;