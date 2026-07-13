var data = (msg.payload);
var m = {
 topic : "UPDATE `domotica`.`caminetto` SET `stopTime` = ('" + data + "');"     
 };
return m;