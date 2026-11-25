#!/usr/bin/env bash
# Deployment build script for the Django API.
# Run from the repository root: ./build.sh

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
PYTHON_BIN="${PYTHON_BIN:-python}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Error: Python 3 is required to build the backend." >&2
  exit 1
fi

cd "$BACKEND_DIR"

echo "Installing backend dependencies..."
"$PYTHON_BIN" -m pip install --upgrade pip
"$PYTHON_BIN" -m pip install -r requirements.txt

echo "Checking Django configuration..."
"$PYTHON_BIN" manage.py check

echo "Collecting static files..."
"$PYTHON_BIN" manage.py collectstatic --noinput

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "Applying database migrations..."
  "$PYTHON_BIN" manage.py migrate --noinput
else
  echo "Skipping migrations because RUN_MIGRATIONS is not true."
fi

echo "Backend build completed successfully."
