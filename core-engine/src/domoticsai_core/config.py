from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    mqtt_host: str
    mqtt_port: int
    mqtt_username: str
    mqtt_password: str
    mqtt_topic: str
    api_host: str
    api_port: int
    db_path: str

    @classmethod
    def from_env(cls):
        return cls(
            mqtt_host=os.getenv("DOMOTICSAI_MQTT_HOST", "127.0.0.1"),
            mqtt_port=int(os.getenv("DOMOTICSAI_MQTT_PORT", "1883")),
            mqtt_username=os.getenv("DOMOTICSAI_MQTT_USERNAME", ""),
            mqtt_password=os.getenv("DOMOTICSAI_MQTT_PASSWORD", ""),
            mqtt_topic=os.getenv("DOMOTICSAI_MQTT_TOPIC", "domoticsai/v1/#"),
            api_host=os.getenv("DOMOTICSAI_API_HOST", "0.0.0.0"),
            api_port=int(os.getenv("DOMOTICSAI_API_PORT", "8090")),
            db_path=os.getenv("DOMOTICSAI_DB_PATH", "data/core-engine.db"),
        )
