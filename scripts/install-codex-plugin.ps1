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
  Write-Output "Marketplace added."
} catch {
  Write-Output "Automatic marketplace add failed. Run manually: codex plugin marketplace add $Source"
}

$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
$CodexConfig = Join-Path $CodexHome "config.toml"
New-Item -ItemType Directory -Force -Path $CodexHome | Out-Null
if (-not (Test-Path $CodexConfig)) {
  New-Item -ItemType File -Force -Path $CodexConfig | Out-Null
}
$PluginBlock = @'

[plugins."sourcing-agent-1688@sourcing-agent-1688-marketplace"]
enabled = true
'@
if (-not (Select-String -Path $CodexConfig -Pattern '[plugins."sourcing-agent-1688@sourcing-agent-1688-marketplace"]' -SimpleMatch -Quiet)) {
  Add-Content -LiteralPath $CodexConfig -Value $PluginBlock
  Write-Output "Plugin enabled in Codex config: sourcing-agent-1688@sourcing-agent-1688-marketplace"
} else {
  Write-Output "Plugin already enabled in Codex config."
}

if (Get-Command sourcing1688 -ErrorAction SilentlyContinue) {
  sourcing1688 init-home --json
} else {
  uvx --from $UVX_SOURCE sourcing1688 init-home --json
}

Write-Output "Restart Codex, then use @1688 Sourcing Agent in a new chat."
Write-Output "After install, run: sourcing1688 provider-check --provider auto --json"
