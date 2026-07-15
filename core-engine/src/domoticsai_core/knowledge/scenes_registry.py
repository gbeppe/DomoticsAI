from __future__ import annotations


SCENES = {
    "ALL_ON": {
        "label": "Tutte le luci accese",
        "semantic_mode": "all_on",
        "description": (
            "Attiva il gruppo di luci associato "
            "allo scenario generale di accensione."
        ),
    },
    "ALL_OFF": {
        "label": "Tutte le luci spente",
        "semantic_mode": "all_off",
        "description": (
            "Disattiva il gruppo di luci associato "
            "allo scenario generale di spegnimento."
        ),
    },
    "TV_MODE": {
        "label": "Modalità TV",
        "semantic_mode": "tv",
        "description": (
            "Configura l’illuminazione associata "
            "alla visione della televisione."
        ),
    },
    "SLEEP_MODE": {
        "label": "Modalità notte",
        "semantic_mode": "sleep",
        "description": (
            "Configura l’illuminazione associata "
            "alla preparazione per la notte."
        ),
    },
}


def is_known_scene(scene_id: str) -> bool:
    return scene_id in SCENES


def scene_metadata(
    scene_id: str,
) -> dict | None:
    metadata = SCENES.get(scene_id)

    if metadata is None:
        return None

    return {
        "id": scene_id,
        **metadata,
    }
