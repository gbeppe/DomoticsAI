from __future__ import annotations

from ..facts import KnowledgeFact
from ..scene_state import SceneStateSnapshot
from ..scenes_registry import (
    is_known_scene,
    scene_metadata,
)


class SceneReasoner:
    category = "scenes"

    def reason(
        self,
        scene_state: SceneStateSnapshot,
    ) -> list[KnowledgeFact]:
        requested = scene_state.requested_scene
        confirmed = scene_state.confirmed_scene

        requested_metadata = (
            scene_metadata(requested)
            if requested
            else None
        )

        confirmed_metadata = (
            scene_metadata(confirmed)
            if confirmed
            else None
        )

        requested_known = (
            is_known_scene(requested)
            if requested
            else False
        )

        confirmed_known = (
            is_known_scene(confirmed)
            if confirmed
            else False
        )

        return [
            KnowledgeFact(
                name="scenes.requested",
                category=self.category,
                value=requested,
                reason=[
                    "latest scene command received"
                ],
            ),
            KnowledgeFact(
                name="scenes.requested_known",
                category=self.category,
                value=requested_known,
                reason=[
                    (
                        f"scene registry contains "
                        f"{requested!r}"
                    )
                ],
            ),
            KnowledgeFact(
                name="scenes.requested_mode",
                category=self.category,
                value=(
                    requested_metadata[
                        "semantic_mode"
                    ]
                    if requested_metadata
                    else None
                ),
                reason=[
                    "mapped through scene registry"
                ],
            ),
            KnowledgeFact(
                name="scenes.command_state",
                category=self.category,
                value=scene_state.command_state,
                reason=[
                    "latest Command Manager state"
                ],
            ),
            KnowledgeFact(
                name="scenes.confirmed",
                category=self.category,
                value=confirmed,
                reason=[
                    (
                        "latest scene reaching "
                        "confirmed or simulated state"
                    )
                ],
            ),
            KnowledgeFact(
                name="scenes.confirmed_known",
                category=self.category,
                value=confirmed_known,
                reason=[
                    (
                        f"scene registry contains "
                        f"{confirmed!r}"
                    )
                ],
            ),
            KnowledgeFact(
                name="scenes.confirmed_mode",
                category=self.category,
                value=(
                    confirmed_metadata[
                        "semantic_mode"
                    ]
                    if confirmed_metadata
                    else None
                ),
                reason=[
                    "mapped through scene registry"
                ],
            ),
            KnowledgeFact(
                name="scenes.execution_pending",
                category=self.category,
                value=(
                    scene_state.command_state
                    in {
                        "created",
                        "validated",
                        "queued",
                        "sent",
                        "waiting_confirmation",
                    }
                ),
                reason=[
                    (
                        "Command Manager state="
                        f"{scene_state.command_state}"
                    )
                ],
            ),
            KnowledgeFact(
                name="scenes.last_error",
                category=self.category,
                value=scene_state.last_error,
                reason=[
                    "latest scene command failure"
                ],
            ),
            KnowledgeFact(
                name="scenes.observed_match",
                category=self.category,
                value="unknown",
                confidence=0.0,
                reason=[
                    (
                        "physical light composition "
                        "of each scene is not yet encoded"
                    )
                ],
            ),
        ]
