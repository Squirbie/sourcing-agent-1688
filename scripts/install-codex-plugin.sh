#!/usr/bin/env bash
set -euo pipefail

SOURCE="${1:-.}"
UVX_SOURCE="${SOURCE}"
# uvx expects Git URLs as git+https://... while codex marketplace add accepts the original URL.
if [[ "${SOURCE}" =~ ^https?:// ]] && [[ "${SOURCE}" != git+* ]]; then
  UVX_SOURCE="git+${SOURCE}"
fi

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found. Install or open Codex, then add this marketplace manually."
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found. Install uv before running sourcing1688."
  exit 1
fi

echo "Adding Codex plugin marketplace: ${SOURCE}"
if codex plugin marketplace add "${SOURCE}"; then
  echo "Marketplace added. Open /plugins in Codex and install sourcing-agent-1688."
else
  echo "Automatic marketplace add failed. Run manually:"
  echo "  codex plugin marketplace add ${SOURCE}"
fi

if command -v sourcing1688 >/dev/null 2>&1; then
  sourcing1688 init-home --json
else
  uvx --from "${UVX_SOURCE}" sourcing1688 init-home --json || true
fi

echo "After install, run:"
echo "  sourcing1688 provider-check --provider auto --json"
