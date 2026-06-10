---
name: onboard
description: Start or resume a working session. Use when the user says "welcome back", "let's onboard", "onboard and continue", "let's continue", or opens a fresh session. Branches between first-time onboarding (read the _intake/ brief and set up the project docs + textbook outline) and resuming an in-flight project (preflight, reconcile docs against the tracker, surface the decision queue, pick up the resume point).
---

# Onboard / Resume

The session entry point. Decide which mode you're in, then run it. Token-lean by design: the anchors are small; everything else is read on demand.

## Procedure

**Mode A — First-time onboarding** (the `CLAUDE.md` Status block still has `<placeholders>`, or `_intake/` has new planning docs):
1. Read everything in [`_intake/`](../../_intake/) — the brief, architecture notes, roadmap sketch, domain notes.
2. Fill [`CLAUDE.md`](../../CLAUDE.md): the project name, one-liner, and the **Status** block. Remove the "new project" blockquote.
3. Draft [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) (shape, invariants, the initial `D-NN` decision log) and [`docs/ROADMAP.md`](../../docs/ROADMAP.md) (milestones `M0..`, slices as stepping stones toward the ambitious end-state). Surface unresolved forks as `decision` items with a recommended default.
4. Propose the **textbook/RAG library outline** per [`textbooks/LIBRARY_SEED.md`](../../textbooks/LIBRARY_SEED.md) §1 and get explicit approval. Hand off to [`build_library`](build_library.md).
5. Run [`configure_project`](configure_project.md) to fill [`PROJECT_CONVENTIONS.md`](../../PROJECT_CONVENTIONS.md) once code/tooling exists.
6. **When the repo goes live** (`gh repo create <name> --private --source . --push`):
   - Create the label set from `PROJECT_CONVENTIONS.md` › Tracker & Hygiene: `slice decision followup idea debt blocked research` (one `gh label create <name> -d "<desc>" || true` each — idempotent).
   - Protect `main` (require PRs + green CI) so autopilot can't bypass the gates.
   - **Migrate any `PROJECT_BACKLOG.md` items to issues and delete that file** — once the tracker exists, a second backlog is a staleness machine.

**Mode B — Resume an in-flight project** (the default day-to-day):
1. **Preflight (cheap, mechanical):** `gh auth status` works; `git status` clean (or the dirt is explained by Status); **main CI is green** (`gh run list --branch main -L 1`). A red main is the first slice — never build on red.
2. **Read the anchors only:** the `CLAUDE.md` Status block; the **current milestone section** of [`docs/ROADMAP.md`](../../docs/ROADMAP.md); [`PROJECT_CONVENTIONS.md`](../../PROJECT_CONVENTIONS.md). Don't re-read ARCHITECTURE or the library until the slice routes you there.
3. **Reconcile docs against reality** (truth order: git/CI > tracker > docs > chat): pull `gh issue list --state open` and `git log --oneline -10`; if the Status block's claims or its **As-of** stamp disagree with the tracker / recent merges, **fix Status first**, then proceed. Docs are caches.
4. **Surface the decision queue:** `gh issue list --label decision`. Present a compact digest to the human — `D-NN (#issue) <fork> — recommended: <default> [proceeding provisionally | blocked, slice parked]` — they may answer asynchronously; don't block on it.
5. **Pick up the Resume point** (branch · issue · next action · verify command) and run the [`textbooks/AGENT_GUIDE.md`](../../textbooks/AGENT_GUIDE.md) build loop on the slice. Delegate broad exploration to read-only subagents; keep conclusions, not file dumps.
6. **At a fork**, follow `CLAUDE.md` §3: file the `decision` issue; proceed provisionally if reversible; park-and-switch to the next independent slice if not.

## Verification

- You can state in two sentences: the current milestone, the resume point, and the exact next action.
- Status agrees with the tracker (or was just fixed to); the decision digest was surfaced if any exist.
- Build/test commands came from `PROJECT_CONVENTIONS.md`, not guessed; main was green before new work started.

## Don't

- Don't start coding before the preflight + reconcile — building on a red main or a stale Status multiplies waste.
- Don't re-read the whole ROADMAP / ARCHITECTURE / library "for context" — the anchors are enough; route narrowly when the slice needs it.
- Don't silently resolve a fork to keep momentum, and don't stall on one either — provisional-proceed or park-and-switch per `CLAUDE.md` §3.
- Don't re-litigate decisions already in the `D-NN` log.
- Don't run Mode A again on an onboarded project — confirm the resume point and go.
