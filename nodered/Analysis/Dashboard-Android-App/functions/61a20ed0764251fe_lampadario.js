if (msg.payload == "on") msg.payload = "lampadario acceso";
if (msg.payload == "off") msg.payload = "lampadario spento";
return msg;