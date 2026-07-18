# DomoticsAI Governance Toolkit v0.2.0

Repository Census Engine with deterministic scanning, SHA-256 inventory, category/domain classification, rule findings, Markdown/JSON reporting and optional `--fail-on` quality gate.

```bash
./scripts/run-governance.sh doctor
./scripts/run-governance.sh census
./scripts/run-governance.sh census --fail-on high
python3 -m pytest tests/governance
```
