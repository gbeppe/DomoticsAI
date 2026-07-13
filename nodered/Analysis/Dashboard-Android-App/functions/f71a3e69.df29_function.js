var msgAC = { payload : 0 };
var msgHP = { payload : 0 };
var HPStatus = { payload: "on" };

if (msg.payload == "stop"){
    HPStatus.payload = "off";
} else if (msg.payload == "eco16heat"){
    msgHP.payload = 16;
} else if (msg.payload == "eco17heat"){
    msgHP.payload = 17;
} else if (msg.payload == "eco18heat"){
    msgHP.payload = 18;
} else if (msg.payload == "eco19heat"){
    msgHP.payload = 19;
} else if (msg.payload == "eco20heat"){
    msgHP.payload = 20;
} else if (msg.payload == "eco21heat"){
    msgHP.payload = 21;
} else if (msg.payload == "eco22heat"){
    msgHP.payload = 22;
} else if (msg.payload == "OnAutoAuto23OffOff"){
    msgAC.payload = 23;
} else if (msg.payload == "OnAutoAuto24OffOff"){
    msgAC.payload = 24;
} else if (msg.payload == "OnAutoAuto25OffOff"){
    msgAC.payload = 25;
}


return [msgAC,msgHP,HPStatus];