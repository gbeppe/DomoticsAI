var a = msg.payload.split(':'); // split it at the colons

var d = new Date(2018, 11, 24, (+a[0]) + 1, (+a[1]), 0, 0);
msg.payload = d.getTime();

return msg;