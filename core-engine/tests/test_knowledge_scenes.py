from domoticsai_core.knowledge.reasoners.scene_reasoner import (
    SceneReasoner,
)
from domoticsai_core.knowledge.scene_state import (
    SceneStateSnapshot,
    SceneStateTracker,
)


def facts_by_name(facts):
    return {
        fact.name: fact
        for fact in facts
    }


def test_requested_scene_is_pending():
    tracker = SceneStateTracker()

    tracker.handle_command_event({
        "commandId": "cmd-1",
        "domain": "scenes",
        "target": "TV_MODE",
        "state": "waiting_confirmation",
        "updatedAt": "2026-07-15T14:00:00+00:00",
    })

    facts = facts_by_name(
        SceneReasoner().reason(
            tracker.snapshot()
        )
    )

    assert (
        facts["scenes.requested"].value
        == "TV_MODE"
    )

    assert (
        facts["scenes.requested_mode"].value
        == "tv"
    )

    assert (
        facts[
            "scenes.execution_pending"
        ].value
        is True
    )

    assert (
        facts["scenes.confirmed"].value
        is None
    )


def test_confirmed_scene():
    tracker = SceneStateTracker()

    tracker.handle_command_event({
        "commandId": "cmd-2",
        "domain": "scenes",
        "target": "ALL_OFF",
        "state": "confirmed",
        "updatedAt": "2026-07-15T14:01:00+00:00",
    })

    facts = facts_by_name(
        SceneReasoner().reason(
            tracker.snapshot()
        )
    )

    assert (
        facts["scenes.confirmed"].value
        == "ALL_OFF"
    )

    assert (
        facts["scenes.confirmed_mode"].value
        == "all_off"
    )

    assert (
        facts[
            "scenes.execution_pending"
        ].value
        is False
    )

    assert (
        facts[
            "scenes.observed_match"
        ].value
        == "unknown"
    )


def test_non_scene_command_is_ignored():
    tracker = SceneStateTracker()

    tracker.handle_command_event({
        "commandId": "cmd-3",
        "domain": "lights",
        "target": "internal/sala",
        "state": "confirmed",
    })

    snapshot = tracker.snapshot()

    assert snapshot.requested_scene is None
    assert snapshot.confirmed_scene is None
