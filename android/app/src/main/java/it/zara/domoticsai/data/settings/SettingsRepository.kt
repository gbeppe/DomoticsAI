package it.zara.domoticsai.data.settings

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import it.zara.domoticsai.domain.model.BrokerEndpoint
import it.zara.domoticsai.domain.model.ConnectionMode
import it.zara.domoticsai.domain.model.ConnectionSettings
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore by preferencesDataStore(name = "domoticsai_settings")

class SettingsRepository(private val context: Context) {
    private object Keys {
        val mode = stringPreferencesKey("connection_mode")
        val localHost = stringPreferencesKey("local_host")
        val localPort = intPreferencesKey("local_port")
        val remoteHost = stringPreferencesKey("remote_host")
        val remotePort = intPreferencesKey("remote_port")
    }

    val settings: Flow<ConnectionSettings> = context.dataStore.data.map { prefs ->
        ConnectionSettings(
            mode = prefs[Keys.mode]
                ?.let { runCatching { ConnectionMode.valueOf(it) }.getOrNull() }
                ?: ConnectionMode.AUTO,
            local = BrokerEndpoint(
                host = prefs[Keys.localHost] ?: "192.168.1.40",
                port = prefs[Keys.localPort] ?: 1883
            ),
            remote = BrokerEndpoint(
                host = prefs[Keys.remoteHost] ?: "",
                port = prefs[Keys.remotePort] ?: 1883
            )
        )
    }

    suspend fun save(settings: ConnectionSettings) {
        context.dataStore.edit { prefs ->
            prefs[Keys.mode] = settings.mode.name
            prefs[Keys.localHost] = settings.local.host.trim()
            prefs[Keys.localPort] = settings.local.port
            prefs[Keys.remoteHost] = settings.remote.host.trim()
            prefs[Keys.remotePort] = settings.remote.port
        }
    }
}
