const cmd = msg.payload;
const tempMatch = cmd.match(/\d+/);
const setpoint = tempMatch ? parseInt(tempMatch[0], 10) : 0;
const msgEmon = { payload: setpoint };

// RECUPERA IL DIZIONARIO DALLA MEMORIA GLOBALE
// (Caricato al boot dal nodo Template)
const irDictionary = global.get("ir_dictionary") || {};

let payloadRM = null;

if (irDictionary[cmd]) {
    payloadRM = irDictionary[cmd];
    payloadRM.action = "send";
} else {
    node.warn("Comando non riconosciuto nel dizionario IR o dizionario non inizializzato: " + cmd);
}

const msgRM = payloadRM ? { payload: payloadRM } : null;

// 3. USCITE MULTIPLE: [Broadlink, EmonCMS]
return [msgRM, msgEmon];