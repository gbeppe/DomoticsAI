package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.CoreHealth
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

    private fun requestJson(url: String): String {
        val connection =
            URL(url).openConnection() as HttpURLConnection

        return try {
            connection.requestMethod = "GET"
            connection.connectTimeout = 3_000
            connection.readTimeout = 5_000
            connection.setRequestProperty(
                "Accept",
                "application/json"
            )

            val code = connection.responseCode
            val stream =
                if (code in 200..299) {
                    connection.inputStream
                } else {
                    connection.errorStream
                }

            val body =
                stream.bufferedReader().use {
                    it.readText()
                }

            if (code !in 200..299) {
                error("HTTP $code: $body")
            }

            body
        } finally {
            connection.disconnect()
        }
    }
}
