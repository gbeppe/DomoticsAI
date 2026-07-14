package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.CommandReceiptDto
import it.zara.domoticsai.domain.model.CoreHealth
import it.zara.domoticsai.domain.model.LightDevice
import it.zara.domoticsai.domain.model.LightState
import it.zara.domoticsai.domain.model.UiCommandState
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class CoreEngineClient {

    fun fetchHealth(baseUrl: String): CoreHealth {
        val json = requestJson("${baseUrl.trimEnd('/')}/health")
        val obj = JSONObject(json)

        return CoreHealth(
            status = obj.optString("status", "unknown"),
            mqttConnected = obj.optBoolean("mqttConnected", false),
            mqttBroker = obj.optString("mqttBroker", ""),
            mqttTopic = obj.optString("mqttTopic", ""),
            digitalTwinUpdatedAt = obj.optString(
                "digitalTwinUpdatedAt",
                ""
            )
        )
    }

    fun fetchTwin(baseUrl: String): String =
        JSONObject(
            requestJson(
                "${baseUrl.trimEnd('/')}/api/v1/twin"
            )
        ).toString(2)

    fun fetchEnergy(baseUrl: String): String =
        requestJson(
            "${baseUrl.trimEnd('/')}/api/v1/energy"
        )

    fun fetchLights(baseUrl: String): String =
        requestJson(
            "${baseUrl.trimEnd('/')}/api/v1/lights"
        )

    fun createLightCommand(
        baseUrl: String,
        device: LightDevice,
        desiredState: LightState
    ): CommandReceiptDto {
        val target =
            "${device.area.name.lowercase()}/${device.id}"

        val body = JSONObject()
            .put("domain", "lights")
            .put("action", "set_state")
            .put("target", target)
            .put(
                "parameters",
                JSONObject().put(
                    "state",
                    desiredState.name
                )
            )
            .put("source", "android")
            .put("timeout_seconds", 15)
            .toString()

        val response = requestJson(
            url =
                "${baseUrl.trimEnd('/')}/api/v1/commands",
            method = "POST",
            body = body
        )

        val obj = JSONObject(response)

        return CommandReceiptDto(
            commandId = obj.getString("command_id"),
            state = parseCommandState(
                obj.optString("state")
            ),
            message = obj.optString(
                "error"
            ).takeIf { it.isNotBlank() }
        )
    }

    fun fetchCommand(
        baseUrl: String,
        commandId: String
    ): CommandReceiptDto {
        val response = requestJson(
            "${baseUrl.trimEnd('/')}/api/v1/commands/$commandId"
        )

        val root = JSONObject(response)
        val command = root.getJSONObject("command")

        return CommandReceiptDto(
            commandId = commandId,
            state = parseCommandState(
                command.optString("state")
            ),
            message = command.optString(
                "error"
            ).takeIf { it.isNotBlank() }
        )
    }

    private fun parseCommandState(
        value: String
    ): UiCommandState =
        when (value.lowercase()) {
            "created",
            "validated",
            "queued",
            "sent" ->
                UiCommandState.SENDING

            "waiting_confirmation" ->
                UiCommandState.WAITING_CONFIRMATION

            "simulated" ->
                UiCommandState.SIMULATED

            "confirmed" ->
                UiCommandState.CONFIRMED

            "rejected" ->
                UiCommandState.REJECTED

            "timeout" ->
                UiCommandState.TIMEOUT

            "failed" ->
                UiCommandState.FAILED

            else ->
                UiCommandState.IDLE
        }

    private fun requestJson(
        url: String,
        method: String = "GET",
        body: String? = null
    ): String {
        val connection =
            URL(url).openConnection() as HttpURLConnection

        return try {
            connection.requestMethod = method
            connection.connectTimeout = 3_000
            connection.readTimeout = 5_000
            connection.setRequestProperty(
                "Accept",
                "application/json"
            )

            if (body != null) {
                connection.doOutput = true
                connection.setRequestProperty(
                    "Content-Type",
                    "application/json"
                )
                connection.outputStream
                    .bufferedWriter()
                    .use { it.write(body) }
            }

            val code = connection.responseCode
            val stream =
                if (code in 200..299) {
                    connection.inputStream
                } else {
                    connection.errorStream
                }

            val responseBody =
                stream.bufferedReader().use {
                    it.readText()
                }

            if (code !in 200..299) {
                error("HTTP $code: $responseBody")
            }

            responseBody
        } finally {
            connection.disconnect()
        }
    }
}
