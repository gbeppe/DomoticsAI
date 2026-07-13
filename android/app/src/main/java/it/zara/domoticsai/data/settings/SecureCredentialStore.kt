package it.zara.domoticsai.data.settings

import android.content.Context
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import android.util.Base64
import it.zara.domoticsai.domain.model.AppCredentials
import it.zara.domoticsai.domain.model.BrokerCredentials
import org.json.JSONObject
import java.nio.charset.StandardCharsets
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

class SecureCredentialStore(context: Context) {
    private val preferences = context.getSharedPreferences(
        "domoticsai_secure_credentials",
        Context.MODE_PRIVATE
    )

    private val keyAlias = "domoticsai_mqtt_credentials_key"
    private val payloadKey = "encrypted_credentials"

    fun load(): AppCredentials {
        val encoded = preferences.getString(payloadKey, null) ?: return AppCredentials()

        return runCatching {
            val envelope = JSONObject(encoded)
            val iv = Base64.decode(envelope.getString("iv"), Base64.NO_WRAP)
            val ciphertext = Base64.decode(envelope.getString("ciphertext"), Base64.NO_WRAP)

            val cipher = Cipher.getInstance(TRANSFORMATION)
            cipher.init(
                Cipher.DECRYPT_MODE,
                getOrCreateKey(),
                GCMParameterSpec(128, iv)
            )

            val plain = cipher.doFinal(ciphertext)
                .toString(StandardCharsets.UTF_8)

            val json = JSONObject(plain)

            AppCredentials(
                local = BrokerCredentials(
                    username = json.optString("localUsername"),
                    password = json.optString("localPassword")
                ),
                remote = BrokerCredentials(
                    username = json.optString("remoteUsername"),
                    password = json.optString("remotePassword")
                )
            )
        }.getOrElse {
            AppCredentials()
        }
    }

    fun save(credentials: AppCredentials) {
        val plain = JSONObject()
            .put("localUsername", credentials.local.username)
            .put("localPassword", credentials.local.password)
            .put("remoteUsername", credentials.remote.username)
            .put("remotePassword", credentials.remote.password)
            .toString()
            .toByteArray(StandardCharsets.UTF_8)

        val cipher = Cipher.getInstance(TRANSFORMATION)
        cipher.init(Cipher.ENCRYPT_MODE, getOrCreateKey())

        val ciphertext = cipher.doFinal(plain)
        val envelope = JSONObject()
            .put("iv", Base64.encodeToString(cipher.iv, Base64.NO_WRAP))
            .put("ciphertext", Base64.encodeToString(ciphertext, Base64.NO_WRAP))
            .toString()

        preferences.edit()
            .putString(payloadKey, envelope)
            .apply()
    }

    private fun getOrCreateKey(): SecretKey {
        val keyStore = KeyStore.getInstance(ANDROID_KEYSTORE).apply {
            load(null)
        }

        (keyStore.getKey(keyAlias, null) as? SecretKey)?.let {
            return it
        }

        val generator = KeyGenerator.getInstance(
            KeyProperties.KEY_ALGORITHM_AES,
            ANDROID_KEYSTORE
        )

        generator.init(
            KeyGenParameterSpec.Builder(
                keyAlias,
                KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
            )
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setRandomizedEncryptionRequired(true)
                .build()
        )

        return generator.generateKey()
    }

    companion object {
        private const val ANDROID_KEYSTORE = "AndroidKeyStore"
        private const val TRANSFORMATION = "AES/GCM/NoPadding"
    }
}
