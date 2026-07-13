let baseTopic = global.get("app_base_topic", "file") || "zara/android/domotica";

return {
    topic: `${baseTopic}/history/ac/response`,
    payload: msg.payload // Inoltra direttamente l'array JSON del DB
};