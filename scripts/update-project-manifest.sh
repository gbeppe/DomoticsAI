#!/usr/bin/env bash

set -euo pipefail

ROOT="$(
  cd "$(dirname "${BASH_SOURCE[0]}")/.."
  pwd
)"

cd "$ROOT"

python3 scripts/generate-project-manifest.py

echo
echo "=== PROJECT_MANIFEST.md ==="

git --no-pager diff -- \
  docs/PROJECT_MANIFEST.md

echo
echo "=== PROJECT_INDEX.md ==="

git --no-pager diff -- \
  docs/PROJECT_INDEX.md

echo
echo "=== STATO DOCUMENTI ==="

git status --short -- \
  docs/PROJECT_MANIFEST.md \
  docs/PROJECT_INDEX.md
