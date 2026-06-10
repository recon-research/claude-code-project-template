#!/usr/bin/env bash
# preflight.sh — every merge-blocking gate, locally, in CI order.
# TEMPLATE: replace each `echo "TODO …"` stage body with the real command from
# PROJECT_CONVENTIONS.md › Build & Test (the same commands .github/workflows/ci.yml
# runs — keep the two mirrored: if you change one, change the other).
#
# Run before EVERY push. A clean preflight means CI should be green; a red CI
# after a clean preflight is environmental (read the log, don't guess). This
# kills the "fix one lint, push, wait for CI to find the next one" loop.
# (Windows-native equivalent: scripts/preflight.ps1.)
#
# Flags: --quick (static gates only: format + lint) · --skip-smoke (skip the run-loop gate)
set -u
cd "$(dirname "$0")/.."

QUICK=0
SKIP_SMOKE=0
for arg in "$@"; do
    case "$arg" in
        --quick) QUICK=1 ;;
        --skip-smoke) SKIP_SMOKE=1 ;;
        *) echo "unknown flag: $arg (use --quick, --skip-smoke)" >&2; exit 2 ;;
    esac
done

FAILED=0
stage() {
    local name="$1"; shift
    [ "$FAILED" -ne 0 ] && return 0
    echo "==> $name"
    local t0=$SECONDS
    if "$@"; then
        echo "PASS  $name ($((SECONDS - t0))s)"
    else
        echo "FAIL  $name ($((SECONDS - t0))s)"
        FAILED=1
    fi
}

# --- The gates, in the same order as ci.yml. Replace the echo placeholders. ---
stage "format --check" echo "TODO: format --check command (PROJECT_CONVENTIONS.md > Format / lint)"
stage "lint (warnings as errors)" echo "TODO: lint command"

if [ "$QUICK" -eq 0 ]; then
    stage "build" echo "TODO: build command"
    stage "test" echo "TODO: test command"
    if [ "$SKIP_SMOKE" -eq 0 ]; then
        # The headless / CI-operability gate (validate_headless_mode). Drop if no run loop.
        stage "headless smoke" echo "TODO: headless gate command"
    fi
fi

if [ "$FAILED" -ne 0 ]; then
    echo "PREFLIGHT: FAIL — do not push"
    exit 1
fi
echo "PREFLIGHT: PASS — safe to push"
echo "(template note: stages above are TODO placeholders until configure_project fills them)"
