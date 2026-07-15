from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import threading


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


@dataclass(frozen=True)
class SceneStateSnapshot:
    requested_scene: str | None
    requested_at: str | None
    command_id: str | None
    command_state: str | None
    confirmed_scene: str | None
    confirmed_at: str | None
    last_error: str | None


class SceneStateTracker:
    """
    Conserva lo stato operativo degli scenari.

    Non deduce lo stato delle luci: registra soltanto
    intenzione e conferma provenienti dal Command Manager.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()

        self._requested_scene = None
        self._requested_at = None
        self._command_id = None
        self._command_state = None
        self._confirmed_scene = None
        self._confirmed_at = None
        self._last_error = None

    def handle_command_event(
        self,
        event: dict,
    ) -> None:
        if event.get("domain") != "scenes":
            return

        scene_id = event.get("target")
        state = event.get("state")
        command_id = event.get("commandId")

        if not scene_id or not state:
            return

        now = event.get("updatedAt") or utc_now_iso()

        with self._lock:
            self._requested_scene = scene_id
            self._requested_at = (
                self._requested_at
                if self._command_id == command_id
                else now
            )
            self._command_id = command_id
            self._command_state = state

            if state in {
                "confirmed",
                "simulated",
            }:
                self._confirmed_scene = scene_id
                self._confirmed_at = now
                self._last_error = None

            elif state in {
                "failed",
                "rejected",
                "timeout",
            }:
                self._last_error = (
                    event.get("message")
                    or state
                )

    def snapshot(self) -> SceneStateSnapshot:
        with self._lock:
            return SceneStateSnapshot(
                requested_scene=(
                    self._requested_scene
                ),
                requested_at=(
                    self._requested_at
                ),
                command_id=self._command_id,
                command_state=(
                    self._command_state
                ),
                confirmed_scene=(
                    self._confirmed_scene
                ),
                confirmed_at=(
                    self._confirmed_at
                ),
                last_error=self._last_error,
            )
