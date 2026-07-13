switch(msg.topic) {
    case 'emon/emontx3/power1':
        global.set('gridPower', parseInt(msg.payload));
    break;
    case 'emon/emontx3/power2':
        global.set('solarPower', parseInt(msg.payload));
    break;
}

gridPower  = global.get('gridPower')||0;
solarPower = global.get('solarPower')||0;

homePower = solarPower + gridPower;
global.set('homePower',homePower);

msg.topic = "Consumo";
msg.payload = global.get('homePower')||0;

return msg;