param(
  [switch]$Yes,
  [switch]$CleanUvCache
)

$ErrorActionPreference = "Stop"

if (-not $Yes) {
  Write-Output "This removes the Codex marketplace entry and sourcing1688 runtime state."
  Write-Output "Re-run with -Yes after reviewing. Optional: -CleanUvCache"
  exit 1
}

if (Get-Command codex -ErrorAction SilentlyContinue) {
  try {
    codex plugin marketplace remove sourcing-agent-1688-marketplace
  } catch {
    Write-Output "Marketplace remove failed or was already absent. You can remove it manually in /plugins."
  }
} else {
  Write-Output "codex CLI not found. Remove the plugin from /plugins manually."
}

if (Get-Command sourcing1688 -ErrorAction SilentlyContinue) {
  sourcing1688 uninstall --yes --json
} else {
  Write-Output "sourcing1688 CLI not found. If needed, delete SOURCING1688_HOME manually after checking the path."
}

if ($CleanUvCache) {
  Write-Output "uv cache cleaning is intentionally not automatic. Run 'uv cache clean' yourself if desired."
}
