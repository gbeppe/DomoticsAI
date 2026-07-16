package it.zara.domoticsai.data.core

import it.zara.domoticsai.domain.model.ClimateBooleanMetric
import it.zara.domoticsai.domain.model.ClimateDashboardState
import it.zara.domoticsai.domain.model.ClimateEnvironmentState
import it.zara.domoticsai.domain.model.ClimateFireplaceState
import it.zara.domoticsai.domain.model.ClimateNumberMetric
import it.zara.domoticsai.domain.model.ClimateOutdoorState
import it.zara.domoticsai.domain.model.ClimateRoomState
import it.zara.domoticsai.domain.model.ClimateTextMetric
import it.zara.domoticsai.domain.model.ClimateThermalState
import it.zara.domoticsai.domain.model.ClimateThermostatState
import it.zara.domoticsai.domain.model.ClimateVentilationState
import org.json.JSONObject


object ClimateParser {

    fun parse(
        json: String
    ): ClimateDashboardState {
        val root = JSONObject(json)

        val environment =
            root.optJSONObject("environment")
                ?: JSONObject()

        val living =
            environment.optJSONObject("living")
                ?: JSONObject()

        val bedroom =
            environment.optJSONObject("bedroom")
                ?: JSONObject()

        val outdoor =
            environment.optJSONObject("outdoor")
                ?: JSONObject()

        val thermostat =
            root.optJSONObject("thermostat")
                ?: JSONObject()

        val ventilation =
            root.optJSONObject("ventilation")
                ?: JSONObject()

        val thermal =
            root.optJSONObject("thermal")
                ?: JSONObject()

        val fireplace =
            root.optJSONObject("fireplace")
                ?: JSONObject()

        val completeSnapshot =
            root.optJSONObject(
                "completeSnapshot"
            )

        return ClimateDashboardState(
            environment =
                ClimateEnvironmentState(
                    living =
                        ClimateRoomState(
                            temperature =
                                numberMetric(
                                    living,
                                    "temperature"
                                ),
                            humidity =
                                numberMetric(
                                    living,
                                    "humidity"
                                ),
                            humidex =
                                numberMetric(
                                    living,
                                    "humidex"
                                )
                        ),
                    bedroom =
                        ClimateRoomState(
                            temperature =
                                numberMetric(
                                    bedroom,
                                    "temperature"
                                ),
                            humidity =
                                numberMetric(
                                    bedroom,
                                    "humidity"
                                ),
                            humidex =
                                numberMetric(
                                    bedroom,
                                    "humidex"
                                )
                        ),
                    outdoor =
                        ClimateOutdoorState(
                            temperature =
                                numberMetric(
                                    outdoor,
                                    "temperature"
                                ),
                            humidity =
                                numberMetric(
                                    outdoor,
                                    "humidity"
                                )
                        )
                ),
            thermostat =
                ClimateThermostatState(
                    livingTargetTemperature =
                        numberMetric(
                            thermostat,
                            "livingTargetTemperature"
                        )
                ),
            ventilation =
                ClimateVentilationState(
                    speed =
                        numberMetric(
                            ventilation,
                            "speed"
                        )
                ),
            thermal =
                ClimateThermalState(
                    dhwBufferTemperature =
                        numberMetric(
                            thermal,
                            "dhwBufferTemperature"
                        ),
                    bufferLowerTemperature =
                        numberMetric(
                            thermal,
                            "bufferLowerTemperature"
                        ),
                    bufferUpperTemperature =
                        numberMetric(
                            thermal,
                            "bufferUpperTemperature"
                        )
                ),
            fireplace =
                ClimateFireplaceState(
                    mode =
                        textMetric(
                            fireplace,
                            "mode"
                        ),
                    powered =
                        booleanMetric(
                            fireplace,
                            "powered"
                        ),
                    powerLevel =
                        numberMetric(
                            fireplace,
                            "powerLevel"
                        )
                ),
            completeSnapshotJson =
                metricObjectValueAsJson(
                    completeSnapshot
                ),
            updatedAt =
                root.optNullableString(
                    "updatedAt"
                ),
            complete =
                root.optBoolean(
                    "complete",
                    false
                )
        )
    }


    private fun numberMetric(
        parent: JSONObject,
        name: String
    ): ClimateNumberMetric {
        val item =
            parent.optJSONObject(name)
                ?: return ClimateNumberMetric()

        return ClimateNumberMetric(
            value = nullableDouble(
                item,
                "value"
            ),
            unit = item.optNullableString(
                "unit"
            ),
            quality =
                item.optNullableString(
                    "quality"
                ),
            source =
                item.optNullableString(
                    "source"
                ),
            timestamp =
                item.optNullableString(
                    "timestamp"
                ),
            available =
                item.optBoolean(
                    "available",
                    false
                )
        )
    }


    private fun textMetric(
        parent: JSONObject,
        name: String
    ): ClimateTextMetric {
        val item =
            parent.optJSONObject(name)
                ?: return ClimateTextMetric()

        return ClimateTextMetric(
            value =
                item.optNullableString(
                    "value"
                ),
            unit =
                item.optNullableString(
                    "unit"
                ),
            quality =
                item.optNullableString(
                    "quality"
                ),
            source =
                item.optNullableString(
                    "source"
                ),
            timestamp =
                item.optNullableString(
                    "timestamp"
                ),
            available =
                item.optBoolean(
                    "available",
                    false
                )
        )
    }


    private fun booleanMetric(
        parent: JSONObject,
        name: String
    ): ClimateBooleanMetric {
        val item =
            parent.optJSONObject(name)
                ?: return ClimateBooleanMetric()

        return ClimateBooleanMetric(
            value = nullableBoolean(
                item,
                "value"
            ),
            unit =
                item.optNullableString(
                    "unit"
                ),
            quality =
                item.optNullableString(
                    "quality"
                ),
            source =
                item.optNullableString(
                    "source"
                ),
            timestamp =
                item.optNullableString(
                    "timestamp"
                ),
            available =
                item.optBoolean(
                    "available",
                    false
                )
        )
    }


    private fun nullableDouble(
        objectValue: JSONObject,
        name: String
    ): Double? {
        if (
            !objectValue.has(name) ||
            objectValue.isNull(name)
        ) {
            return null
        }

        return when (
            val value =
                objectValue.opt(name)
        ) {
            is Number ->
                value.toDouble()

            is String ->
                value
                    .trim()
                    .replace(
                        ',',
                        '.'
                    )
                    .toDoubleOrNull()

            else ->
                null
        }
    }


    private fun nullableBoolean(
        objectValue: JSONObject,
        name: String
    ): Boolean? {
        if (
            !objectValue.has(name) ||
            objectValue.isNull(name)
        ) {
            return null
        }

        return when (
            val value =
                objectValue.opt(name)
        ) {
            is Boolean ->
                value

            is Number ->
                value.toInt() != 0

            is String ->
                when (
                    value
                        .trim()
                        .uppercase()
                ) {
                    "TRUE",
                    "ON",
                    "1" ->
                        true

                    "FALSE",
                    "OFF",
                    "0" ->
                        false

                    else ->
                        null
                }

            else ->
                null
        }
    }


    private fun metricObjectValueAsJson(
        metric: JSONObject?
    ): String? {
        if (metric == null) {
            return null
        }

        if (
            !metric.has("value") ||
            metric.isNull("value")
        ) {
            return null
        }

        return when (
            val value =
                metric.opt("value")
        ) {
            is JSONObject ->
                value.toString()

            else ->
                value?.toString()
        }
    }


    private fun JSONObject.optNullableString(
        name: String
    ): String? {
        if (
            !has(name) ||
            isNull(name)
        ) {
            return null
        }

        return optString(
            name,
            ""
        ).takeIf {
            it.isNotBlank() &&
                !it.equals(
                    "null",
                    ignoreCase = true
                )
        }
    }
}
