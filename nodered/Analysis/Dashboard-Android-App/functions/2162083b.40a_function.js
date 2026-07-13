data = (msg.payload);
var m = {
 topic : "UPDATE `domotica`.`caminetto` SET `modalita` = ('" + data + "');"     
 };
return m;