from __future__ import annotations

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
    lines = [
        "# DomoticsAI — Dependency Inventory",
        "",
        f"Generato automaticamente: "
        f"`{utc_now_iso()}`",
        "",
        "> Questo documento censisce le dipendenze "
        "dichiarate nel repository. I campi relativi "
        "a licenza, costi, cloud e Raspberry Pi "
        "devono essere verificati prima di essere "
        "considerati definitivi.",
        "",
        "## Politica del progetto",
        "",
        "- Nessuna licenza commerciale obbligatoria.",
        "- Nessun abbonamento obbligatorio.",
        "- Nessun cloud obbligatorio.",
        "- Esecuzione server prevista su Raspberry Pi.",
        "- Client previsto su smartphone Android.",
        "- Preferenza per MIT, BSD, Apache-2.0, "
        "MPL-2.0 e altre licenze open source "
        "compatibili con il progetto.",
        "",
        "## Riepilogo",
        "",
        f"- Dipendenze dichiarate: `{len(records)}`",
        f"- Python: "
        f"`{sum(r.ecosystem == 'Python' for r in records)}`",
        f"- Android/Gradle: "
        f"`{sum(r.ecosystem == 'Android/Gradle' for r in records)}`",
        f"- Node.js/npm: "
        f"`{sum(r.ecosystem == 'Node.js/npm' for r in records)}`",
        "",
        "## Inventario",
        "",
        "| Ecosistema | Dipendenza | Versione/vincolo | "
        "Ambito | File sorgente | Licenza | Costi | "
        "Cloud obbligatorio | Raspberry Pi |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    _escape(
                        record.ecosystem
                    ),
                    f"`{_escape(record.name)}`",
                    f"`{_escape(record.version)}`",
                    _escape(record.scope),
                    f"`{_escape(record.source_file)}`",
                    _escape(record.license),
                    _escape(record.cost_model),
                    _escape(
                        record.cloud_required
                    ),
                    _escape(
                        record.raspberry_pi
                    ),
                ]
            )
            + " |"
        )

    if not records:
        lines.append(
            "| — | Nessuna dipendenza rilevata "
            "| — | — | — | — | — | — | — |"
        )

    lines.extend(
        [
            "",
            "## Metodo di verifica previsto",
            "",
            "Nella fase successiva ogni dipendenza "
            "sarà verificata usando, in ordine:",
            "",
            "1. metadati ufficiali del pacchetto;",
            "2. repository ufficiale del progetto;",
            "3. file `LICENSE` o documentazione ufficiale;",
            "4. compatibilità architetturale ARM64/ARMv7;",
            "5. eventuali dipendenze da servizi cloud;",
            "6. eventuali componenti premium o "
            "funzioni con abbonamento.",
            "",
            "Un pacchetto non verrà classificato come "
            "compatibile finché la verifica non sarà "
            "supportata da una fonte attendibile.",
            "",
        ]
    )

    return "\n".join(lines)
