var data = (msg.payload);
var m = {
 topic : "UPDATE `domotica`.`general` SET `ACAUTO` = ('" + data + "');"     
 };
return m;