from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Optional

from .command_request import CommandRequest


class CommandRoutingError(Exception):
    """Base error raised while resolving a logical command."""


class CommandEntityNotFoundError(CommandRoutingError):
    """Raised when the requested Registry entity does not exist."""


class CommandNotWritableError(CommandRoutingError):
    """Raised when the requested entity cannot receive commands."""


class CommandTopicMissingError(CommandRoutingError):
    """Raised when a writable entity has no command topic."""


@dataclass(frozen=True)
class CommandRoute:
    """
    Transport route resolved from a logical command.

    The CommandRouter builds this object, while the transport
    service is responsible only for publishing it.
    """

    entity_id: str
    command_topic: str
    ack_topic: Optional[str]
    payload: str
    qos: int = 1
    retain: bool = False


class CommandRouter:
    """
    Resolves logical commands through the Digital Twin Registry.

    It does not connect to MQTT and does not publish messages.
    """

    def __init__(self, registry):
        self._registry = registry

    def resolve(
        self,
        request: CommandRequest,
    ) -> CommandRoute:
        entity = self._registry.by_entity_id(
            request.entity_id
        )

        if entity is None:
            raise CommandEntityNotFoundError(
                "Registry entity not found: "
                f"{request.entity_id}"
            )

        if not entity.writable:
            raise CommandNotWritableError(
                "Registry entity is not writable: "
                f"{request.entity_id}"
            )

        if not entity.command_topic:
            raise CommandTopicMissingError(
                "Writable Registry entity has no "
                "command topic: "
                f"{request.entity_id}"
            )

        payload = json.dumps(
            {
                "action": request.action,
                "parameters": request.parameters,
                "source": request.source,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )

        return CommandRoute(
            entity_id=entity.id,
            command_topic=entity.command_topic,
            ack_topic=entity.ack_topic,
            payload=payload,
        )
