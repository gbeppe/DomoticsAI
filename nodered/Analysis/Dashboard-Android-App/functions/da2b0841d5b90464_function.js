data = (msg.payload);
var m = {
 topic : "UPDATE `domotica`.`general` SET `luciECO` = ('" + data + "');"     
 };
return m;