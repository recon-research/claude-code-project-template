# preflight.ps1 — every merge-blocking gate, locally, in CI order.
# TEMPLATE: replace each `Write-Host "TODO …"` stage body with the real command from
# PROJECT_CONVENTIONS.md > Build & Test (the same commands .github/workflows/ci.yml
# runs — keep the two mirrored: if you change one, change the other).
#
# Run before EVERY push. A clean preflight means CI should be green; a red CI
# after a clean preflight is environmental (read the log, don't guess).
# (POSIX equivalent: scripts/preflight.sh.)
#
# Windows PowerShell 5.1 compatible (no &&, no ternary). Keep output strings
# ASCII: PS 5.1 reads un-BOM'd .ps1 files as ANSI, so non-ASCII renders as mojibake.
#
# Flags: -Quick (static gates only: format + lint) · -SkipSmoke (skip the run-loop gate)
[CmdletBinding()]
param(
    [switch]$Quick,
    [switch]$SkipSmoke
)

Set-Location (Split-Path -Parent $PSScriptRoot)

$script:Failed = $false
$Watch = [System.Diagnostics.Stopwatch]::new()

function Invoke-Stage {
    param([string]$Name, [scriptblock]$Body)
    if ($script:Failed) { return }
    Write-Host "==> $Name" -ForegroundColor Cyan
    $Watch.Restart()
    & $Body
    $code = $LASTEXITCODE
    $secs = [math]::Round($Watch.Elapsed.TotalSeconds, 1)
    if ($null -ne $code -and $code -ne 0) {
        Write-Host "FAIL  $Name (${secs}s, exit $code)" -ForegroundColor Red
        $script:Failed = $true
    }
    else {
        Write-Host "PASS  $Name (${secs}s)" -ForegroundColor Green
    }
}

# --- The gates, in the same order as ci.yml. Replace the placeholders. ---
Invoke-Stage 'format --check' { Write-Host 'TODO: format --check command (PROJECT_CONVENTIONS.md > Format / lint)' }
Invoke-Stage 'lint (warnings as errors)' { Write-Host 'TODO: lint command' }

if (-not $Quick) {
    Invoke-Stage 'build' { Write-Host 'TODO: build command' }
    Invoke-Stage 'test' { Write-Host 'TODO: test command' }
    if (-not $SkipSmoke) {
        # The headless / CI-operability gate (validate_headless_mode). Drop if no run loop.
        Invoke-Stage 'headless smoke' { Write-Host 'TODO: headless gate command' }
    }
}

if ($script:Failed) {
    Write-Host 'PREFLIGHT: FAIL - do not push' -ForegroundColor Red
    exit 1
}
Write-Host 'PREFLIGHT: PASS - safe to push' -ForegroundColor Green
Write-Host '(template note: stages above are TODO placeholders until configure_project fills them)'
exit 0
