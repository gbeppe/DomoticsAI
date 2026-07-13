var res = msg.payload.split(":");

if (res[1] == "00") res[1] = 0;

var out1 = { payload : res[0] };
var out2 = { payload : res[1] };
return [out1, out2];