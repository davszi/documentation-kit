#!/usr/bin/env bash
set -euo pipefail
TASK_KIT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$TASK_KIT_ROOT"
: "${DOCS_PYTHON:=python3.12}"
export DOCSITE_PROJECT_ROOT="$TASK_KIT_ROOT/examples/starter"
export PYTHONPATH="$TASK_KIT_ROOT/tooling"
"$DOCS_PYTHON" docsite.py build --project examples/starter
"$DOCS_PYTHON" docsite.py lint --project examples/starter --strict
"$DOCS_PYTHON" -m unittest discover -s tests -p 'test_*.py'
node tests/test_math_runtime.cjs
node tests/test_site_filelinks.cjs
