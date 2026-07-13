if(msg.payload.toString().length==1)msg.payload='0'+msg.payload;

global.set("stophour", msg.payload);

msg.payload = global.get("stophour") + ":" + global.get("stopminute") + ":00";
return msg;