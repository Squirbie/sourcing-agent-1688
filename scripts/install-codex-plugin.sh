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
  echo "Marketplace added."
else
  echo "Automatic marketplace add failed. Run manually:"
  echo "  codex plugin marketplace add ${SOURCE}"
fi

CODEX_HOME_DIR="${CODEX_HOME:-${HOME}/.codex}"
CODEX_CONFIG="${CODEX_HOME_DIR}/config.toml"
mkdir -p "${CODEX_HOME_DIR}"
touch "${CODEX_CONFIG}"
if grep -Fq '[plugins."sourcing-agent-1688@sourcing-agent-1688-marketplace"]' "${CODEX_CONFIG}"; then
  echo "Plugin already enabled in Codex config."
else
  cat >>"${CODEX_CONFIG}" <<'EOF'

[plugins."sourcing-agent-1688@sourcing-agent-1688-marketplace"]
enabled = true
EOF
  echo "Plugin enabled in Codex config: sourcing-agent-1688@sourcing-agent-1688-marketplace"
fi

if command -v sourcing1688 >/dev/null 2>&1; then
  sourcing1688 init-home --json
else
  uvx --from "${UVX_SOURCE}" sourcing1688 init-home --json || true
fi

echo "After install, run:"
echo "  sourcing1688 provider-check --provider auto --json"
echo "Restart Codex, then use @1688 Sourcing Agent in a new chat."
