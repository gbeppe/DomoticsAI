from __future__ import annotations

from ..models import TwinValue
from .context_engine import (
    HouseContextEngine,
)
from .reasoners.energy_reasoner import (
    EnergyReasoner,
)
from .reasoners.lights_reasoner import (
    LightsReasoner,
)
from .reasoners.pool_reasoner import (
    PoolReasoner,
)
from .reasoners.scene_reasoner import (
    SceneReasoner,
)
from .scene_state import (
    SceneStateSnapshot,
)


class HouseKnowledgeEngine:
    def __init__(self) -> None:
        self._domain_reasoners = [
            EnergyReasoner(),
            LightsReasoner(),
            PoolReasoner(),
        ]

        self._scene_reasoner = (
            SceneReasoner()
        )

        self._context_engine = (
            HouseContextEngine()
        )

    def evaluate(
        self,
        domains: dict[
            str,
            dict[str, TwinValue],
        ],
        scene_state: (
            SceneStateSnapshot | None
        ) = None,
    ) -> dict[str, dict]:
        facts: dict[str, dict] = {}

        for reasoner in self._domain_reasoners:
            for fact in reasoner.reason(
                domains
            ):
                facts[fact.name] = (
                    fact.model_dump()
                )

        if scene_state is not None:
            for fact in (
                self._scene_reasoner.reason(
                    scene_state
                )
            ):
                facts[fact.name] = (
                    fact.model_dump()
                )

        contexts = (
            self._context_engine.evaluate(
                facts
            )
        )

        for name, context in contexts.items():
            facts[
                f"context.{name}"
            ] = {
                "name": (
                    f"context.{name}"
                ),
                "category": "context",
                "value": context,
                "confidence": (
                    context["confidence"]
                ),
                "reason": (
                    context["reason"]
                ),
                "observed_at": (
                    context["observed_at"]
                ),
                "source": (
                    "house-context-engine"
                ),
            }

        return facts
