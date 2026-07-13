// Lettura persistente dal File System
let min_run = parseFloat(global.get("user_min_run_time", "file"));
let min_off = parseFloat(global.get("user_min_off_time", "file"));
let target_h = parseFloat(global.get("user_target_humidex_estate", "file"));
let vmc_notte = parseFloat(global.get("user_vmc_max_notte", "file"));
let deficit_tol = parseFloat(global.get("user_deficit_tolerance_time", "file")); // Nuova variabile

let ai_enabled = flow.get("AI_climate_enabling", "file");
if (ai_enabled === "true") ai_enabled = true;
if (ai_enabled === "false") ai_enabled = false;
if (typeof ai_enabled !== "boolean") ai_enabled = true;

let msgs = [];

// Accodamento messaggi per aggiornare la UI
if (!isNaN(min_run)) msgs.push({ payload: min_run, topic: "casa/clima/cmnd/min_run_time" });
if (!isNaN(min_off)) msgs.push({ payload: min_off, topic: "casa/clima/cmnd/min_off_time" });
if (!isNaN(target_h)) msgs.push({ payload: target_h, topic: "casa/clima/cmnd/target_humidex" });
if (!isNaN(vmc_notte)) msgs.push({ payload: vmc_notte, topic: "casa/clima/cmnd/vmc_max_notte" });
if (!isNaN(deficit_tol)) msgs.push({ payload: deficit_tol, topic: "casa/clima/cmnd/deficit_tolerance_time" });

msgs.push({ payload: ai_enabled, topic: "AI_climate_enabling" });

return [msgs];