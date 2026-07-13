let currentTopic = global.get("app_base_topic", "file");
if (!currentTopic) {
    global.set("app_base_topic", "zara/android/domotica", "file");
    node.warn("App Base Topic inizializzato al default.");
}
return null;