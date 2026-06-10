---
name: definition_of_done
description: Run the full definition-of-done verification gate for a subsystem or change — build, tests, domain checks, anti-patterns, determinism, profile, milestone exit — and report pass/fail per gate with evidence before declaring work complete. Use when the user says "is this done", "verify the subsystem", "run the gates", "definition of done", or before claiming a feature is finished. Broader than build_and_test (which is only build + test).
---

# Definition Of Done (Verification Gate)

Runs the full verification gate from AGENT_GUIDE §2 against a subsystem or change, so "is this done?" is answered with evidence, not vibes. Read paths and commands from `PROJECT_CONVENTIONS.md`.

## Procedure

**Mechanical first:** `scripts/preflight.sh` (or `scripts\preflight.ps1`) runs the CI-mirrored gate set (format, lint, build, test, run-loop smoke) locally in CI order — run it, attach its PASS line as the evidence for gates 1–2 (and 5 where it applies), then assess the judgment gates.

Run each gate that applies; record **PASS / FAIL / N/A** with evidence:

1. **Builds clean** — `build_and_test` passes; no new warnings the project treats as errors.
2. **Tests** — has tests appropriate to its kind (`add_test`: unit / integration / property / golden) and they pass.
3. **Domain checks** — the verification specific to this kind of change passes (whatever the library / `PROJECT_CONVENTIONS.md` mandates for this area — e.g. schema / data-contract validation, security or safety checks, accessibility, migration round-trips). The next two gates are the common domain checks for stateful, run-loop systems; apply them only when they fit.
4. **State round-trip** *(if the system owns state)* — `snapshot_restore_test` round-trips (mandatory where state must reset, replay, or roll back; otherwise N/A).
5. **Headless / CI-operability** *(if the system has a run loop)* — `validate_headless_mode` still passes: it initializes, runs, and shuts down with no hard dependency on a window, audio/input device, or human (otherwise N/A).
6. **Anti-patterns** — the cataloged failure modes for this subsystem (ANTI_PATTERNS / SYMPTOMS) are explicitly avoided or guarded. For a substantial feature, confirm `adversarial_review`'s Must-fix findings are resolved — run it now if it wasn't already run earlier in the workflow; don't re-run a fan-out that already happened.
7. **Determinism** *(if the system requires reproducibility)* — preserved where the library requires it (fixed-step simulation, seeded generation + recorded inputs, replay); otherwise N/A.
8. **Performance** — any performance claim is backed by a profile (`profile_subsystem`), not a guess.
9. **Milestone** — if this work closes a milestone, the ROADMAP / STARTER_KIT milestone exit criterion is met.
10. **Backlog & deferrals** — completion is reflected in the tracker (the PR closes its slice issue); every deferred finding has a ticket (`track_followups`); and the diff introduces **no naked TODO/FIXME** — only `TODO(#NN)` with a filed issue. Quick check (should print nothing): `git diff origin/main...HEAD -- ':!*.md' ':!textbooks' | grep -E '^\+.*\b(TODO|FIXME)\b' | grep -vE '\(#[0-9]+\)'`.
11. **Merge-time checkpoint** — the `CLAUDE.md` Status line and the ROADMAP slice state reflect this merge (the standing checkpoint-at-every-merge rule).

## Output

A checklist with each gate marked PASS / FAIL / N/A and the **evidence** attached (command output, profile capture, test name). **Do not declare the work done unless every applicable gate is PASS.** A FAIL routes back to fix-then-re-run (hand redesign to `plan_work`).

## Verification

- Every applicable gate was actually executed (not assumed).
- Each result carries evidence.
- N/A gates have a one-line reason (e.g. "stateless — no run loop").

## Don't

- Don't declare "done" with an unrun or failing gate.
- Don't skip the state round-trip / headless gates when they *do* apply (stateful or run-loop systems) — those are the ones that ship broken.
- Don't accept a performance claim without a profile.
- Don't re-implement what `build_and_test`, `validate_headless_mode`, `snapshot_restore_test`, and `profile_subsystem` already do — this skill *orchestrates* them.
