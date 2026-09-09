param([switch]$WithAgent)
$ErrorActionPreference = 'Stop'
$localRoot = Join-Path $PSScriptRoot 'runtime/local'
if (-not (Test-Path (Join-Path $localRoot 'config.json'))) { throw '请先按 README 完成本地环境初始化。' }
$pgCtl = Join-Path (Split-Path (Get-Command psql.exe).Source) 'pg_ctl.exe'
& $pgCtl -D (Join-Path $localRoot 'pgdata') status | Out-Null
if ($LASTEXITCODE -ne 0) { & $pgCtl -D (Join-Path $localRoot 'pgdata') -l (Join-Path $localRoot 'postgres.log') start }
$services = @('backend','web','research')
if ($WithAgent) { $services += 'daemon' }
$taskShell = (Get-Process -Id $PID).Path
foreach ($service in $services) {
  $pidPath = Join-Path $localRoot "$service.pid"
  if (Test-Path $pidPath) {
    $recordedId = [int](Get-Content $pidPath)
    $existing = Get-CimInstance Win32_Process -Filter "ProcessId = $recordedId"
    if ($existing -and $existing.CommandLine.Contains($PSScriptRoot) -and $existing.CommandLine.Contains('launch-service.ps1')) { Write-Output "$service 已运行"; continue }
  }
  $proc = Start-Process -FilePath $taskShell -WindowStyle Hidden -ArgumentList @('-NoProfile','-File',(Join-Path $PSScriptRoot 'runtime/launch-service.ps1'),'-Service',$service) -RedirectStandardOutput (Join-Path $localRoot "$service.out.log") -RedirectStandardError (Join-Path $localRoot "$service.err.log") -PassThru
  $proc.Id | Set-Content $pidPath
  Write-Output "$service 已启动"
}
Write-Output '研究页：http://127.0.0.1:8011'
Write-Output '原版应用：http://localhost:3111/multica-lab/issues'
Write-Output '服务首次打开页面时会编译，请稍候。'
