msg.payload = msg.payload * -1;
if (msg.payload < 0) msg.payload = 0;
return msg;