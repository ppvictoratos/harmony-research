#!/usr/bin/env bash
# Start the API (http://localhost:8000) and web UI (http://localhost:3000) together.
# Ctrl-C stops both.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -x backend/venv/bin/uvicorn ]; then
  echo "Setting up backend venv..."
  python3.12 -m venv backend/venv
  backend/venv/bin/pip install -q -e backend
fi
if [ ! -d web/node_modules ]; then
  echo "Installing web dependencies..."
  (cd web && npm install --no-audit --no-fund)
fi

trap 'kill 0' EXIT
(cd backend && ./venv/bin/uvicorn app.main:app --port 8000 --reload) &
(cd web && npm run dev) &
wait
