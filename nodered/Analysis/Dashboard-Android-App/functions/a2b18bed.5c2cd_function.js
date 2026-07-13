if (msg.payload == "on") {
    msg.topic = "Acceso";
    msg.payload == "on";
} else {
    msg.topic = "Spento";
    msg.payload == "off";
}
return msg;