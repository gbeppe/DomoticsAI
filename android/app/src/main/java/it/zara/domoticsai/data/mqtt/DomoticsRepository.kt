package it.zara.domoticsai.data.mqtt

import it.zara.domoticsai.data.settings.SettingsRepository
import it.zara.domoticsai.domain.model.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import org.json.JSONObject

class DomoticsRepository(
    private val mqttClientService: MqttClientService,
    private val settingsRepository: SettingsRepository
) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    private val _homeState = MutableStateFlow(HomeState())
    val homeState = _homeState.asStateFlow()
    val connectionState = mqttClientService.connectionState

    private val _logs = MutableStateFlow<List<LogEntry>>(emptyList())
    val logs = _logs.asStateFlow()

    init {
        scope.launch {
            mqttClientService.messages.collect { (topic, payload) ->
                consumeMessage(topic, payload)
            }
        }
        scope.launch {
            mqttClientService.logs.collect { entry ->
                _logs.update { (listOf(entry) + it).take(500) }
            }
        }
    }

    fun connect(settings: ConnectionSettings, credentials: Map<String, Pair<String, String>> = emptyMap()) {
        scope.launch {
            when (settings.mode) {
                ConnectionMode.LOCAL_ONLY -> connectEndpoint(settings.local, false, credentials["local"])
                ConnectionMode.REMOTE_ONLY -> connectEndpoint(settings.remote, true, credentials["remote"])
                ConnectionMode.AUTO -> {
                    val localOk = connectEndpointAwait(settings.local, false, credentials["local"])
                    if (!localOk && settings.remote.host.isNotBlank()) {
                        connectEndpoint(settings.remote, true, credentials["remote"])
                    }
                }
            }
        }
    }

    fun disconnect() = mqttClientService.disconnect()

    private fun connectEndpoint(
        endpoint: BrokerEndpoint,
        remote: Boolean,
        credentials: Pair<String, String>?
    ) {
        if (endpoint.host.isBlank()) return
        mqttClientService.connect(
            endpoint.copy(
                username = credentials?.first.orEmpty(),
                password = credentials?.second.orEmpty()
            ),
            remote
        ) { }
    }

    private suspend fun connectEndpointAwait(
        endpoint: BrokerEndpoint,
        remote: Boolean,
        credentials: Pair<String, String>?
    ): Boolean = suspendCancellableCoroutine { continuation ->
        if (endpoint.host.isBlank()) {
            continuation.resume(false) {}
            return@suspendCancellableCoroutine
        }
        mqttClientService.connect(
            endpoint.copy(
                username = credentials?.first.orEmpty(),
                password = credentials?.second.orEmpty()
            ),
            remote
        ) { ok ->
            if (continuation.isActive) continuation.resume(ok) {}
        }
    }

    private fun consumeMessage(topic: String, payload: String) {
        val value = parseValue(payload) ?: return
        _homeState.update { old ->
            val updated = when (topic) {
                "domoticsai/v1/state/energy/solar_power_w" ->
                    old.copy(energy = old.energy.copy(solarPowerW = value))
                "domoticsai/v1/state/energy/home_load_w" ->
                    old.copy(energy = old.energy.copy(homeLoadW = value))
                "domoticsai/v1/state/energy/powerwall_soc_pct" ->
                    old.copy(energy = old.energy.copy(powerwallSocPct = value))
                "domoticsai/v1/state/climate/living_temperature_c" ->
                    old.copy(climate = old.climate.copy(livingTemperatureC = value))
                "domoticsai/v1/state/climate/living_humidex" ->
                    old.copy(climate = old.climate.copy(livingHumidex = value))
                "domoticsai/v1/state/climate/bedroom_humidex" ->
                    old.copy(climate = old.climate.copy(bedroomHumidex = value))
                "domoticsai/v1/state/climate/ac_power_w" ->
                    old.copy(climate = old.climate.copy(acPowerW = value))
                "domoticsai/v1/state/vmc/speed" ->
                    old.copy(vmc = old.vmc.copy(speed = value.toInt()))
                else -> old
            }
            updated.copy(lastUpdateEpochMs = System.currentTimeMillis())
        }
    }

    private fun parseValue(payload: String): Double? =
        runCatching {
            if (payload.trim().startsWith("{")) {
                JSONObject(payload).optDouble("value")
            } else {
                payload.toDouble()
            }
        }.getOrNull()
}
