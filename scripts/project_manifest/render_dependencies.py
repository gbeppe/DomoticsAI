from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from .dependencies import DependencyRecord


def utc_now_iso() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def _escape(
    value: str,
) -> str:
    return (
        value
        .replace("|", r"\|")
        .replace("\n", " ")
    )


def render_dependency_inventory(
    records: list[DependencyRecord],
) -> str:
    status_counts = Counter(
        record.verification_status
        for record in records
    )

    unresolved = [
        record
        for record in records
        if record.verification_status
        == "NON_VERIFICATA"
    ]

    lines = [
        "# DomoticsAI — Dependency Inventory",
        "",
        f"Generato automaticamente: "
        f"`{utc_now_iso()}`",
        "",
        "> Le informazioni verificate derivano "
        "dal catalogo versionato del progetto. "
        "Le dipendenze sconosciute restano "
        "esplicitamente non verificate.",
        "",
        "## Politica del progetto",
        "",
        "- Nessuna licenza commerciale obbligatoria.",
        "- Nessun abbonamento obbligatorio.",
        "- Nessun cloud obbligatorio.",
        "- Server previsto su Raspberry Pi.",
        "- Client previsto su Android.",
        "- Le nuove dipendenze devono essere "
        "registrate nel catalogo prima della release.",
        "",
        "## Riepilogo",
        "",
        f"- Dipendenze dichiarate: `{len(records)}`",
        f"- Verificate esattamente: "
        f"`{status_counts['VERIFICATA']}`",
        f"- Verificate per famiglia: "
        f"`{status_counts['VERIFICATA_FAMIGLIA']}`",
        f"- Non verificate: "
        f"`{len(unresolved)}`",
        "",
        "## Inventario",
        "",
        "| Ecosistema | Dipendenza | Versione | "
        "Ambito | Licenza | Costi | Cloud | "
        "Piattaforma | Stato |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    _escape(record.ecosystem),
                    f"`{_escape(record.name)}`",
                    f"`{_escape(record.version)}`",
                    _escape(record.scope),
                    _escape(record.license),
                    _escape(record.cost_model),
                    _escape(
                        record.cloud_required
                    ),
                    _escape(
                        record.raspberry_pi
                    ),
                    _escape(
                        record.verification_status
                    ),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Dettagli di verifica",
            "",
            "| Dipendenza | Fonte ufficiale | "
            "Verificata il | Note |",
            "|---|---|---|---|",
        ]
    )

    for record in records:
        source = (
            record.official_source
            or "—"
        )

        verified_at = (
            record.verified_at
            or "—"
        )

        notes = (
            record.notes
            or "—"
        )

        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{_escape(record.name)}`",
                    (
                        f"[fonte ufficiale]"
                        f"({_escape(source)})"
                        if source != "—"
                        else "—"
                    ),
                    _escape(verified_at),
                    _escape(notes),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Dipendenze da verificare",
            "",
        ]
    )

    if unresolved:
        for record in unresolved:
            lines.append(
                f"- `{record.ecosystem}` / "
                f"`{record.name}` "
                f"({record.version})"
            )
    else:
        lines.append(
            "- Nessuna dipendenza diretta "
            "rimasta senza classificazione."
        )

    lines.extend(
        [
            "",
            "## Limiti della verifica",
            "",
            "- Il catalogo riguarda le dipendenze "
            "dirette dichiarate.",
            "- Le dipendenze transitive saranno "
            "analizzate nello Sprint 10.3C.",
            "- La compatibilità Raspberry Pi deve "
            "essere confermata con build e runtime "
            "sull’hardware destinazione.",
            "- Questa documentazione non sostituisce "
            "una valutazione legale professionale.",
            "",
        ]
    )

    return "\n".join(lines)
