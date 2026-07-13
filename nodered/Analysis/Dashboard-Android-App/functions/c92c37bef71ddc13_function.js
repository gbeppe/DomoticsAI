var data = (msg.payload);
var m = {
 topic : "UPDATE `domotica`.`general` SET `luciPiscinaAUTO` = ('" + data + "');"     
 };
return m;