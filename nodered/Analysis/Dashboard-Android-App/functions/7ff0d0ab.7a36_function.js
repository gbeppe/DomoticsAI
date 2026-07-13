val = parseInt(msg.payload);

if (val == 1 || val == 100) {
    msg.payload = "on";
    msg.topic = "Accesa";
} else {
    msg.payload = "off";
    msg.topic = "Spenta";
}

msg.enabled = "false";

return msg;