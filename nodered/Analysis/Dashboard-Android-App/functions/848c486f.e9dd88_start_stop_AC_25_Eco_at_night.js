var humidexCamera = msg.payload;
var bedroomTemp = Number(global.get("bedroomTemp"));
var date = new Date();
var currentHour = date.getHours();
var ACRaffrescamento = global.get("ACRaffrescamento")||"off";

var ACAuto = global.get("ACAUTO", "file") || "false";

if (ACAuto == "false") {
    msg.payload = "off";
} else {
    

global.set("ACRaffrescamento", ACRaffrescamento);

//if ((currentHour >= 23 || currentHour <= 7) && bedroomTemp > 25.4) {
if (bedroomTemp > 23 && (currentHour >= 0 && currentHour <= 5)) {
    if (humidexCamera <= 28 && ACRaffrescamento != "off") {
        msg.payload = "off";
        global.set("ACRaffrescamento", msg.payload);
    }
    if (humidexCamera >= 29 || humidexCamera <= 30) {
        msg.payload = "on26dry";
        global.set("ACRaffrescamento", msg.payload);
    }
    if (humidexCamera > 30 || humidexCamera <= 31) {
        msg.payload = "on25dry";
        global.set("ACRaffrescamento", msg.payload);
    }
    if (humidexCamera > 31 && ACRaffrescamento == "off") {
        msg.payload = "on25dry";
        global.set("ACRaffrescamento", msg.payload);
    }
} else {
    if (ACRaffrescamento != "off") {
        msg.payload = "off";
        global.set("ACRaffrescamento", msg.payload);
    }
}
}

return msg;

