var holiday = global.get("holiday", "file");

if (holiday === "false") return null;
    
msg.payload = 17;
return msg;