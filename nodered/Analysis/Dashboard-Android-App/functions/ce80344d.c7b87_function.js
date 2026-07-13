if (msg.payload == "100") {
    msg.topic = "Accesa";
    msg.payload = "on";
} else if (msg.payload == "0"){
    msg.topic = "Spenta";
    msg.payload = "off";
}
return msg;