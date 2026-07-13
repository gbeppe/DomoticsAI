package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.ClimateState
import it.zara.domoticsai.domain.model.EnergyState
import it.zara.domoticsai.domain.model.HomeState
import it.zara.domoticsai.domain.model.VmcState
import org.json.JSONObject

object CoreTwinParser {

    fun parse(json: String): HomeState {
        val root = JSONObject(json)
        val domains = root.optJSONObject("domains") ?: JSONObject()

        val energy = domains.optJSONObject("energy")
        val climate = domains.optJSONObject("climate")
        val vmc = domains.optJSONObject("vmc")

        return HomeState(
            energy = EnergyState(
                solarPowerW = valueOf(energy, "solar_power_w"),
                homeLoadW = valueOf(energy, "home_load_w"),
                powerwallSocPct = valueOf(energy, "powerwall_soc_pct")
            ),
            climate = ClimateState(
                livingTemperatureC = valueOf(
                    climate,
                    "living_temperature_c"
                ),
                livingHumidex = valueOf(
                    climate,
                    "living_humidex"
                ),
                bedroomHumidex = valueOf(
                    climate,
                    "bedroom_humidex"
                ),
                acPowerW = valueOf(
                    climate,
                    "ac_power_w"
                )
            ),
            vmc = VmcState(
                speed = valueOf(vmc, "speed")?.toInt()
            ),
            lastUpdateEpochMs = System.currentTimeMillis()
        )
    }

    fun hasAnyValue(state: HomeState): Boolean =
        state.energy.solarPowerW != null ||
            state.energy.homeLoadW != null ||
            state.energy.powerwallSocPct != null ||
            state.climate.livingTemperatureC != null ||
            state.climate.livingHumidex != null ||
            state.climate.bedroomHumidex != null ||
            state.climate.acPowerW != null ||
            state.vmc.speed != null

    private fun valueOf(
        domain: JSONObject?,
        entity: String
    ): Double? {
        val entityObject = domain?.optJSONObject(entity) ?: return null
        if (!entityObject.has("value") || entityObject.isNull("value")) {
            return null
        }

        val value = entityObject.opt("value")

        return when (value) {
            is Number -> value.toDouble()
            is String -> value.toDoubleOrNull()
            else -> null
        }
    }
}
