from datetime import datetime, timezone
import logging
import threading

import paho.mqtt.client as mqtt

from .config import Settings


logger = logging.getLogger(__name__)


ALLOWED_COMMAND_PREFIXES = (
    "domoticsai/v1/cmd/lights/",
    "domoticsai/v1/cmd/scenes/",
)


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


class MqttService:
    def __init__(
        self,
        settings: Settings,
        on_message,
    ):
        self._settings = settings
        self._on_message_handler = on_message
        self._connected = threading.Event()

        self._metrics_lock = threading.RLock()
        self._messages_received = 0
        self._message_errors = 0
        self._last_message_at = None
        self._last_error_at = None
        self._last_error = None

        self._client = mqtt.Client(
            callback_api_version=(
                mqtt.CallbackAPIVersion.VERSION2
            ),
            client_id="domoticsai-core-engine",
            protocol=mqtt.MQTTv311,
        )

        if settings.mqtt_username:
            self._client.username_pw_set(
                settings.mqtt_username,
                settings.mqtt_password,
            )

        self._client.on_connect = (
            self._on_connect
        )
        self._client.on_disconnect = (
            self._on_disconnect
        )
        self._client.on_message = (
            self._on_message
        )

    @property
    def connected(self):
        return self._connected.is_set()

    @property
    def diagnostics(self) -> dict:
        with self._metrics_lock:
            return {
                "connected": self.connected,
                "messagesReceived": (
                    self._messages_received
                ),
                "messageErrors": (
                    self._message_errors
                ),
                "lastMessageAt": (
                    self._last_message_at
                ),
                "lastErrorAt": (
                    self._last_error_at
                ),
                "lastError": (
                    self._last_error
                ),
            }

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

    def publish_command(
        self,
        topic,
        payload,
        *,
        qos=1,
        retain=False,
    ):
        if not topic.startswith(
            ALLOWED_COMMAND_PREFIXES
        ):
            raise ValueError(
                "Command topic is not allowed: "
                f"{topic}"
            )

        if retain:
            raise ValueError(
                "Command messages must never "
                "be retained"
            )

        if not self.connected:
            raise RuntimeError(
                "MQTT broker is not connected"
            )

        result = self._client.publish(
            topic,
            payload,
            qos=qos,
            retain=False,
        )

        if (
            result.rc
            != mqtt.MQTT_ERR_SUCCESS
        ):
            raise RuntimeError(
                "MQTT publish failed with "
                f"rc={result.rc}"
            )

    def _on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties,
    ):
        if reason_code.is_failure:
            self._connected.clear()

            logger.error(
                "MQTT connection failed: %s",
                reason_code,
            )
            return

        self._connected.set()

        client.subscribe(
            self._settings.mqtt_topic,
            qos=1,
        )

        logger.info(
            "MQTT connected and subscribed to %s",
            self._settings.mqtt_topic,
        )

    def _on_disconnect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties,
    ):
        self._connected.clear()

        logger.warning(
            "MQTT disconnected: %s",
            reason_code,
        )

    def _on_message(
        self,
        client,
        userdata,
        message,
    ):
        payload = message.payload.decode(
            "utf-8",
            errors="replace",
        )

        with self._metrics_lock:
            self._messages_received += 1
            self._last_message_at = (
                utc_now_iso()
            )

        try:
            self._on_message_handler(
                message.topic,
                payload,
            )

        except Exception as error:
            with self._metrics_lock:
                self._message_errors += 1
                self._last_error_at = (
                    utc_now_iso()
                )
                self._last_error = (
                    f"{type(error).__name__}: "
                    f"{error}"
                )

            logger.exception(
                "MQTT message handling failed: "
                "topic=%s",
                message.topic,
            )
