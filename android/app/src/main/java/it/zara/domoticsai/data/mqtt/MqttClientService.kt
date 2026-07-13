package it.zara.domoticsai.data.mqtt

import com.hivemq.client.mqtt.MqttClient
import com.hivemq.client.mqtt.MqttGlobalPublishFilter
import com.hivemq.client.mqtt.datatypes.MqttQos
import com.hivemq.client.mqtt.mqtt3.Mqtt3AsyncClient
import it.zara.domoticsai.domain.model.BrokerEndpoint
import it.zara.domoticsai.domain.model.ConnectionState
import it.zara.domoticsai.domain.model.LogEntry
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.flow.asStateFlow
import java.nio.charset.StandardCharsets
import java.util.UUID

class MqttClientService {
    private var client: Mqtt3AsyncClient? = null

    private val _connectionState = MutableStateFlow(ConnectionState.DISCONNECTED)
    val connectionState = _connectionState.asStateFlow()

    private val _messages = MutableSharedFlow<Pair<String, String>>(extraBufferCapacity = 128)
    val messages = _messages.asSharedFlow()

    private val _logs = MutableSharedFlow<LogEntry>(extraBufferCapacity = 256)
    val logs = _logs.asSharedFlow()

    fun connect(endpoint: BrokerEndpoint, remote: Boolean, onResult: (Boolean) -> Unit) {
        disconnect()
        _connectionState.value = ConnectionState.CONNECTING
        log("SYSTEM", "CONNECT", "${endpoint.host}:${endpoint.port}")

        val builder = MqttClient.builder()
            .identifier("domoticsai-android-${UUID.randomUUID()}")
            .serverHost(endpoint.host)
            .serverPort(endpoint.port)
            .useMqttVersion3()

        val newClient = builder.buildAsync()
        client = newClient

        newClient.publishes(MqttGlobalPublishFilter.ALL) { publish ->
            val topic = publish.topic.toString()
            val payload = StandardCharsets.UTF_8.decode(publish.payload.orElse(null)).toString()
            _messages.tryEmit(topic to payload)
            log("RX", topic, payload)
        }

        val connectBuilder = newClient.connectWith()
            .cleanSession(true)
            .keepAlive(30)

        if (endpoint.username.isNotBlank()) {
            connectBuilder.simpleAuth()
                .username(endpoint.username)
                .password(endpoint.password.toByteArray(StandardCharsets.UTF_8))
                .applySimpleAuth()
        }

        connectBuilder.send().whenComplete { _, error ->
            if (error != null) {
                _connectionState.value = ConnectionState.ERROR
                log("ERROR", "CONNECT", error.message ?: error.javaClass.simpleName)
                onResult(false)
            } else {
                _connectionState.value =
                    if (remote) ConnectionState.CONNECTED_REMOTE else ConnectionState.CONNECTED_LOCAL
                newClient.subscribeWith()
                    .topicFilter("domoticsai/v1/#")
                    .qos(MqttQos.AT_LEAST_ONCE)
                    .send()
                    .whenComplete { _, subscribeError ->
                        if (subscribeError != null) {
                            log("ERROR", "SUBSCRIBE", subscribeError.message ?: "Subscribe failed")
                            onResult(false)
                        } else {
                            log("SYSTEM", "SUBSCRIBE", "domoticsai/v1/#")
                            onResult(true)
                        }
                    }
            }
        }
    }

    fun disconnect() {
        val old = client
        client = null
        if (old != null) {
            runCatching { old.disconnect() }
            log("SYSTEM", "DISCONNECT", "Requested")
        }
        _connectionState.value = ConnectionState.DISCONNECTED
    }

    private fun log(direction: String, topic: String, payload: String) {
        _logs.tryEmit(
            LogEntry(
                timestampEpochMs = System.currentTimeMillis(),
                direction = direction,
                topic = topic,
                payload = payload.take(500)
            )
        )
    }
}
