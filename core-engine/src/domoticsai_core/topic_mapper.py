from dataclasses import dataclass

BASE_PREFIX = "domoticsai/v1/state/"


@dataclass(frozen=True)
class TopicAddress:
    domain: str
    entity: str


_registry = None


def configure_registry(registry):
    """Registers the global Registry instance used for topic resolution."""
    global _registry
    _registry = registry


def _legacy_map_state_topic(topic: str):
    if not topic.startswith(BASE_PREFIX):
        return None

    suffix = topic[len(BASE_PREFIX):].strip("/")
    parts = [part for part in suffix.split("/") if part]

    if len(parts) < 2:
        return None

    return TopicAddress(
        parts[0],
        "/".join(parts[1:]),
    )


def map_state_topic(topic: str):
    if _registry is not None:
        entity = _registry.by_state_topic(topic)

        if entity is not None:
            return TopicAddress(
                domain=entity.domain,
                entity=entity.entity_id,
            )

    return _legacy_map_state_topic(topic)
