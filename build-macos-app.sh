#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MACOS_DIR="${SCRIPT_DIR}/macos"

if [ ! -d "${MACOS_DIR}" ]; then
  echo "Error: macos/ directory not found in ${SCRIPT_DIR}"
  exit 1
fi

echo "==> Building native macOS Swift application (Hermes Agent.app)..."
cd "${MACOS_DIR}"
bash build.sh

echo "==> Done! App installed at /Applications/Hermes Agent.app"
