#!/usr/bin/env bash

set -euo pipefail

ROOT="$(
  cd "$(dirname "${BASH_SOURCE[0]}")/.."
  pwd
)"

cd "$ROOT"

python3 scripts/generate-project-manifest.py

echo
git diff -- \
  docs/PROJECT_MANIFEST.md
