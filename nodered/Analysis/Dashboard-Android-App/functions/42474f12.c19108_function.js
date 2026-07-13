var data = (msg.payload);
var m = {
 topic : "UPDATE `domotica`.`general` SET `modalitavacanza` = ('" + data + "');"     
 };
return m;