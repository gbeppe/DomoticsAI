package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.*
import org.json.JSONObject

object LightsParser {

    fun parse(json: String): LightsDashboardState {
        val root = JSONObject(json)
        val derived = root.optJSONObject("derived") ?: JSONObject()

        val devicesObject =
            derived.optJSONObject("devices")
                ?.opt("value") as? JSONObject
                ?: JSONObject()

        val devices = buildList {
            val keys = devicesObject.keys()

            while (keys.hasNext()) {
                val key = keys.next()
                val item = devicesObject.optJSONObject(key)
                    ?: continue

                add(
                    LightDevice(
                        id = item.optString(
                            "id",
                            key.substringAfter("/")
                        ),
                        label = item.optString(
                            "label",
                            key.substringAfter("/")
                        ),
                        area = parseArea(
                            item.optString("area")
                        ),
                        type = parseType(
                            item.optString("type")
                        ),
                        state = parseState(
                            item.optString("state")
                        ),
                        available =
                            item.optBoolean(
                                "available",
                                false
                            ),
                        quality =
                            item.optString(
                                "quality",
                                "unknown"
                            ),
                        timestamp =
                            item.optString(
                                "timestamp"
                            ).takeIf {
                                it.isNotBlank()
                            }
                    )
                )
            }
        }.sortedWith(
            compareBy<LightDevice>(
                { it.area.ordinal },
                { it.label.lowercase() }
            )
        )

        return LightsDashboardState(
            devices = devices,
            summary = LightsSummary(
                lightsOnTotal = intValue(
                    derived,
                    "lights_on_total"
                ),
                relaysOnTotal = intValue(
                    derived,
                    "relays_on_total"
                ),
                unknownTotal = intValue(
                    derived,
                    "unknown_total"
                ),
                internalOn = intValue(
                    derived,
                    "internal_on"
                ),
                internalTotal = intValue(
                    derived,
                    "internal_total"
                ),
                externalOn = intValue(
                    derived,
                    "external_on"
                ),
                externalTotal = intValue(
                    derived,
                    "external_total"
                ),
                poolOn = intValue(
                    derived,
                    "pool_on"
                ),
                poolTotal = intValue(
                    derived,
                    "pool_total"
                ),
                allAvailable = boolValue(
                    derived,
                    "all_available"
                )
            )
        )
    }

    private fun intValue(
        domain: JSONObject,
        entity: String
    ): Int =
        domain.optJSONObject(entity)
            ?.optInt("value", 0)
            ?: 0

    private fun boolValue(
        domain: JSONObject,
        entity: String
    ): Boolean =
        domain.optJSONObject(entity)
            ?.optBoolean("value", false)
            ?: false

    private fun parseArea(value: String): LightArea =
        when (value.lowercase()) {
            "internal" -> LightArea.INTERNAL
            "external" -> LightArea.EXTERNAL
            "pool" -> LightArea.POOL
            else -> LightArea.INTERNAL
        }

    private fun parseType(value: String): LightDeviceType =
        when (value.lowercase()) {
            "relay" -> LightDeviceType.RELAY
            else -> LightDeviceType.LIGHT
        }

    private fun parseState(value: String): LightState =
        when (value.uppercase()) {
            "ON" -> LightState.ON
            "OFF" -> LightState.OFF
            else -> LightState.UNKNOWN
        }
}
