var data = (msg.payload);
var m = {
 topic : "UPDATE `domotica`.`caminetto` SET `startTime` = ('" + data + "');"     
 };
return m;