package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.CommandHistoryItem
import it.zara.domoticsai.domain.model.UiCommandState
import org.json.JSONObject

object CommandJson {
    fun nullableString(obj: JSONObject, name: String): String? {
        if (!obj.has(name) || obj.isNull(name)) return null
        return obj.optString(name).takeIf {
            it.isNotBlank() && !it.equals("null", ignoreCase = true)
        }
    }

    fun parseState(value: String): UiCommandState =
        when (value.lowercase()) {
            "created", "validated", "queued", "sent" ->
                UiCommandState.SENDING
            "waiting_confirmation" -> UiCommandState.WAITING_CONFIRMATION
            "simulated" -> UiCommandState.SIMULATED
            "confirmed" -> UiCommandState.CONFIRMED
            "rejected" -> UiCommandState.REJECTED
            "timeout" -> UiCommandState.TIMEOUT
            "failed" -> UiCommandState.FAILED
            else -> UiCommandState.IDLE
        }

    fun parseHistoryItem(obj: JSONObject) = CommandHistoryItem(
        commandId = obj.optString("command_id"),
        domain = obj.optString("domain"),
        action = obj.optString("action"),
        target = obj.optString("target"),
        source = obj.optString("source"),
        state = parseState(obj.optString("state")),
        createdAt = obj.optString("created_at"),
        updatedAt = obj.optString("updated_at"),
        mode = obj.optString("mode"),
        error = nullableString(obj, "error")
    )
}
