let log = msg.payload.dettaglio_comandi;
let envv = msg.payload.condizioni_ambientali;
let energy = msg.payload.stato_energia; // <-- AGGIUNTO: Peschiamo lo stato energia

// Filtro di sicurezza
if (!log || !envv || !energy) return null;

// Formattazione data JS -> MySQL DATETIME
let dateObj = new Date(msg.payload.timestamp);
let tzOffset = (new Date()).getTimezoneOffset() * 60000;
let localISOTime = (new Date(dateObj.getTime() - tzOffset)).toISOString().slice(0, 19).replace('T', ' ');

let query = `INSERT INTO storico_clima 
    (timestamp_evento, comando_ir, stato_ac, modalita, temp_impostata, temp_rilevata, humidex, vmc_velocita, humidex_living, humidex_bedroom, batteria_soc, temp_camera, temp_esterno, surplus_w) 
    VALUES (
        '${localISOTime}', 
        '${log.comando_ir_inviato}', 
        '${log.stato_ac_attuale}', 
        '${log.modalita_aria}', 
        ${log.temperatura_impostata_c}, 
        ${envv.temperatura_c}, 
        ${envv.humidex},
        ${log.vmc_velocita_attuale},
        ${envv.humidex_living},
        ${envv.humidex_bedroom},
        ${energy.powerwall_soc_percent},
        ${envv.temp_cameraMatrimoniale},
        ${log.temperatura_esterna_c},
        ${energy.surplus_w}
    );`;

return { topic: query };