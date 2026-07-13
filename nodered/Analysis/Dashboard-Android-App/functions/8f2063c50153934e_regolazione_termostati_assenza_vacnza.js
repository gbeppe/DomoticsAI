var holiday = global.get("holiday", "file");

if (holiday === "false") msg.payload = "schedule-only";
else msg.payload ="stop";

return msg;