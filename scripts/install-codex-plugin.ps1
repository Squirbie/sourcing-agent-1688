param(
  [string]$Source = "."
)

$ErrorActionPreference = "Stop"
$UVX_SOURCE = $Source
# uvx expects Git URLs as git+https://... while codex marketplace add accepts the original URL.
if ($Source -match '^https?://' -and -not $Source.StartsWith('git+')) {
  $UVX_SOURCE = "git+$Source"
}

if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
  Write-Error "codex CLI not found. Add the marketplace manually from Codex."
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  Write-Error "uv not found. Install uv before running sourcing1688."
}

Write-Output "Adding Codex plugin marketplace: $Source"
try {
  codex plugin marketplace add $Source
  Write-Output "Marketplace added. Open /plugins in Codex and install sourcing-agent-1688."
} catch {
  Write-Output "Automatic marketplace add failed. Run manually: codex plugin marketplace add $Source"
}

if (Get-Command sourcing1688 -ErrorAction SilentlyContinue) {
  sourcing1688 init-home --json
} else {
  uvx --from $UVX_SOURCE sourcing1688 init-home --json
}

Write-Output "After install, run: sourcing1688 provider-check --provider auto --json"
