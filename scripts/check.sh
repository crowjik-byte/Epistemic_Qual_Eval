#!/usr/bin/env sh
# Run every check CI runs. Agents and humans run this before each commit and push.
# Usage: scripts/check.sh          (check only)
#        scripts/check.sh --fix    (apply safe lint fixes and formatting first)
set -eu
cd "$(dirname "$0")/.."

if ! command -v ruff >/dev/null 2>&1; then
    echo "ruff is not installed. Run: python -m pip install -e '.[dev]'" >&2
    exit 1
fi

if [ "${1:-}" = "--fix" ]; then
    ruff check --fix .
    ruff format .
fi

ruff check .
ruff format --check .
python -m unittest discover -s tests -v
