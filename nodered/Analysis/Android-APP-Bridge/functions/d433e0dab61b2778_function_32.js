// Legge il valore in arrivo
let gridPower = parseFloat(msg.payload) || 0;

// Se il valore è tra -30W e +30W, lo forza a 0
if (Math.abs(gridPower) <= 30) {
    gridPower = 0;
}

// Passa il valore pulito al nodo MQTT
msg.payload = gridPower.toString();
return msg;