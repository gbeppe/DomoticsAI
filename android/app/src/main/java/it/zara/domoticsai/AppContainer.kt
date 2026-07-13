package it.zara.domoticsai

import android.content.Context
import it.zara.domoticsai.data.mqtt.DomoticsRepository
import it.zara.domoticsai.data.mqtt.MqttClientService
import it.zara.domoticsai.data.settings.SecureCredentialStore
import it.zara.domoticsai.data.settings.SettingsRepository

class AppContainer(context: Context) {
    val settingsRepository = SettingsRepository(context)
    val credentialStore = SecureCredentialStore(context)
    val mqttClientService = MqttClientService()

    val domoticsRepository = DomoticsRepository(
        mqttClientService = mqttClientService,
        settingsRepository = settingsRepository
    )
}
