package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.EnergyDashboardState
import it.zara.domoticsai.domain.model.EnergyDerivedState
import it.zara.domoticsai.domain.model.EnergyState
import org.json.JSONObject

object EnergyParser {

    fun parse(json: String): EnergyDashboardState {
        val root = JSONObject(json)
        val raw = root.optJSONObject("raw") ?: JSONObject()
        val derived =
            root.optJSONObject("derived") ?: JSONObject()

        return EnergyDashboardState(
            raw = EnergyState(
                solarPowerW = valueOf(raw, "solar_power_w"),
                homeLoadW = valueOf(raw, "home_load_w"),
                gridPowerW = valueOf(raw, "grid_power_w"),
                batteryPowerW = valueOf(
                    raw,
                    "battery_power_w"
                ),
                powerwallSocPct = valueOf(
                    raw,
                    "powerwall_soc_pct"
                )
            ),
            derived = EnergyDerivedState(
                gridDirection = textOf(
                    derived,
                    "grid_direction"
                ),
                batteryDirection = textOf(
                    derived,
                    "battery_direction"
                ),
                gridImportW = valueOf(
                    derived,
                    "grid_import_w"
                ),
                gridExportW = valueOf(
                    derived,
                    "grid_export_w"
                ),
                batteryChargeW = valueOf(
                    derived,
                    "battery_charge_w"
                ),
                batteryDischargeW = valueOf(
                    derived,
                    "battery_discharge_w"
                ),
                selfConsumptionPct = valueOf(
                    derived,
                    "self_consumption_pct"
                ),
                selfSufficiencyPct = valueOf(
                    derived,
                    "self_sufficiency_pct"
                ),
                balanceErrorW = valueOf(
                    derived,
                    "balance_error_w"
                ),
                operatingMode = textOf(
                    derived,
                    "operating_mode"
                )
            )
        )
    }

    private fun valueOf(
        domain: JSONObject,
        entity: String
    ): Double? {
        val item = domain.optJSONObject(entity)
            ?: return null

        if (!item.has("value") || item.isNull("value")) {
            return null
        }

        return when (val value = item.opt("value")) {
            is Number -> value.toDouble()
            is String -> value.toDoubleOrNull()
            else -> null
        }
    }

    private fun textOf(
        domain: JSONObject,
        entity: String
    ): String {
        val item = domain.optJSONObject(entity)
            ?: return "unknown"

        return item.optString("value", "unknown")
    }
}
