package it.zara.domoticsai.domain.model

enum class EnergyDataSource {
    CORE_ENGINE,
    MQTT_FALLBACK,
    NONE
}

data class EnergyDerivedState(
    val gridDirection: String = "unknown",
    val batteryDirection: String = "unknown",
    val gridImportW: Double? = null,
    val gridExportW: Double? = null,
    val batteryChargeW: Double? = null,
    val batteryDischargeW: Double? = null,
    val selfConsumptionPct: Double? = null,
    val selfSufficiencyPct: Double? = null,
    val balanceErrorW: Double? = null,
    val operatingMode: String = "unknown"
)

data class EnergyDashboardState(
    val loading: Boolean = false,
    val raw: EnergyState = EnergyState(),
    val derived: EnergyDerivedState = EnergyDerivedState(),
    val source: EnergyDataSource = EnergyDataSource.NONE,
    val error: String? = null
)
