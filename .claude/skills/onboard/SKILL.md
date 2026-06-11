---
name: onboard
description: Start or resume a working session. Use when the user says "welcome back", "let's onboard", "onboard and continue", "let's continue", or opens a fresh session. Branches between first-time onboarding (read the _intake/ brief and set up the project docs + textbook outline) and resuming an in-flight project (preflight, reconcile docs against the tracker, surface the decision queue, pick up the resume point).
---

# Onboard / Resume

The session entry point. Decide which mode you're in, then run it. Token-lean by design: the anchors are small; everything else is read on demand.

## Session snapshot (auto-rendered when this skill loads)

- Recent commits: !`git log --oneline -5 2>/dev/null || echo "(no git yet)"`
- Working tree: !`git status --porcelain 2>/dev/null | head -15`
- Open decisions: !`gh issue list --label decision --state open 2>/dev/null || echo "(no tracker yet)"`
- Open PRs: !`gh pr list --state open 2>/dev/null || echo "(none / no tracker)"`

## Procedure

**Mode A — First-time onboarding** (the `CLAUDE.md` Status block still has `<placeholders>`, or `_intake/` has new planning docs):
1. Read everything in [`_intake/`](../../../_intake/) — the brief, architecture notes, roadmap sketch, domain notes.
2. Fill [`CLAUDE.md`](../../../CLAUDE.md): the project name, one-liner, and the **Status** block. Remove the "new project" blockquote.
3. Draft [`docs/ARCHITECTURE.md`](../../../docs/ARCHITECTURE.md) (shape, invariants, the initial `D-NN` decision log) and [`docs/ROADMAP.md`](../../../docs/ROADMAP.md) (milestones `M0..`, slices as stepping stones toward the ambitious end-state). Surface unresolved forks as `decision` items with a recommended default.
4. Propose the **textbook/RAG library outline** per [`textbooks/LIBRARY_SEED.md`](../../../textbooks/LIBRARY_SEED.md) §1 and get explicit approval. Hand off to [`build_library`](../build_library/SKILL.md).
5. Run [`configure_project`](../configure_project/SKILL.md) to fill [`PROJECT_CONVENTIONS.md`](../../../PROJECT_CONVENTIONS.md) once code/tooling exists.
6. **When the repo goes live** (`gh repo create <name> --private --source . --push`):
   - Create **every** label listed in `PROJECT_CONVENTIONS.md` › Tracker & Hygiene (one `gh label create <name> -d "<desc>" || true` each — idempotent; don't enumerate from memory or trust GitHub's default labels to cover the set).
   - Protect `main` — require PRs + green checks **and enable "include administrators"** (otherwise `gh pr merge --admin` silently bypasses every gate). This is an **attended** step: use the web UI or `gh api` (deliberately not pre-approved). **Caveat:** on a free-plan **private** repo, GitHub does not enforce branch protection/rulesets — the options are GitHub Pro, an org plan, or a public repo. Until one of those holds, the written policy + the allowlist's narrowed grants are the *only* guard against force-push/main-push — say so in Status, and revisit the moment the repo goes public or Pro.
   - **Migrate any `PROJECT_BACKLOG.md` items to issues and delete that file** — once the tracker exists, a second backlog is a staleness machine.
   - File the standing day-one followup: replace `textbooks/AGENT_GUIDE.md` §1.5's schematic trace with a real one after the first slice ships.

**Mode B — Resume an in-flight project** (the default day-to-day):
1. **Preflight (cheap, mechanical):** `gh auth status` works; `git status` clean; **main CI is green** (`gh run list --branch main -L 1`). Edge cases, each with a safe default — never improvise here:
   - **Unexplained dirt** (not explained by Status — e.g. the last session died mid-slice): don't stash, don't discard. Commit it verbatim to a `rescue/<date>` branch, push, file a `followup` issue pointing at it, return to main, proceed.
   - **Red main** is the first slice — never build on red. Cause beyond your reach (CI infra, billing, secrets)? File `bug` + `blocked`, note it in Status, park CI-dependent work; CI-independent work may continue.
   - **Placeholder green is red:** if `scripts/preflight.*` / `ci.yml` still carry TODO-placeholder stages while real code exists, run `configure_project` to fill them before trusting any green.
   - **`gh` dead** (auth/network, after one retry)? Stop and report — don't run an autopilot loop on a dead tracker.
2. **Read the anchors only:** the `CLAUDE.md` Status block; the **current milestone section** of [`docs/ROADMAP.md`](../../../docs/ROADMAP.md); [`PROJECT_CONVENTIONS.md`](../../../PROJECT_CONVENTIONS.md). Don't re-read ARCHITECTURE or the library until the slice routes you there.
3. **Reconcile docs against reality** (truth order: git/CI > tracker > docs > chat): pull `gh issue list --state open`, `gh pr list`, and `git log --oneline -10`; if the Status block's claims or its **As-of** stamp disagree with the tracker / recent merges, **fix Status first**, then proceed. Sweep **new human comments** on open PRs/issues since the As-of stamp (`gh pr view <n> --comments`) — route each: act now / `track_followups` / a decision answer (step 4). Drain any `## Unfiled` section in `PROJECT_BACKLOG.md` into real issues. Docs are caches.
4. **Surface the decision queue — and read the answers.** `gh issue list --label decision` shows titles only; for each open one run `gh issue view <n> --comments`. A human comment **is the decision**: record it as `D-NN` (ARCHITECTURE Appendix A), reflect the ROADMAP, close the issue — and if it overrules a provisional default, file a re-route slice referencing every PR marked `Provisional on #<n>`. An objection window passed in **silence ratifies the default**: record the D-NN (note "ratified by silence") and close. Also reconcile `decision` issues *closed* since the As-of stamp against Appendix A — closed without a D-NN row is a miss; fix it now. Then present the compact digest — `D-NN (#issue) <fork> — recommended: <default> [provisional | blocked]` — the human may answer asynchronously; don't block on it.
5. **Pick up the Resume point** (branch · issue · next action · verify command) and run the [`textbooks/AGENT_GUIDE.md`](../../../textbooks/AGENT_GUIDE.md) build loop on the slice. Delegate broad exploration to read-only subagents; keep conclusions, not file dumps.
6. **At a fork**, follow `CLAUDE.md` §3: file the `decision` issue; proceed provisionally if reversible; park-and-switch to the next independent slice if not.

## Verification

- You can state in two sentences: the current milestone, the resume point, and the exact next action.
- Status agrees with the tracker (or was just fixed to); the decision digest was surfaced; **comments on open decisions were read, not just titles**.
- Build/test commands came from `PROJECT_CONVENTIONS.md`, not guessed; main was green before new work started.

## Don't

- Don't start coding before the preflight + reconcile — building on a red main or a stale Status multiplies waste.
- Don't stash or `checkout --` away unexplained working-tree changes — rescue-branch them; they may be the only copy of a dead session's slice.
- Don't re-read the whole ROADMAP / ARCHITECTURE / library "for context" — the anchors are enough; route narrowly when the slice needs it.
- Don't silently resolve a fork to keep momentum, and don't stall on one either — provisional-proceed or park-and-switch per `CLAUDE.md` §3.
- Don't treat a silent decision issue as forever-open — silence past its stated window ratifies the recommended default.
- Don't re-litigate decisions already in the `D-NN` log.
- Don't run Mode A again on an onboarded project — confirm the resume point and go.
