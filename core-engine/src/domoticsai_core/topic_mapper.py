from dataclasses import dataclass

BASE_PREFIX = "domoticsai/v1/state/"

@dataclass(frozen=True)
class TopicAddress:
    domain: str
    entity: str

def map_state_topic(topic: str):
    if not topic.startswith(BASE_PREFIX):
        return None
    suffix = topic[len(BASE_PREFIX):].strip("/")
    parts = [part for part in suffix.split("/") if part]
    if len(parts) < 2:
        return None
    return TopicAddress(parts[0], "/".join(parts[1:]))
