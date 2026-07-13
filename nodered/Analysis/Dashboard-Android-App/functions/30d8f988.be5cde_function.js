if (msg.topic == "emon/emonth5/temperature_calibrated")
    flow.set("livingTemp", msg.payload);
else if (msg.topic == "emon/cameraMatrimoniale/temperature")
    flow.set("bedroomTemp", msg.payload);
else if (msg.topic == "emon/emonth5/humidity")
    flow.set("livingHumidity", msg.payload);
else if (msg.topic == "emon/cameraMatrimoniale/humidity")
    flow.set("bedroomHumidity", msg.payload);

var livingTemp = flow.get("livingTemp")||0;
var bedroomTemp = flow.get("bedroomTemp")||0;
var livingHumidity = flow.get("livingHumidity")||0;
var bedroomHumidity = flow.get("bedroomHumidity")||0;

var hum = parseInt(livingHumidity);
var temp = parseInt(livingTemp);
var dewPoint = Math.pow(hum/100, 1 / 8) * (112 + 0.9 * temp) + 0.1 * temp - 112;
var expIndex = 5417.753 * ((1 / 273.16) - (1 / (dewPoint + 273.16)));
var humidex = Math.floor(temp + 0.5555 * (6.11 * Math.exp(expIndex) - 10));


msg.topic = "Humidex";
msg.payload = humidex;

hum = parseInt(bedroomHumidity);
temp = parseInt(bedroomTemp);
dewPoint = Math.pow(hum/100, 1 / 8) * (112 + 0.9 * temp) + 0.1 * temp - 112;
expIndex = 5417.753 * ((1 / 273.16) - (1 / (dewPoint + 273.16)));
humidex = Math.floor(temp + 0.5555 * (6.11 * Math.exp(expIndex) - 10));

var msg2 = { topic : "Humidex", payload : humidex };

return [msg,msg2];