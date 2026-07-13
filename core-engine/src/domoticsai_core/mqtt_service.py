import logging
import threading
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)

class MqttService:
    def __init__(self, settings, on_message):
        self._settings = settings
        self._handler = on_message
        self._connected = threading.Event()
        self._client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id="domoticsai-core-engine",
            protocol=mqtt.MQTTv311,
        )
        if settings.mqtt_username:
            self._client.username_pw_set(
                settings.mqtt_username,
                settings.mqtt_password,
            )
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_message = self._on_message

    @property
    def connected(self):
        return self._connected.is_set()

    def start(self):
        self._client.connect_async(
            self._settings.mqtt_host,
            self._settings.mqtt_port,
            keepalive=30,
        )
        self._client.loop_start()

    def stop(self):
        self._client.disconnect()
        self._client.loop_stop()
        self._connected.clear()

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            logger.error("MQTT rejected: %s", reason_code)
            self._connected.clear()
            return
        self._connected.set()
        client.subscribe(self._settings.mqtt_topic, qos=1)

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        self._connected.clear()

    def _on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8", errors="replace")
        self._handler(message.topic, payload)
