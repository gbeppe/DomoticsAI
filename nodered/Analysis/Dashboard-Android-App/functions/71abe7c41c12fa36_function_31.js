if (msg.payload == "true") global.set("SensorePorticoAbilitato", "true")
else global.set("SensorePorticoAbilitato", "false");
return msg;