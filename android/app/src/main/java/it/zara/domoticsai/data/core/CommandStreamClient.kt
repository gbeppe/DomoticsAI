package it.zara.domoticsai.data.core

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.SocketTimeoutException
import java.net.URL

class CommandStreamClient {

    suspend fun connect(
        baseUrl: String,
        onConnected: () -> Unit,
        onDisconnected: () -> Unit,
        onEvent: (JSONObject) -> Unit
    ) = withContext(Dispatchers.IO) {
        val url =
            "${baseUrl.trimEnd('/')}" +
                "/api/v1/commands/stream"

        val connection =
            URL(url).openConnection()
                as HttpURLConnection

        try {
            connection.requestMethod = "GET"
            connection.connectTimeout = 5_000

            /*
             * Il Core Engine invia un keep-alive ogni 20 secondi.
             * Un timeout di 35 secondi permette di rilevare
             * connessioni interrotte senza lasciare il client
             * bloccato indefinitamente.
             */
            connection.readTimeout = 25_000

            connection.setRequestProperty(
                "Accept",
                "text/event-stream"
            )
            connection.setRequestProperty(
                "Cache-Control",
                "no-cache"
            )

            val responseCode =
                connection.responseCode

            if (responseCode !in 200..299) {
                error(
                    "SSE HTTP $responseCode"
                )
            }

            onConnected()

            connection.inputStream
                .bufferedReader()
                .useLines { lines ->
                    lines.forEach { line ->
                        if (
                            line.startsWith(
                                "data: "
                            )
                        ) {
                            val payload =
                                line.removePrefix(
                                    "data: "
                                ).trim()

                            /*
                             * L'evento ready contiene {} e
                             * non richiede un refresh.
                             */
                            if (
                                payload.isNotBlank() &&
                                payload != "{}"
                            ) {
                                onEvent(
                                    JSONObject(payload)
                                )
                            }
                        }
                    }
                }

        } catch (error: SocketTimeoutException) {
            /*
             * Il ciclo del ViewModel eseguirà
             * automaticamente la riconnessione.
             */
            throw error

        } finally {
            connection.disconnect()
            onDisconnected()
        }
    }
}
