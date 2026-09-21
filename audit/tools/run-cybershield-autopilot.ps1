param(
    [int]$StartPhase = 1,
    [int]$MaxRounds = 20,
    [switch]$Once,
    [string]$RepairCommand = ""
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

Set-Location $Root

$ReportDir = Join-Path $Root "audit\audit-results"

New-Item -ItemType Directory -Force $ReportDir | Out-Null

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " CYBERSHIELD AI CONTINUOUS AUTOPILOT" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository : $Root"
Write-Host "Scope      : Phase $StartPhase -> Phase 15"
Write-Host "Max Rounds : $MaxRounds"
Write-Host ""

$VenvPython = Join-Path $Root "backend\.venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    $Python = $VenvPython
    Write-Host "Python     : backend\.venv" -ForegroundColor Green
}
else {
    $PythonCommand = Get-Command python -ErrorAction SilentlyContinue

    if (-not $PythonCommand) {
        $PythonCommand = Get-Command py -ErrorAction SilentlyContinue
    }

    if (-not $PythonCommand) {
        throw "Python was not found."
    }

    $Python = $PythonCommand.Source
    Write-Host "Python     : system Python" -ForegroundColor Yellow
}

$Script = Join-Path $Root "audit\tools\cybershield_autopilot.py"

if (-not (Test-Path $Script)) {
    throw "Missing file: $Script"
}

$Arguments = @(
    $Script
    "--start-phase"
    "$StartPhase"
    "--max-rounds"
    "$MaxRounds"
)

if ($Once) {
    $Arguments += "--once"
}

if ($RepairCommand) {
    $Arguments += "--repair-command"
    $Arguments += $RepairCommand
}

Write-Host ""
Write-Host "Starting audit..." -ForegroundColor Cyan
Write-Host ""

& $Python @Arguments

$ExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " AUDIT FINISHED" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Report:"
Write-Host "$ReportDir\audit-report.md"
Write-Host ""

if ($ExitCode -eq 0) {
    Write-Host "OBJECTIVE GATES PASSED." -ForegroundColor Green
}
elseif ($ExitCode -eq 2) {
    Write-Host "ONE-SHOT AUDIT COMPLETED." -ForegroundColor Yellow
}
elseif ($ExitCode -eq 3) {
    Write-Host "ISSUES FOUND. NO REPAIR COMMAND CONFIGURED." -ForegroundColor Yellow
}
elseif ($ExitCode -eq 4) {
    Write-Host "REPAIR AGENT FAILED OR BLOCKED." -ForegroundColor Red
}
elseif ($ExitCode -eq 5) {
    Write-Host "MAXIMUM AUDIT ROUNDS REACHED." -ForegroundColor Red
}
else {
    Write-Host "AUDIT FAILED. EXIT CODE: $ExitCode" -ForegroundColor Red
}

exit $ExitCode