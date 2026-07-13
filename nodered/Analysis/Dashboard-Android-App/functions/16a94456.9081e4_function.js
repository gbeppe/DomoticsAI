if(msg.payload.toString().length==1)msg.payload='0'+msg.payload;

global.set("starthour", msg.payload);
msg.payload = global.get("starthour") + ":" + global.get("startminute") + ":00";
return msg;