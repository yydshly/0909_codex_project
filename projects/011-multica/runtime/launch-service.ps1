param([ValidateSet('backend','web','research','daemon')][string]$Service)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$localRoot = Join-Path $PSScriptRoot 'local'
$config = Get-Content (Join-Path $localRoot 'config.json') -Raw | ConvertFrom-Json
$config.PSObject.Properties | ForEach-Object { [Environment]::SetEnvironmentVariable($_.Name, [string]$_.Value, 'Process') }
switch ($Service) {
  'backend' { Set-Location $localRoot; & (Join-Path $PSScriptRoot 'bin/multica-server.exe') }
  'web' { Set-Location (Join-Path $projectRoot 'upstream/apps/web'); & (Get-Command node.exe).Source 'node_modules/next/dist/bin/next' dev --webpack --hostname 127.0.0.1 --port 3111 }
  'research' { Set-Location $projectRoot; & (Get-Command python.exe).Source -m http.server 8011 --bind 127.0.0.1 --directory web }
  'daemon' { Set-Location $localRoot; & (Join-Path $PSScriptRoot 'bin/multica.exe') --profile multica-research-011 daemon start --foreground --no-auto-update --no-auto-reload --workspaces-root (Join-Path $localRoot 'workspaces') }
}
