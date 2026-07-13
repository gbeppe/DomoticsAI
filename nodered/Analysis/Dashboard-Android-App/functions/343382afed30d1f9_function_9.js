var a = msg.payload.split(':'); // split it at the colons

// minutes are worth 60 seconds. Hours are worth 60 minutes.
//msg.payload = (+a[0]) * 60 * 60 + (+a[1]) * 60 ;
//var d = new Date(Date.parse(msg.payload + "+0000")) ;
//msg.payload = d.getTime();

var d = new Date(2018, 11, 24, (+a[0])+1, (+a[1]), 0, 0);
msg.payload = d.getTime();

return msg;