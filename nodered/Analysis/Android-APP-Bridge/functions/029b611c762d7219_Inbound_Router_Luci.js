// ============================================================================
// INBOUND ROUTER LUCI
// Riceve i comandi on/off/scene. Supporta topic base dinamico.
// ============================================================================

let baseTopic = global.get("app_base_topic") || "zara/android/domotica";

// Estraiamo il nome del dispositivo usando un'Espressione Regolare.
// Cerca la stringa tra "/light/" e "/set"
let regexLight = new RegExp(`^${baseTopic}/light/([^/]+)/set$`);
let matchLight = msg.topic.match(regexLight);

let device = null;
let cmd = msg.payload.toString().toUpperCase();
let targetTopic = "";
let targetPayload = cmd;
let usaLinkInterno = false;

// Gestione speciale per le scene (che non passano per /light/)
if (msg.topic.includes("/scene/set")) {
    return [msg, null]; 
}

if (matchLight && matchLight[1]) {
    device = matchLight[1];
} else {
    return null; 
}

// Normalizzazione del comando
if (cmd === "TRUE" || cmd === "1") cmd = "ON";
if (cmd === "FALSE" || cmd === "0") cmd = "OFF";
targetPayload = cmd;

switch (device) {
    case "sala":
    case "libreria":
    case "luciPiscina":
    case "luciPedanaPiscina":
    case "skimmerPiscina":
    case "ingressoServizio":
    case "pompaPiscina":
    case "tavolinoLettura":
    case "lampadaHifi":
    case "televisione":
    case "portico":
    case "lavanderia":
        targetPayload = cmd.toLowerCase();
        usaLinkInterno = true;             
        break;
        
    case "esterno":
        targetTopic = "shellies/shelly1-esterno/relay/0/command";
        targetPayload = cmd.toLowerCase(); 
        break;
        
    case "cucina":
        targetTopic = "zigbee2mqtt/Luce_Cucina/set";
        targetPayload = { state: cmd };
        break;
        
    default:
        node.warn("Comando App ricevuto per luce non mappata: " + device);
        return null;
}

let messaggioInUscita = {
    topic: device,
    payload: targetPayload
};

if (targetTopic !== "") {
    messaggioInUscita.topic = targetTopic;
}

if (usaLinkInterno) {
    return [null, messaggioInUscita];
} else {
    return [messaggioInUscita, null];
}