#!/usr/bin/env bash

set -euo pipefail

ROOT="$(
  cd "$(dirname "${BASH_SOURCE[0]}")/.."
  pwd
)"

cd "$ROOT"

python3 scripts/generate-project-manifest.py

for document in \
  docs/PROJECT_MANIFEST.md \
  docs/PROJECT_INDEX.md \
  docs/DEPENDENCY_INVENTORY.md
do
  echo
  echo "=== ${document} ==="

  git --no-pager diff -- "$document"
done

echo
echo "=== STATO DOCUMENTI ==="

git status --short -- \
  docs/PROJECT_MANIFEST.md \
  docs/PROJECT_INDEX.md \
  docs/DEPENDENCY_INVENTORY.md
