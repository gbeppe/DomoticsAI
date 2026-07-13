// Seleziona gli ultimi 7 giorni con tutti i nuovi parametri energetici e ambientali
msg.topic = `SELECT 
                DATE_FORMAT(timestamp_evento, '%Y-%m-%d %H:%i') as data_ora, 
                comando_ir, 
                stato_ac, 
                modalita, 
                temp_impostata, 
                temp_rilevata as temp_living, 
                humidex,
                vmc_velocita,
                humidex_living,
                humidex_bedroom,
                batteria_soc,
                temp_camera,
                temp_esterno,
                surplus_w
             FROM storico_clima 
             WHERE timestamp_evento >= DATE_SUB(NOW(), INTERVAL 7 DAY) 
             ORDER BY timestamp_evento DESC;`;
return msg;