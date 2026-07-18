#!/usr/bin/env bash
set -euo pipefail

cd "${1:-.}"

source core-engine/.venv/bin/activate

echo "1/4 - Compilazione moduli Registry"
python -m py_compile \
  core-engine/src/domoticsai_core/registry/query.py \
  core-engine/src/domoticsai_core/registry/service.py \
  core-engine/src/domoticsai_core/registry/__init__.py

echo
echo "2/4 - Test Registry Service"
PYTHONPATH="core-engine/src:${PYTHONPATH:-}" \
python -m pytest -q \
  core-engine/tests/registry/test_registry_service.py

echo
echo "3/4 - Controllo formattazione Git"
git diff --check

echo
echo "4/4 - Stato Git"
git status --short

echo
echo "Sprint 12.9 Registry Service: test completati."
