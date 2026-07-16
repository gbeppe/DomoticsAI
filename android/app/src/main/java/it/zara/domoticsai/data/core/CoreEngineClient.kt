package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.CommandReceiptDto
import it.zara.domoticsai.domain.model.CommandHistoryItem
import it.zara.domoticsai.domain.model.CoreHealth
import it.zara.domoticsai.domain.model.HouseDecisionItem
import it.zara.domoticsai.domain.model.HouseDecisionKind
import it.zara.domoticsai.domain.model.HouseDecisionsResult
import it.zara.domoticsai.domain.model.HouseContextItem
import it.zara.domoticsai.domain.model.HouseContextsResult
import it.zara.domoticsai.domain.model.HomeIntelligenceSnapshot
import it.zara.domoticsai.domain.model.HomeIntelligenceSummary
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

    fun fetchClimate(baseUrl: String): String =
        requestJson(
            "${baseUrl.trimEnd('/')}/api/v1/climate"
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
            message =
                if (
                    !obj.has("error") ||
                    obj.isNull("error")
                ) {
                    null
                } else {
                    obj.optString("error")
                        .takeIf {
                            it.isNotBlank() &&
                                !it.equals(
                                    "null",
                                    ignoreCase = true
                                )
                        }
                }
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
            message =
                if (
                    !command.has("error") ||
                    command.isNull("error")
                ) {
                    null
                } else {
                    command.optString("error")
                        .takeIf {
                            it.isNotBlank() &&
                                !it.equals(
                                    "null",
                                    ignoreCase = true
                                )
                        }
                }
        )
    }

    fun fetchCommands(
        baseUrl: String
    ): List<CommandHistoryItem> {
        val root = JSONObject(
            requestJson(
                "${baseUrl.trimEnd('/')}/api/v1/commands"
            )
        )
        val items = root.optJSONArray("items")
            ?: return emptyList()

        return buildList {
            for (index in 0 until items.length()) {
                val item = items.optJSONObject(index)
                    ?: continue
                add(CommandJson.parseHistoryItem(item))
            }
        }
    }

    private fun parseHouseContext(
        item: JSONObject
    ): HouseContextItem {
        val dataObject =
            item.optJSONObject("data")
                ?: JSONObject()

        return HouseContextItem(
            name =
                item.optString(
                    "name",
                    ""
                ),
            priority =
                item.optInt(
                    "priority",
                    0
                ),
            category =
                item.optString(
                    "category",
                    "house"
                ),
            confidence =
                item.optDouble(
                    "confidence",
                    1.0
                ),
            reasons =
                item.optJSONArray(
                    "reason"
                ).toStringList(),
            observedAt =
                item.optString(
                    "observedAt",
                    ""
                ).takeIf {
                    it.isNotBlank()
                        && !it.equals(
                            "null",
                            ignoreCase = true
                        )
                },
            data =
                dataObject.toStringMap()
        )
    }

    fun fetchHomeIntelligence(
        baseUrl: String
    ): HomeIntelligenceSnapshot {
        val root = JSONObject(
            requestJson(
                "${baseUrl.trimEnd('/')}/api/v1/home"
            )
        )

        val contextsArray =
            root.optJSONArray("contexts")

        val contexts =
            if (contextsArray == null) {
                emptyList()
            } else {
                buildList {
                    for (
                        index in 0 until
                            contextsArray.length()
                    ) {
                        val item =
                            contextsArray
                                .optJSONObject(index)
                                ?: continue

                        add(
                            parseHouseContext(
                                item
                            )
                        )
                    }
                }.sortedWith(
                    compareByDescending<
                        HouseContextItem
                    > {
                        it.priority
                    }.thenBy {
                        it.name
                    }
                )
            }

        val decisionsArray =
            root.optJSONArray("decisions")

        val decisions =
            if (decisionsArray == null) {
                emptyList()
            } else {
                buildList {
                    for (
                        index in 0 until
                            decisionsArray.length()
                    ) {
                        val item =
                            decisionsArray
                                .optJSONObject(index)
                                ?: continue

                        add(
                            parseHouseDecision(
                                item
                            )
                        )
                    }
                }.sortedWith(
                    compareByDescending<
                        HouseDecisionItem
                    > {
                        it.priority
                    }.thenBy {
                        it.action
                    }
                )
            }

        val summaryObject =
            root.optJSONObject("summary")
                ?: JSONObject()

        return HomeIntelligenceSnapshot(
            generatedAt =
                root.optNullableString(
                    "generatedAt"
                ),
            knowledgeUpdatedAt =
                root.optNullableString(
                    "knowledgeUpdatedAt"
                ),
            contexts = contexts,
            decisions = decisions,
            summary =
                HomeIntelligenceSummary(
                    activeContexts =
                        summaryObject.optInt(
                            "activeContexts",
                            contexts.size
                        ),
                    activeDecisions =
                        summaryObject.optInt(
                            "activeDecisions",
                            decisions.size
                        ),
                    warnings =
                        summaryObject.optInt(
                            "warnings",
                            0
                        ),
                    recommendations =
                        summaryObject.optInt(
                            "recommendations",
                            0
                        ),
                    information =
                        summaryObject.optInt(
                            "information",
                            0
                        )
                ),
            executionEnabled =
                root.optBoolean(
                    "executionEnabled",
                    false
                )
        )
    }

    fun fetchActiveContexts(
        baseUrl: String
    ): HouseContextsResult {
        val root = JSONObject(
            requestJson(
                "${baseUrl.trimEnd('/')}/api/v1/context/active"
            )
        )

        val array =
            root.optJSONArray("contexts")
                ?: return HouseContextsResult(
                    contexts = emptyList()
                )

        val contexts = buildList {
            for (
                index in 0 until array.length()
            ) {
                val item =
                    array.optJSONObject(index)
                        ?: continue
                add(
                    parseHouseContext(
                        item
                    )
                )
        }
        }.sortedWith(
            compareByDescending<
                HouseContextItem
            > {
                it.priority
            }.thenBy {
                it.name
            }
        )

        return HouseContextsResult(
            contexts = contexts
        )
    }

    fun fetchDecisions(
        baseUrl: String
    ): HouseDecisionsResult {
        val root = JSONObject(
            requestJson(
                "${baseUrl.trimEnd('/')}/api/v1/decisions"
            )
        )

        val executionEnabled =
            root.optBoolean(
                "executionEnabled",
                false
            )

        val array =
            root.optJSONArray("decisions")

        if (array == null) {
            return HouseDecisionsResult(
                decisions = emptyList(),
                executionEnabled =
                    executionEnabled
            )
        }

        val decisions = buildList {
            for (
                index in 0 until array.length()
            ) {
                val item =
                    array.optJSONObject(index)
                        ?: continue

                add(
                    parseHouseDecision(
                        item
                    )
                )
            }
        }.sortedWith(
            compareByDescending<
                HouseDecisionItem
            > {
                it.priority
            }.thenBy {
                it.action
            }
        )

        return HouseDecisionsResult(
            decisions = decisions,
            executionEnabled =
                executionEnabled
        )
    }

    private fun parseHouseDecision(
        item: JSONObject
    ): HouseDecisionItem {
        val data =
            item.optJSONObject("data")
                ?: JSONObject()

        return HouseDecisionItem(
            decisionId =
                item.optString(
                    "decision_id",
                    ""
                ),
            ruleId =
                item.optString(
                    "rule_id",
                    ""
                ),
            kind =
                parseDecisionKind(
                    item.optString(
                        "kind",
                        ""
                    )
                ),
            action =
                item.optString(
                    "action",
                    ""
                ),
            title =
                item.optString(
                    "title",
                    "Suggerimento"
                ),
            description =
                item.optString(
                    "description",
                    ""
                ),
            priority =
                item.optInt(
                    "priority",
                    0
                ),
            confidence =
                item.optDouble(
                    "confidence",
                    1.0
                ),
            reasons =
                item.optJSONArray("reason")
                    .toStringList(),
            contextNames =
                item.optJSONArray(
                    "context_names"
                ).toStringList(),
            executionAllowed =
                data.optBoolean(
                    "executionAllowed",
                    false
                ),
            requiresConfirmation =
                data.optBoolean(
                    "requiresConfirmation",
                    true
                ),
            suggestedAction =
                data.optString(
                    "suggestedAction",
                    ""
                ).takeIf {
                    it.isNotBlank()
                },
            createdAt =
                item.optString(
                    "created_at",
                    ""
                )
        )
    }

    private fun parseDecisionKind(
        value: String
    ): HouseDecisionKind =
        when (
            value.trim().lowercase()
        ) {
            "recommendation" ->
                HouseDecisionKind.RECOMMENDATION

            "warning" ->
                HouseDecisionKind.WARNING

            "information" ->
                HouseDecisionKind.INFORMATION

            else ->
                HouseDecisionKind.UNKNOWN
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

private fun org.json.JSONArray?.toStringList(): List<String> {
    if (this == null) {
        return emptyList()
    }

    return buildList {
        for (index in 0 until length()) {
            val value =
                optString(
                    index,
                    ""
                )

            if (value.isNotBlank()) {
                add(value)
            }
        }
    }
}

private fun JSONObject.toStringMap(): Map<String, String> =
    buildMap {
        val names = keys()

        while (names.hasNext()) {
            val name = names.next()
            val value = opt(name)

            if (
                value != null
                && value != JSONObject.NULL
            ) {
                put(
                    name,
                    value.toString()
                )
            }
        }
    }

private fun JSONObject.optNullableString(
    name: String
): String? {
    if (
        !has(name)
        || isNull(name)
    ) {
        return null
    }

    return optString(
        name,
        ""
    ).takeIf {
        it.isNotBlank()
            && !it.equals(
                "null",
                ignoreCase = true
            )
    }
}
