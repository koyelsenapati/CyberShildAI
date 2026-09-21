[CmdletBinding()]
param(
    [string]$Root = "",
    [switch]$SkipPlaywright,
    [switch]$SkipFrontend,
    [switch]$SkipTests,
    [switch]$CreateReleaseZip
)

$ErrorActionPreference = "Continue"

function Write-Section([string]$Text) {
    Write-Host ""
    Write-Host ("=" * 72) -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host ("=" * 72) -ForegroundColor Cyan
}

function Add-Result([int]$No, [string]$Name, [string]$Status, [string]$Evidence) {
    $script:Results += [pscustomobject]@{
        No = $No
        Task = $Name
        Status = $Status
        Evidence = $Evidence
    }

    $color = switch ($Status) {
        "PASS" { "Green" }
        "FAIL" { "Red" }
        "PARTIAL" { "Yellow" }
        "NOT PROVEN" { "Yellow" }
        "SKIPPED" { "DarkGray" }
        default { "White" }
    }

    Write-Host ("[{0}] {1} - {2}" -f $Status, $No, $Name) -ForegroundColor $color
    if ($Evidence) {
        Write-Host ("       " + $Evidence) -ForegroundColor DarkGray
    }
}

function Run-Command {
    param(
        [string]$FilePath,
        [string[]]$Arguments,
        [string]$WorkingDirectory,
        [int]$TimeoutSeconds = 900
    )

    $stdout = [IO.Path]::GetTempFileName()
    $stderr = [IO.Path]::GetTempFileName()

    try {
        $p = Start-Process `
            -FilePath $FilePath `
            -ArgumentList $Arguments `
            -WorkingDirectory $WorkingDirectory `
            -NoNewWindow `
            -Wait `
            -PassThru `
            -RedirectStandardOutput $stdout `
            -RedirectStandardError $stderr

        $out = if (Test-Path $stdout) { Get-Content $stdout -Raw } else { "" }
        $err = if (Test-Path $stderr) { Get-Content $stderr -Raw } else { "" }

        return [pscustomobject]@{
            ExitCode = $p.ExitCode
            Output = (($out + "`n" + $err).Trim())
        }
    }
    finally {
        Remove-Item $stdout,$stderr -Force -ErrorAction SilentlyContinue
    }
}

if ([string]::IsNullOrWhiteSpace($Root)) {
    $scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    $candidate = Split-Path -Parent (Split-Path -Parent $scriptRoot)

    if (Test-Path (Join-Path $candidate "backend")) {
        $Root = $candidate
    }
    else {
        $Root = (Get-Location).Path
    }
}

$Root = (Resolve-Path $Root).Path
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$Reports = Join-Path $Root "reports"
$Tools = Join-Path $Root "tools"
$Main = Join-Path $Backend "app\main.py"
$PytestIni = Join-Path $Backend "pytest.ini"
$Python = Join-Path $Backend ".venv\Scripts\python.exe"
$Report = Join-Path $Reports "final-release-report.md"

New-Item -ItemType Directory -Path $Reports -Force | Out-Null
New-Item -ItemType Directory -Path $Tools -Force | Out-Null

$Results = @()
$Evidence = @()
$OverallHardFailures = 0
$Unproven = 0

Write-Host ""
Write-Host "CYBERSHIELD AI - 12-STEP RELEASE VERIFICATION" -ForegroundColor Cyan
Write-Host "Root: $Root"
Write-Host "Mode: VERIFY ONLY - no source rewrite is performed." -ForegroundColor Yellow

if (-not (Test-Path $Backend)) {
    throw "Backend directory not found: $Backend"
}

if (-not (Test-Path $Main)) {
    throw "main.py not found: $Main"
}

if (-not (Test-Path $Python)) {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) {
        $Python = $cmd.Source
    }
    else {
        throw "Python virtual environment and system Python were not found."
    }
}

# -------------------------------------------------------------------
# 1. FastAPI compile + import + 5 PRD routes + OpenAPI
# -------------------------------------------------------------------
Write-Section "1 / 12 - FASTAPI ROUTER + OPENAPI"

$r = Run-Command $Python @("-m","compileall","-q","app") $Backend 900
if ($r.ExitCode -eq 0) {
    $s1a = "PASS"
} else {
    $s1a = "FAIL"
    $OverallHardFailures++
    $Evidence += "Step 1 compile failed:`n$r.Output"
}

$r2 = Run-Command $Python @("-c","from app.main import app; print('APPLICATION_IMPORT=PASS')") $Backend 900
if ($r2.ExitCode -eq 0) {
    $s1b = "PASS"
} else {
    $s1b = "FAIL"
    $OverallHardFailures++
    $Evidence += "Step 1 application import failed:`n$r2.Output"
}

$routePy = @'
from app.main import app

expected = {
    "/password/analyze",
    "/malware-hash/analyze",
    "/incidents/",
    "/incidents/{incident_id}",
    "/email-phishing/analyze",
}

actual = {getattr(r, "path", "") for r in app.routes if hasattr(r, "path")}
missing = sorted(expected - actual)

for p in sorted(expected):
    print(("PASS: " if p in actual else "FAIL: ") + p)

print("NEW_PRD_ROUTES_PASS=" + str(not missing))
print("TOTAL_ROUTES=" + str(len(actual)))

schema = app.openapi()
paths = set(schema.get("paths", {}).keys())
missing_openapi = sorted(expected - paths)

for p in sorted(expected):
    print(("OPENAPI PASS: " if p in paths else "OPENAPI FAIL: ") + p)

print("OPENAPI_PRD_ROUTES_PASS=" + str(not missing_openapi))
print("OPENAPI_TOTAL_PATHS=" + str(len(paths)))
'@

$routeFile = Join-Path $Reports "_route_verify.py"
Set-Content $routeFile $routePy -Encoding UTF8
$r3 = Run-Command $Python @($routeFile) $Backend 900
Remove-Item $routeFile -Force -ErrorAction SilentlyContinue

if ($r3.ExitCode -eq 0 -and $r3.Output -match "NEW_PRD_ROUTES_PASS=True" -and $r3.Output -match "OPENAPI_PRD_ROUTES_PASS=True") {
    $s1c = "PASS"
} else {
    $s1c = "FAIL"
    $OverallHardFailures++
    $Evidence += "Step 1 route/OpenAPI verification failed:`n$r3.Output"
}

if ($s1a -eq "PASS" -and $s1b -eq "PASS" -and $s1c -eq "PASS") {
    Add-Result 1 "FastAPI compile + application import + 5 PRD routes + OpenAPI verification" "PASS" "Compile, import, route set and OpenAPI route set all passed."
} else {
    Add-Result 1 "FastAPI compile + application import + 5 PRD routes + OpenAPI verification" "FAIL" "One or more FastAPI gates failed."
}

# -------------------------------------------------------------------
# 2. Authentication/security/current_user ownership
# -------------------------------------------------------------------
Write-Section "2 / 12 - AUTHENTICATION + OWNERSHIP"

$apiPy = Get-ChildItem (Join-Path $Backend "app") -Recurse -Filter *.py -File
$authHits = @()
$currentUserHits = 0
$dangerousDevHits = @()

foreach ($f in $apiPy) {
    $t = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
    if ($t -match "current_user") { $currentUserHits++ }

    if ($t -match "(?i)(dev[-_ ]?token|development[-_ ]?token|bypass.*auth|auth.*bypass|skip.*auth|disable.*auth)") {
        $dangerousDevHits += $f.FullName
    }

    if ($t -match "current_user") {
        $authHits += $f.FullName
    }
}

if ($dangerousDevHits.Count -eq 0) {
    $devGate = "PASS"
} else {
    $devGate = "FAIL"
    $OverallHardFailures++
}

if ($currentUserHits -gt 0) {
    $ownerGate = "PASS"
} else {
    $ownerGate = "NOT PROVEN"
    $Unproven++
}

$authTests = Get-ChildItem (Join-Path $Backend "tests") -Recurse -Filter *.py -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "auth|security|ownership|user|permission|access" }

if ($devGate -eq "PASS" -and $ownerGate -eq "PASS" -and $authTests.Count -gt 0) {
    Add-Result 2 "Authentication/security + dev-token bypass + backend current_user ownership isolation" "PASS" "No dev-token/bypass keyword found; current_user is used; auth/security/ownership tests exist."
} elseif ($devGate -eq "FAIL") {
    Add-Result 2 "Authentication/security + dev-token bypass + backend current_user ownership isolation" "FAIL" "Potential authentication bypass keyword found: $($dangerousDevHits -join '; ')"
} else {
    Add-Result 2 "Authentication/security + dev-token bypass + backend current_user ownership isolation" "NOT PROVEN" "Static evidence is incomplete; current_user references=$currentUserHits, relevant tests=$($authTests.Count)."
}

# -------------------------------------------------------------------
# 3. Real scanner result / no fake data
# -------------------------------------------------------------------
Write-Section "3 / 12 - REAL SCANNER DATA AUDIT"

$scannerFiles = @(
    "app\security_engine\network_scanner.py",
    "app\security_engine\vulnerability_scanner.py",
    "app\api\network_scan.py",
    "app\api\vulnerability_scan.py",
    "app\services\network_service.py",
    "app\services\vulnerability_service.py"
)

$scannerMissing = @()
$fakeHits = @()

foreach ($rel in $scannerFiles) {
    $fp = Join-Path $Backend $rel
    if (-not (Test-Path $fp)) {
        $scannerMissing += $rel
        continue
    }

    $txt = Get-Content $fp -Raw
    if ($txt -match "(?i)(mock|dummy|fake|placeholder|demo[_ -]?data|sample[_ -]?data)") {
        $fakeHits += $rel
    }
}

if ($scannerMissing.Count -eq 0 -and $fakeHits.Count -eq 0) {
    Add-Result 3 "All scanners use real results; mock/demo/fake/placeholder security data removed" "PASS" "Required scanner files exist and no configured fake-data keywords were found."
} elseif ($fakeHits.Count -gt 0) {
    Add-Result 3 "All scanners use real results; mock/demo/fake/placeholder security data removed" "FAIL" "Potential fake-data keyword found in: $($fakeHits -join '; ')"
    $OverallHardFailures++
} else {
    Add-Result 3 "All scanners use real results; mock/demo/fake/placeholder security data removed" "FAIL" "Missing scanner files: $($scannerMissing -join '; ')"
    $OverallHardFailures++
}

# -------------------------------------------------------------------
# 4. Master scan schema + flow
# -------------------------------------------------------------------
Write-Section "4 / 12 - MASTER SCAN"

$masterFiles = @(
    "app\api\master_scan.py",
    "app\schemas\master_scan.py",
    "app\crud\master_scan.py",
    "app\models\master_scan.py"
)

$masterMissing = @($masterFiles | Where-Object { -not (Test-Path (Join-Path $Backend $_)) })

$masterText = ""
foreach ($rel in $masterFiles) {
    $fp = Join-Path $Backend $rel
    if (Test-Path $fp) { $masterText += "`n" + (Get-Content $fp -Raw) }
}

$masterSignals = 0
foreach ($term in @("current_user","scan","history","status","result","db")) {
    if ($masterText -match [regex]::Escape($term)) { $masterSignals++ }
}

if ($masterMissing.Count -eq 0 -and $masterSignals -ge 5) {
    Add-Result 4 "master_scan schema + scan/history/details/ownership flow" "PASS" "Required master-scan layers exist with expected flow/ownership signals."
} else {
    Add-Result 4 "master_scan schema + scan/history/details/ownership flow" "NOT PROVEN" "Missing=$($masterMissing -join '; '); expected signals=$masterSignals/6."
    $Unproven++
}

# -------------------------------------------------------------------
# 5. Alerts / Reports / File Integrity ownership
# -------------------------------------------------------------------
Write-Section "5 / 12 - ALERTS + REPORTS + FILE INTEGRITY"

$accessFiles = @(
    "app\api\alert.py",
    "app\api\reports.py",
    "app\api\file_integrity.py",
    "app\crud\alert.py",
    "app\crud\file_integrity.py"
)

$missing5 = @()
$weakOwnership = @()

foreach ($rel in $accessFiles) {
    $fp = Join-Path $Backend $rel
    if (-not (Test-Path $fp)) {
        $missing5 += $rel
        continue
    }

    $txt = Get-Content $fp -Raw
    if ($rel -like "app\api\*") {
        if ($txt -notmatch "current_user") {
            $weakOwnership += $rel
        }
    }
}

if ($missing5.Count -eq 0 -and $weakOwnership.Count -eq 0) {
    Add-Result 5 "Alerts, Reports, File Integrity ownership/access control" "PASS" "Required API/CRUD files exist and API layers reference current_user."
} else {
    Add-Result 5 "Alerts, Reports, File Integrity ownership/access control" "NOT PROVEN" "Missing=$($missing5 -join '; '); APIs without current_user=$($weakOwnership -join '; ')."
    $Unproven++
}

# -------------------------------------------------------------------
# 6. Duplicate router/file + main.py structure
# -------------------------------------------------------------------
Write-Section "6 / 12 - DUPLICATE ROUTER + MAIN STRUCTURE"

$includeLines = Select-String -Path $Main -Pattern "app\.include_router\(" -ErrorAction SilentlyContinue
$duplicateRegistrations = $includeLines |
    ForEach-Object { $_.Line.Trim() } |
    Group-Object |
    Where-Object { $_.Count -gt 1 }

$routerFiles = Get-ChildItem (Join-Path $Backend "app\api") -Filter *.py -File |
    Group-Object BaseName |
    Where-Object { $_.Count -gt 1 }

if ($duplicateRegistrations.Count -eq 0 -and $routerFiles.Count -eq 0) {
    Add-Result 6 "Duplicate router/file + main.py structure verification" "PASS" "No duplicate include_router registrations or duplicate API basenames detected."
} else {
    $details = @()
    if ($duplicateRegistrations.Count -gt 0) {
        $details += "duplicate registrations: " + (($duplicateRegistrations | ForEach-Object { "$($_.Name) x$($_.Count)" }) -join ", ")
    }
    if ($routerFiles.Count -gt 0) {
        $details += "duplicate API basenames: " + (($routerFiles | ForEach-Object Name) -join ", ")
    }
    Add-Result 6 "Duplicate router/file + main.py structure verification" "FAIL" ($details -join " | ")
    $OverallHardFailures++
}

# -------------------------------------------------------------------
# 7. Frontend API/auth/WebSocket consistency
# -------------------------------------------------------------------
Write-Section "7 / 12 - FRONTEND API + AUTH + WEBSOCKET"

$apiTs = Join-Path $Frontend "src\services\api.ts"
$vite = Join-Path $Frontend "vite.config.ts"
$authStoreCandidates = Get-ChildItem (Join-Path $Frontend "src") -Recurse -Include *.ts,*.tsx -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "auth|store" }

$apiText = if (Test-Path $apiTs) { Get-Content $apiTs -Raw } else { "" }
$viteText = if (Test-Path $vite) { Get-Content $vite -Raw } else { "" }

$signals7 = 0
if ($apiText -match "VITE_API_BASE_URL") { $signals7++ }
if ($apiText -match "Authorization") { $signals7++ }
if ($apiText -match "access_token|useAuthStore") { $signals7++ }
if ($viteText -match "/api/v1") { $signals7++ }
if ($viteText -match "/ws") { $signals7++ }

$wsFiles = Get-ChildItem (Join-Path $Frontend "src") -Recurse -Include *.ts,*.tsx -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match "websocket|socket" }

if ($signals7 -ge 4 -and $wsFiles.Count -gt 0) {
    Add-Result 7 "Frontend API paths + auth token consistency + WebSocket token handling" "PASS" "Expected API/auth/proxy/WebSocket integration signals found."
} else {
    Add-Result 7 "Frontend API paths + auth token consistency + WebSocket token handling" "NOT PROVEN" "Integration signals=$signals7/5; websocket files=$($wsFiles.Count)."
    $Unproven++
}

# -------------------------------------------------------------------
# 8. TypeScript + build + Playwright
# -------------------------------------------------------------------
Write-Section "8 / 12 - FRONTEND BUILD + TYPESCRIPT + PLAYWRIGHT"

if ($SkipFrontend -or -not (Test-Path (Join-Path $Frontend "package.json"))) {
    Add-Result 8 "Frontend TypeScript/build + Playwright verification" "SKIPPED" "Frontend verification skipped or package.json missing."
} else {
    $build = Run-Command "npm.cmd" @("run","build") $Frontend 1800

    $tsconfig = Test-Path (Join-Path $Frontend "tsconfig.json")
    if ($tsconfig) {
        $ts = Run-Command "npx.cmd" @("tsc","--noEmit") $Frontend 1200
    } else {
        $ts = [pscustomobject]@{ ExitCode = 0; Output = "tsconfig.json not present; TypeScript gate covered by npm build." }
    }

    $pw = $null
    if (-not $SkipPlaywright -and (Test-Path (Join-Path $Frontend "playwright.config.ts") -or Test-Path (Join-Path $Frontend "playwright.config.js"))) {
        $pw = Run-Command "npx.cmd" @("playwright","test") $Frontend 2400
    }

    $buildPass = $build.ExitCode -eq 0
    $tsPass = $ts.ExitCode -eq 0
    $pwPass = ($null -eq $pw) -or ($pw.ExitCode -eq 0)

    if ($buildPass -and $tsPass -and $pwPass) {
        Add-Result 8 "Frontend TypeScript/build + Playwright verification" "PASS" "npm build, tsc, and configured Playwright suite passed."
    } else {
        $out = "build=$($build.ExitCode); tsc=$($ts.ExitCode)"
        if ($null -ne $pw) { $out += "; playwright=$($pw.ExitCode)" }
        Add-Result 8 "Frontend TypeScript/build + Playwright verification" "FAIL" $out
        $OverallHardFailures++
        $Evidence += "Step 8 output:`nBUILD:`n$($build.Output)`nTSC:`n$($ts.Output)`nPLAYWRIGHT:`n$(if($pw){$pw.Output}else{'not run'})"
    }
}

# -------------------------------------------------------------------
# 9. Full backend pytest
# -------------------------------------------------------------------
Write-Section "9 / 12 - FULL BACKEND PYTEST"

if ($SkipTests -or -not (Test-Path (Join-Path $Backend "tests"))) {
    Add-Result 9 "Full backend pytest; genuine failures only" "SKIPPED" "Tests skipped or tests directory missing."
} else {
    $testEnv = @{
        DATABASE_URL = "sqlite:///$((Join-Path $Reports 'audit_test.db').Replace('\','/'))"
        SECRET_KEY = "audit-test-secret-not-for-production"
        ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = "30"
    }

    $oldEnv = @{}
    foreach ($k in $testEnv.Keys) {
        $oldEnv[$k] = [Environment]::GetEnvironmentVariable($k, "Process")
        [Environment]::SetEnvironmentVariable($k, $testEnv[$k], "Process")
    }

    try {
        $pytest = Run-Command $Python @("-m","pytest","-q") $Backend 2400
    }
    finally {
        foreach ($k in $testEnv.Keys) {
            [Environment]::SetEnvironmentVariable($k, $oldEnv[$k], "Process")
        }
    }

    if ($pytest.ExitCode -eq 0) {
        Add-Result 9 "Full backend pytest; genuine failures only" "PASS" "pytest exited 0."
    } else {
        Add-Result 9 "Full backend pytest; genuine failures only" "FAIL" "pytest exit code=$($pytest.ExitCode)"
        $OverallHardFailures++
        $Evidence += "Step 9 pytest output:`n$($pytest.Output)"
    }
}

# -------------------------------------------------------------------
# 10. Backend + frontend + MySQL/Alembic E2E readiness
# -------------------------------------------------------------------
Write-Section "10 / 12 - E2E + MYSQL + ALEMBIC"

$alembicIni = Join-Path $Backend "alembic.ini"
if (Test-Path $alembicIni) {
    $heads = Run-Command $Python @("-m","alembic","heads") $Backend 900
    $migrationPass = $heads.ExitCode -eq 0
} else {
    $heads = $null
    $migrationPass = $false
}

$envFile = Join-Path $Backend ".env"
$mysqlConfigured = Test-Path $envFile

$liveHealth = $false
try {
    $health = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    $liveHealth = $health.StatusCode -eq 200
} catch {
    $liveHealth = $false
}

if ($migrationPass -and $mysqlConfigured -and $liveHealth) {
    Add-Result 10 "Backend + frontend + MySQL/Alembic end-to-end release verification" "PASS" "Alembic heads passed, backend .env exists, and live /health returned 200."
} elseif ($migrationPass -and $mysqlConfigured) {
    Add-Result 10 "Backend + frontend + MySQL/Alembic end-to-end release verification" "NOT PROVEN" "Alembic and DB configuration are present, but live backend /health was not available."
    $Unproven++
} else {
    Add-Result 10 "Backend + frontend + MySQL/Alembic end-to-end release verification" "FAIL" "Alembic=$($heads.ExitCode); .env=$mysqlConfigured; live_health=$liveHealth."
    $OverallHardFailures++
}

# -------------------------------------------------------------------
# 11. Report + release ZIP
# -------------------------------------------------------------------
Write-Section "11 / 12 - FINAL REPORT + RELEASE ARTIFACT"

$generated = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"

$md = @()
$md += "# CyberShield AI - Final Release Verification"
$md += ""
$md += "Generated: $generated"
$md += ""
$md += "Mode: VERIFY ONLY. No source files were rewritten by this script."
$md += ""
$md += "## 12-Step Result"
$md += ""
$md += "| # | Task | Status | Evidence |"
$md += "|---:|---|---|---|"

foreach ($x in $Results) {
    $safe = ($x.Evidence -replace "\|","/")
    $md += "| $($x.No) | $($x.Task) | $($x.Status) | $safe |"
}

$md += ""
$md += "## Final Gate"
$md += ""
if ($OverallHardFailures -eq 0 -and $Unproven -eq 0 -and $Results.Count -eq 10) {
    $verdict = "VERIFICATION PASSED"
    $md += "**VERDICT: $verdict**"
    $md += ""
    $md += "Steps 1-10 passed. Step 11 generated this report. Step 12 is the final production verdict gate."
} elseif ($OverallHardFailures -gt 0) {
    $verdict = "NOT PRODUCTION READY"
    $md += "**VERDICT: $verdict**"
    $md += ""
    $md += "One or more required automated gates failed."
} else {
    $verdict = "NOT PROVEN"
    $md += "**VERDICT: $verdict**"
    $md += ""
    $md += "No hard failure was detected, but one or more required gates remain unproven."
}

$md += ""
$md += "## Important"
$md += ""
$md += "This automated gate does not replace manual security review, penetration testing, dependency review, infrastructure review, or production credential validation."

if ($Evidence.Count -gt 0) {
    $md += ""
    $md += "## Failure Evidence"
    $md += ""
    foreach ($e in $Evidence) {
        $md += '```text'
        $md += $e
        $md += '```'
    }
}

Set-Content $Report ($md -join "`n") -Encoding UTF8
Add-Result 11 "Final audit/release report + release ZIP" "PASS" "Report generated: $Report"

# ZIP only when every automated gate passed.
if ($CreateReleaseZip -and $OverallHardFailures -eq 0 -and $Unproven -eq 0) {
    $ReleaseDir = Join-Path $Root "release"
    New-Item -ItemType Directory -Path $ReleaseDir -Force | Out-Null
    $Zip = Join-Path $ReleaseDir ("CyberShield-AI-verified-" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".zip")

    $exclude = @(
        "\.git($|\\)",
        "\\backend\\\.venv($|\\)",
        "\\node_modules($|\\)",
        "\\__pycache__($|\\)",
        "\\\.pytest_cache($|\\)",
        "\\audit_test\.db$"
    )

    $files = Get-ChildItem $Root -Recurse -File | Where-Object {
        $rel = $_.FullName.Substring($Root.Length)
        ($exclude | Where-Object { $rel -match $_ }).Count -eq 0
    }

    Compress-Archive -Path ($files.FullName) -DestinationPath $Zip -Force
    $Evidence += "Release ZIP: $Zip"
} elseif ($CreateReleaseZip) {
    $Evidence += "Release ZIP was NOT created because all required gates did not pass."
}

# -------------------------------------------------------------------
# 12. Production-ready verdict
# -------------------------------------------------------------------
Write-Section "12 / 12 - PRODUCTION-READY VERDICT"

$required = $Results | Where-Object { $_.No -le 10 -and $_.Status -ne "PASS" }

if ($required.Count -eq 0 -and $OverallHardFailures -eq 0 -and $Unproven -eq 0) {
    Add-Result 12 "Production-ready verdict after all verification passes" "PASS" "All required automated gates passed."
    $finalVerdict = "PRODUCTION READY"
} else {
    Add-Result 12 "Production-ready verdict after all verification passes" "FAIL" "Production-ready verdict withheld. Required gates are still failing or unproven."
    $finalVerdict = "NOT PRODUCTION READY"
}

# Rewrite report with steps 11-12 included.
$md = @()
$md += "# CyberShield AI - Final Release Verification"
$md += ""
$md += "Generated: $generated"
$md += ""
$md += "Mode: VERIFY ONLY. No source files were rewritten by this script."
$md += ""
$md += "## 12-Step Result"
$md += ""
$md += "| # | Task | Status | Evidence |"
$md += "|---:|---|---|---|"
foreach ($x in $Results) {
    $safe = ($x.Evidence -replace "\|","/")
    $md += "| $($x.No) | $($x.Task) | $($x.Status) | $safe |"
}
$md += ""
$md += "## FINAL VERDICT"
$md += ""
$md += "**$finalVerdict**"
$md += ""
$md += "Hard failures: $OverallHardFailures"
$md += ""
$md += "Unproven gates: $Unproven"
$md += ""
$md += "This report is evidence of automated verification only. It does not replace manual security assessment."

Set-Content $Report ($md -join "`n") -Encoding UTF8

Write-Host ""
Write-Host ("=" * 72) -ForegroundColor Cyan
Write-Host "FINAL VERDICT: $finalVerdict" -ForegroundColor $(if ($finalVerdict -eq "PRODUCTION READY") {"Green"} else {"Red"})
Write-Host "REPORT: $Report" -ForegroundColor White
Write-Host ("=" * 72) -ForegroundColor Cyan

if ($finalVerdict -eq "PRODUCTION READY") {
    exit 0
} else {
    exit 2
}
