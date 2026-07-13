if (msg.payload == "true") global.set("SensorePorticoAbilitato", "true", "file")
else global.set("SensorePorticoAbilitato", "false", "file");
return msg;