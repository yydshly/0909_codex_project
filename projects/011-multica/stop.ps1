param([switch]$IncludeDatabase)
$ErrorActionPreference = 'Stop'
$localRoot = Join-Path $PSScriptRoot 'runtime/local'
function Stop-OwnedTree([int]$ProcessId) {
  $children = @(Get-CimInstance Win32_Process -Filter "ParentProcessId = $ProcessId")
  foreach ($child in $children) { Stop-OwnedTree $child.ProcessId }
  Stop-Process -Id $ProcessId -ErrorAction SilentlyContinue
}
foreach ($service in @('daemon','web','backend','research')) {
  $pidPath = Join-Path $localRoot "$service.pid"
  if (-not (Test-Path $pidPath)) { continue }
  $recordedId = [int](Get-Content $pidPath)
  $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $recordedId"
  if (-not $proc) { continue }
  if (-not $proc.CommandLine.Contains($PSScriptRoot) -or -not $proc.CommandLine.Contains('launch-service.ps1')) { Write-Warning "$service 的 PID 已不属于本项目，跳过"; continue }
  Stop-OwnedTree $recordedId
  Write-Output "$service 已停止"
}
if ($IncludeDatabase) {
  $pgCtl = Join-Path (Split-Path (Get-Command psql.exe).Source) 'pg_ctl.exe'
  & $pgCtl -D (Join-Path $localRoot 'pgdata') stop -m fast
}
Write-Output '研究文件、数据库和执行产物均保留。'
