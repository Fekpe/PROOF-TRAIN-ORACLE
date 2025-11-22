#!/usr/bin/env bash
set -euo pipefail

# start-frontend.sh
# Usage: ./start-frontend.sh
# This script checks for npm, runs npm install, then starts the Vite dev server.

if ! command -v npm >/dev/null 2>&1; then
  cat <<'MSG'
Error: npm not found in PATH.

On Windows you can install Node.js (which includes npm) with one of these methods:
  - PowerShell (recommended):
      winget install --id OpenJS.NodeJS.LTS -e
  - Chocolatey (if you have it):
      choco install nodejs-lts -y
  - Download the installer from https://nodejs.org/en/ (LTS)

After installing, restart your shell and re-run this script.
MSG
  exit 1
fi

# Resolve script directory and frontend path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="${SCRIPT_DIR}/.."

echo "Starting frontend from: $FRONTEND_DIR"
cd "$FRONTEND_DIR"

echo "Installing npm dependencies..."
npm install

echo "Starting Vite dev server (npm run dev)..."
npm run dev
