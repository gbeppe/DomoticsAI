package it.zara.domoticsai.domain.model

enum class ConnectionMode {
    AUTO, LOCAL_ONLY, REMOTE_ONLY
}

enum class ConnectionState {
    DISCONNECTED, CONNECTING, CONNECTED_LOCAL, CONNECTED_REMOTE, ERROR
}

data class BrokerEndpoint(
    val host: String,
    val port: Int,
    val username: String = "",
    val password: String = ""
)

data class ConnectionSettings(
    val mode: ConnectionMode = ConnectionMode.AUTO,
    val local: BrokerEndpoint = BrokerEndpoint("192.168.1.40", 1883),
    val remote: BrokerEndpoint = BrokerEndpoint("", 1883)
)

data class EnergyState(
    val solarPowerW: Double? = null,
    val homeLoadW: Double? = null,
    val powerwallSocPct: Double? = null
)

data class ClimateState(
    val livingTemperatureC: Double? = null,
    val livingHumidex: Double? = null,
    val bedroomHumidex: Double? = null,
    val acPowerW: Double? = null
)

data class VmcState(
    val speed: Int? = null
)

data class HomeState(
    val energy: EnergyState = EnergyState(),
    val climate: ClimateState = ClimateState(),
    val vmc: VmcState = VmcState(),
    val lastUpdateEpochMs: Long? = null
)

data class LogEntry(
    val timestampEpochMs: Long,
    val direction: String,
    val topic: String,
    val payload: String
)
