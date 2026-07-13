let database = context.get("database_medie_storiche", "file") || { 
    medie_consumi: { ESTATE: { GIORNO: 600, NOTTE: 400 }, INVERNO: { GIORNO: 800, NOTTE: 500 } }, 
    efficienza_ricarica_storica: { ESTATE: 0.45, INVERNO: 0.30 } 
};

let adesso = Date.now();
let ultimoCalcoloOrario = context.get("ultimo_calcolo_orario", "file");

if (!ultimoCalcoloOrario) {
    ultimoCalcoloOrario = adesso;
    context.set("ultimo_calcolo_orario", adesso, "file");
}

if (msg.topic === "TeslaPowerwall/load_instant_power") {
    flow.set("consumo_istantaneo_registratore", parseFloat(msg.payload));
} else if (msg.topic === "TeslaPowerwall/solar_instant_power") {
    flow.set("produzione_istantanea_registratore", parseFloat(msg.payload));
}

let consumoAttuale = flow.get("consumo_istantaneo_registratore") || 0;
let produzioneAttuale = flow.get("produzione_istantanea_registratore") || 0;
let potenzaInBatteria = (produzioneAttuale > consumoAttuale) ? (produzioneAttuale - consumoAttuale) : 0;

let accumuloConsumo = context.get("accumulo_consumo_ora", "file") || 0;
let accumuloCaricaBat = context.get("accumulo_carica_bat_ora", "file") || 0;
let accumuloProduzione = context.get("accumulo_produzione_ora", "file") || 0;
let lettureOra = context.get("contatore_letture_ora", "file") || 0;

accumuloConsumo += consumoAttuale;
accumuloCaricaBat += potenzaInBatteria;
accumuloProduzione += produzioneAttuale;
lettureOra++;

context.set("accumulo_consumo_ora", accumuloConsumo, "file");
context.set("accumulo_carica_bat_ora", accumuloCaricaBat, "file");
context.set("accumulo_produzione_ora", accumuloProduzione, "file");
context.set("contatore_letture_ora", lettureOra, "file");

if (adesso - ultimoCalcoloOrario >= 3600000) {
    let ora = new Date().getHours();
    let mese = new Date().getMonth();
    let stagione = (mese >= 4 && mese <= 8) ? "ESTATE" : "INVERNO";
    let fascia = (ora >= 22 || ora < 5) ? "NOTTE" : "GIORNO";
    let dataOraFormattata = new Intl.DateTimeFormat('it-IT', { 
        timeZone: 'Europe/Rome', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false 
    }).format(new Date(adesso));

    let consumoMedioOra = accumuloConsumo / lettureOra;
    let produzioneMediaOra = accumuloProduzione / lettureOra;
    let caricaMediaOra = accumuloCaricaBat / lettureOra;
    let efficienzaOraCalcolata = -1;
    let alpha = 0.05;

    database.medie_consumi[stagione][fascia] = Math.round((database.medie_consumi[stagione][fascia] * (1 - alpha)) + (consumoMedioOra * alpha));

    if (fascia === "GIORNO" && produzioneMediaOra > 100) {
        efficienzaOraCalcolata = parseFloat((caricaMediaOra / produzioneMediaOra).toFixed(3));
        if (efficienzaOraCalcolata >= 0 && efficienzaOraCalcolata <= 1) {
            database.efficienza_ricarica_storica[stagione] = parseFloat(((database.efficienza_ricarica_storica[stagione] * (1 - alpha)) + (efficienzaOraCalcolata * alpha)).toFixed(3));
        }
    }

    context.set("database_medie_storiche", database, "file");
    context.set("ultimo_calcolo_orario", adesso, "file");

    flow.set("tutte_medie_storiche", database.medie_consumi);
    flow.set("efficienza_ricarica_storica", database.efficienza_ricarica_storica);

    let payloadLogStime = {
        timestamp: adesso, data_ora: dataOraFormattata, stagione: stagione, fascia_oraria: fascia, conteggio_letture: lettureOra,
        metriche_medie_ora: { consumo_medio_w: Math.round(consumoMedioOra), produzione_media_w: Math.round(produzioneMediaOra), carica_media_batteria_w: Math.round(caricaMediaOra) },
        calcolo_efficienza: { efficienza_ora_istantanea: efficienzaOraCalcolata, nuova_efficienza_storica_ema: database.efficienza_ricarica_storica[stagione] },
        database_medie_consumi_attuale: { giorno: database.medie_consumi[stagione].GIORNO, notte: database.medie_consumi[stagione].NOTTE }
    };

    context.set("accumulo_consumo_ora", 0, "file");
    context.set("accumulo_carica_bat_ora", 0, "file");
    context.set("accumulo_produzione_ora", 0, "file");
    context.set("contatore_letture_ora", 0, "file");

    msg.payload = payloadLogStime;
    msg.topic = "casa/clima/log_database";
    return msg;
}
return null;