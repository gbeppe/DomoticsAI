msg.payload = Math.round(Number.parseFloat(msg.payload) * 100)/100;
return msg;