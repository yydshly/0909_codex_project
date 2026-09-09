$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot
try {
    if (-not (Test-Path upstream/.git)) {
        git clone https://github.com/FoundationAgents/MetaGPT.git upstream
        if ($LASTEXITCODE -ne 0) { throw 'Source checkout failed.' }
    }
    git -C upstream checkout 11cdf466d042aece04fc6cfd13b28e1a70341b1f
    if ($LASTEXITCODE -ne 0) { throw 'Unable to select the verified source version.' }
    if (-not (Test-Path .venv/Scripts/python.exe)) {
        uv venv .venv --python 3.10
        if ($LASTEXITCODE -ne 0) { throw 'Python environment creation failed.' }
    }
    uv pip install --python .venv/Scripts/python.exe --constraint runtime/requirements.lock.txt --override runtime/windows-overrides.txt -e ./upstream
    if ($LASTEXITCODE -ne 0) { throw 'Dependencies failed to install.' }
    .venv/Scripts/python.exe -X utf8 experiments/run_demo.py
    if ($LASTEXITCODE -ne 0) { throw 'Framework demo failed.' }
} finally {
    Pop-Location
}
