// Inizializza il contesto per memorizzare i dati delle stanze se non esiste già
let stanze = context.get('stanze') || {
    stanza1: { temp: null, hum: null },
    stanza2: { temp: null, hum: null }
};

// Funzione matematica per calcolare l'Humidex
function calcolaHumidex(temp, hum) {
    // Formula basata sul punto di rugiada (Dew Point) e pressione di vapore
    let e = 6.11 * Math.exp(5417.7530 * (1/273.16 - 1/(273.15 + temp)));
    let h = temp + (5/9) * (((hum/100) * e) - 10);
    return Math.round(h * 10) / 10; // Arrotonda a un decimale
}

let msgStanza1 = null;
let msgStanza2 = null;

// Riconoscimento del topic in ingresso
switch (msg.topic) {
    // --- STANZA 1 ---
    case "emon/emonth5/temperature_calibrated":
        stanze.stanza1.temp = parseFloat(msg.payload);
        break;
    case "emon/emonth5/humidity":
        stanze.stanza1.hum = parseFloat(msg.payload);
        break;

    // --- STANZA 2 ---
    case "emon/cameraMatrimoniale/temperature":
        stanze.stanza2.temp = parseFloat(msg.payload);
        break;
    case "emon/cameraMatrimoniale/humidity":
        stanze.stanza2.hum = parseFloat(msg.payload);
        break;
}

// Salva lo stato aggiornato nel contesto del nodo
context.set('stanze', stanze);

// Se la Stanza 1 ha entrambi i dati, calcola l'Humidex
if (stanze.stanza1.temp !== null && stanze.stanza1.hum !== null) {
    msgStanza1 = {
        topic: "casa/stanza1/humidex",
        payload: calcolaHumidex(stanze.stanza1.temp, stanze.stanza1.hum)
    };
}

// Se la Stanza 2 ha entrambi i dati, calcola l'Humidex
if (stanze.stanza2.temp !== null && stanze.stanza2.hum !== null) {
    msgStanza2 = {
        topic: "casa/cameraMatrimoniale/humidex",
        payload: calcolaHumidex(stanze.stanza2.temp, stanze.stanza2.hum)
    };
}

// Restituisce un array con i messaggi destinati alle rispettive uscite [Uscita 1, Uscita 2]
return [msgStanza1, msgStanza2];
return msg;