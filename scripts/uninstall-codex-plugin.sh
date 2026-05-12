#!/usr/bin/env bash
set -euo pipefail

YES="false"
CLEAN_UV_CACHE="false"
for arg in "$@"; do
  case "$arg" in
    --yes) YES="true" ;;
    --clean-uv-cache) CLEAN_UV_CACHE="true" ;;
  esac
done

if [[ "${YES}" != "true" ]]; then
  echo "This removes the Codex marketplace entry and sourcing1688 runtime state."
  echo "Re-run with --yes after reviewing. Optional: --clean-uv-cache"
  exit 1
fi

if command -v codex >/dev/null 2>&1; then
  codex plugin marketplace remove sourcing-agent-1688-marketplace || true
else
  echo "codex CLI not found. Remove the plugin from /plugins manually."
fi

if command -v sourcing1688 >/dev/null 2>&1; then
  sourcing1688 uninstall --yes --json
else
  echo "sourcing1688 CLI not found. If needed, delete SOURCING1688_HOME manually after checking the path."
fi

if [[ "${CLEAN_UV_CACHE}" == "true" ]]; then
  echo "uv cache cleaning is intentionally not automatic. Run 'uv cache clean' yourself if desired."
fi
