# Project Template — Claude-Code-on-Autopilot

A reusable starting point for any new project built primarily by Claude Code. It bundles four things that work together:

1. **A vendored RAG knowledge library** (`textbooks/`) — you grow an exhaustive, self-validating "textbook series" for the project's domain, with machine indexes (`MANIFEST.json` / `SECTIONS.json`) so the agent can route to and cite exact sections.
2. **A frontier research pipeline** (`research/`) — bleeding-edge topics surveyed online into sourced+tiered notes (real fetched paper links, never recalled citations), tested via pre-registered experiments with plottable results, and published as paper-style report artifacts — all audited and CI-gated.
3. **A reusable, domain-agnostic skill set** (`.claude/skills/`, each skill a `<name>/SKILL.md` directory) — planning, review, verification, build/test, research, onboarding, and compaction procedures that read project specifics from `PROJECT_CONVENTIONS.md` (so the same skills work on any project) — plus tool-restricted subagents (`.claude/agents/`) for mechanically read-only reviews and cheap-model sweeps.
4. **An autopilot project harness** (`CLAUDE.md`, `docs/`, `.github/`, `.claude/settings.json` + hooks) — a Status/onboard/compaction loop, a decision protocol, milestone roadmap, CI gates that are real from day one **and minutes-aware** (a configurable CI posture — pacing, blocking-vs-advisory gating, and automatic doc-only skipping, `light` by default — keeps a private repo's Actions burn near zero), and a pre-approved permission loop, so Claude Code can ticket → implement → verify → PR → merge unattended, with the human only making decisions.

It's the generalized, blank-slate version of a proven setup: a domain "textbook" library plus a real codebase that consumes it and runs itself.

## The lifecycle this template supports

```
0. Discuss with Claude Chat → download planning docs (brief, architecture, roadmap, domain notes)
1. Copy this template into a new folder → drop those docs in _intake/ → give the kickoff line (step 3)
2. Claude Code writes the domain textbooks in textbooks/ (RAG setup), iterating until well-covered
3. Skills + conventions get tuned for the domain (configure_project, derive domain skills)
4. Create a private GitHub repo → push → run on autopilot (ticket / merge / verify), deferring decisions
   ↳ daily: "welcome back, onboard and continue" · "prepare for compaction" · pick a decision
```

**Prerequisites:** Claude Code (desktop app or CLI), `git`, the GitHub CLI authenticated (`gh auth login`), and Python 3 on PATH (the audits and hooks are stdlib-only Python). On Windows, Git for Windows provides the bash that `scripts/preflight.sh` uses — or use the native `scripts\preflight.ps1` twin; the hooks and audits are plain Python and need no bash.

## Starting a new project

1. **Copy the folder.** Copy this entire `project_template/` to your new project location and rename it.
2. **Drop your planning docs** from Claude Chat into [`_intake/`](_intake/) (see its README for what to include).
3. **Onboard — the kickoff line.** Open Claude Code in the folder and say: *"let's onboard — you have my permission to adjust the Claude Code settings and set everything up."* That one sentence is the only setup action that's yours. The trailing clause is the **kickoff authorization**: the shipped settings (the pre-approved autopilot allowlist + hooks) arrive with the copy, and the grant lets the agent finish the wiring (machine-local `settings.local.json`, any trims you ask for) and run the whole onboarding unattended — an agent can't, by platform design, widen its own permissions from file text alone, which is why the grant must be your words. [`onboard`](.claude/skills/onboard/SKILL.md) then reads the brief, **walks you through the four-question setup interview** — repo visibility, CI pacing, review cadence, decision objection window; recommended default first, trade-offs stated, answers recorded in [`PROJECT_CONVENTIONS.md`](PROJECT_CONVENTIONS.md) › Operating posture — stamps [`TEMPLATE_VERSION`](TEMPLATE_VERSION) (provenance for later template syncs), fills in [`CLAUDE.md`](CLAUDE.md) Status + [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) + [`docs/ROADMAP.md`](docs/ROADMAP.md), proposes the textbook outline, and finishes with a **feature self-test** (skills load, hooks fire, audits green) so the workflow layer is demonstrably live, not just present. Skip the grant and everything still works — you'll just approve prompts by hand.
4. **Build the library.** Say *"let's build the library"* (runs [`build_library`](.claude/skills/build_library/SKILL.md), which drives [`textbooks/LIBRARY_SEED.md`](textbooks/LIBRARY_SEED.md)). Iterate on coverage until the audits are green.
5. **Configure.** Run [`configure_project`](.claude/skills/configure_project/SKILL.md) to fill [`PROJECT_CONVENTIONS.md`](PROJECT_CONVENTIONS.md) with real paths/commands/stack.
6. **Go on autopilot.** `git init`, create the repo (onboard Mode A creates the labels, sets the `CI_POSTURE` variable from your interview answer, migrates the backlog, and walks the one attended step: branch protection with **"include administrators"** on). The permission allowlist and hooks ship pre-wired in [`.claude/settings.json`](.claude/settings.json). Then run the daily loop below.

## Operating it day-to-day

Your input converges to three messages and the occasional comment:

- **"Welcome back, let's onboard and continue"** — the agent preflights (auth / tree / CI, with written safe defaults for dirty trees, red mains, and dead `gh`), reconciles the docs against the tracker, **reads your answers on open `decision` issues**, and resumes the roadmap.
- **"Let's prepare for compaction"** — the checkpoint: Status rewritten and *verified* against the tracker, deferrals swept into tickets, tree clean and pushed.
- **Answering decisions.** The agent never guesses on hard-to-reverse forks: it files a `decision` issue with options and a recommended default, then proceeds provisionally (reversible) or parks the slice (irreversible). **A comment on the issue is the decision** — typed from anywhere, including the GitHub mobile app; the next onboard picks it up and re-routes any provisional work. Silence past the stated objection window ratifies the default, so an unanswered queue never stalls the run. *(Optional: wire the `@claude` Action — [docs/AUTOMATION.md](docs/AUTOMATION.md) §3 — and a comment gets implemented remotely, no desktop required.)*

Between those, the agent runs the loop alone: ticket → branch → implement → preflight → PR → merge gate green (per the CI posture) → merge → checkpoint. What keeps that honest is mechanical, not vibes: audits that exit non-zero gate every merge (citations + index freshness, routing, links, research source/tier/date discipline, skills structure, naked-TODO hygiene); `scripts/preflight.*` runs **all** gates locally in every posture; a PreToolUse hook blocks `git commit` if the staged diff adds an unticketed TODO; a SessionStart hook injects Status-staleness + the open decision queue for ~100 tokens; and force-push / admin-merge are denied and policy-forbidden. CI is **paced, not weakened**: `light` (the default) runs the ~1-minute consolidated `static gates` job per PR so a free-plan private repo doesn't burn its 2,000 monthly minutes; doc-only changes skip the heavy matrix automatically (no more 15-minute CI to edit the roadmap); and an optional **advisory** gating mode runs the matrix *post-merge* as a sanity check — merge on preflight, fix-forward the rare environment-specific red — instead of blocking each PR. Escalate any PR to the full matrix with the `full-ci` label, `gh workflow run ci.yml`, or a milestone tag ([docs/AUTOMATION.md](docs/AUTOMATION.md) §6). And the process **measures and corrects itself**: `scripts/metrics.py` refreshes a small ledger ([docs/METRICS.md](docs/METRICS.md) — escape rate, rework, preflight↔CI divergence, decision latency) at each checkpoint, and at milestone exits a [`retrospective`](.claude/skills/retrospective/SKILL.md) makes every escaped defect leave a *guard* behind it (a gate / anti-pattern / lens), not just a fix.

## Directory map

| Path | What it is |
|------|------------|
| [`CLAUDE.md`](CLAUDE.md) | Master onboarding + the daily loop + the Status anchor. **The agent reads this first.** |
| [`_intake/`](_intake/) | Drop-zone for the Claude Chat planning docs; onboarding reads it, then it's archived. |
| [`docs/`](docs/) | The operating manual: `ARCHITECTURE.md` (shape + invariants + decision log), `ROADMAP.md` (milestones), `METRICS.md` (the generated process-metrics ledger). |
| [`PROJECT_CONVENTIONS.md`](PROJECT_CONVENTIONS.md) | Per-project paths / commands / stack. Every skill reads it. |
| [`PROJECT_BACKLOG.md`](PROJECT_BACKLOG.md) | **Pre-repo continuity only** — migrated to issues and deleted once the GitHub repo exists. |
| [`TEMPLATE_VERSION`](TEMPLATE_VERSION) | Provenance stamp (template source + sha + dates) — written at onboard, read and re-stamped by `update_from_template`. |
| [`textbooks/`](textbooks/) | The vendored RAG library: `LIBRARY_SEED.md` (how to build it), `MANIFEST`/`SECTIONS`/`ROUTING_EVAL` (machine indexes), `books/` `reference/` `vision/` `tools/`. |
| [`research/`](research/) | The frontier layer: sourced+tiered survey notes, pre-registered experiments (`EXP-NN`), paper-style reports (`RR-NN`), and its own audit. Settled findings graduate into `textbooks/`. |
| [`.claude/skills/`](.claude/skills/) | The reusable skill set — each skill a `<name>/SKILL.md` directory (see [its README](.claude/skills/README.md)). |
| [`.claude/agents/`](.claude/agents/) | Tool-restricted subagents: `adversarial-reviewer` (Read/Grep/Glob — mechanically read-only) and `mech-sweeper` (cheap-model sweeps). |
| [`.claude/hooks/`](.claude/hooks/) | Zero-token mechanical gates (naked-TODO commit block, session staleness banner) — wired in `settings.json`, fail-open by design. |
| [`docs/AUTOMATION.md`](docs/AUTOMATION.md) | The operator console: the hooks/settings posture, `@claude` GitHub Action, scheduled runs, headless CI, **CI minutes & the posture system** (incl. the self-hosted-runner option) — the parts that need the human once. |
| [`scripts/`](scripts/) | `preflight.{sh,ps1}` — every merge-blocking gate locally, in CI order (mirrors the CI workflow; `configure_project` fills the TODO stages; the audit/hygiene stages are real from day one). Run before every push. `metrics.py` — the `gh`-sourced process-metrics ledger (writes `docs/METRICS.md`), refreshed at each checkpoint. |
| [`.github/`](.github/) | CI gates, minutes-aware: the consolidated **`static gates` job** (library + research audits / skills structure / TODO hygiene) runs per the **CI posture** (`light` default); build / test / lint escalate on demand (blocking on PRs, or post-merge under advisory gating), and a `classify changes` job skips them for doc-only edits. Plus issue templates (`slice` / `decision` / `followup` / `research`) and the PR template that keep the tracker uniform and cold-readable. |

## Machinery vs content — the update boundary

Downstream projects fill some template files in and take others verbatim. The split is what makes template updates mechanical instead of hand archaeology ([`update_from_template`](.claude/skills/update_from_template/SKILL.md) applies it):

| Kind | Paths | Update rule |
|------|-------|-------------|
| **Machinery** | `.claude/skills/` · `.claude/hooks/` · `.claude/agents/` · `textbooks/tools/` · `research/tools/` · `scripts/` · `.github/` · `textbooks/LIBRARY_SEED.md` · `textbooks/books/00_TEMPLATE.md` · `research/*/00_TEMPLATE.md` | Take upstream **wholesale** on every sync, then re-apply the project's own pieces on top (derived skills re-registered in the MANIFEST catalog, filled preflight/CI stage bodies). |
| **Content** | `CLAUDE.md` · `PROJECT_CONVENTIONS.md` · `docs/` · `textbooks/` books + the filled `CLAUDE`/`README`/`AGENT_GUIDE`/`MANIFEST` · `research/` notes/experiments/reports | Filled once per project, **never overwritten** — structural improvements are ported by hand from the upstream diff, respecting the project's documented deviations. |
| **Settings** | `.claude/settings.json` | Ships with the copy (adopted via the kickoff authorization). Syncs may update hooks/deny rules; an agent never *widens* the allowlist without the owner's fresh, explicit instruction. |

## The documentation surface — the single-home rule

Many small instruction docs, deliberately. The discipline that keeps "many" from becoming "scattered and contradictory": **each fact lives in exactly one layer; every other mention is a one-line cross-link, never a copy** (a fact written twice drifts). When you add guidance, drop it in its layer and link from the rest:

| Layer — the canonical home | Owns | Loaded into the agent |
|---|---|---|
| [`CLAUDE.md`](CLAUDE.md) | **policy** — the autopilot loop, the daily moves, working style, truth hierarchy | **every session** (so keep it lean) |
| [`PROJECT_CONVENTIONS.md`](PROJECT_CONVENTIONS.md) | **project mechanics + config** — paths, commands, stack, operating posture, tracker/merge rules | when a skill runs (every skill reads it first) |
| [`.claude/skills/<name>/SKILL.md`](.claude/skills/) | **procedure** — how to perform one task | lazy — only each skill's `description:` is always resident, for routing |
| [`docs/`](docs/) | **operating reference** — `ARCHITECTURE`, `ROADMAP`, `AUTOMATION`, `METRICS` | lazy, when a task routes there |
| [`textbooks/CLAUDE.md`](textbooks/CLAUDE.md) · [`research/CLAUDE.md`](research/CLAUDE.md) (+ [`AGENT_GUIDE.md`](textbooks/AGENT_GUIDE.md) / [`research/README.md`](research/README.md) for the full reference) | **library / frontier discipline** — the citation/tier rules + how to consult each knowledge layer | the `CLAUDE.md` is **directory-scoped** (auto-loads while working in that folder); the guides are lazy |
| `README.md` (this file) · each folder's `README.md` | **human overview** — for someone browsing the repo | **not loaded** — humans only |

*(`.claude/rules/` path-scoping was evaluated as an alternative for the per-subtree discipline — it's GA, but for a whole subtree it's functionally equivalent to a directory-scoped `CLAUDE.md` on both token cost and post-compaction reload, so the `CLAUDE.md` stays the single mechanism rather than adding a second one — #4.)*

**Two boundaries here are load-bearing — don't "streamline" them away:**

- **Lazy-loading *is* the token economy.** Only `CLAUDE.md` rides every session; directory-scoped `CLAUDE.md`s, skill bodies, and `docs/` load on demand. Merging a lazy doc *into* `CLAUDE.md` (or folding the human `README`s into it) would tax every session with text it rarely needs — the opposite of streamlining. The split is the optimization; keep it.
- **Pinned paths** the loader or skills depend on, which therefore cannot move or merge: root `CLAUDE.md`; each directory's `CLAUDE.md`; `PROJECT_CONVENTIONS.md` (every skill hard-reads this path); `.claude/skills/<name>/SKILL.md` (Agent-Skills load *only* from `<name>/SKILL.md` directories); `.claude/skills/README.md` (the catalog the routing audit checks). Everything else is movable, but is already single-homed — one doc per audience/layer, not duplication.

## Updating a downstream project

The copy is stamped at onboard (`TEMPLATE_VERSION`: source + sha + date). Later, say **"update from the template"** — [`update_from_template`](.claude/skills/update_from_template/SKILL.md) diffs upstream from the stamped sha, applies machinery wholesale, ports content improvements by diff, re-runs every gate, and re-stamps. Improvements flow the other way too (see *Maintaining this template* below).

## The two layers, and why they're separate

- **The library (`textbooks/`) is domain knowledge** — rebuilt per project. It is *not* code; it's the exhaustive reference the agent consults and cites.
- **The skills are domain-agnostic procedures** — reused as-is. They never hard-code paths; they read `PROJECT_CONVENTIONS.md`.

This separation is the whole trick: the human writes the architecture and the domain knowledge once, and the agent executes against it with high fidelity, citing its sources and verifying its work.

## Maintaining this template itself

Improvements you make on a real project (a sharper skill, a better doc template, a new universal skill) are worth back-porting here. Keep the domain-specific bits out — anything that names a real stack or domain belongs in a project, not the template. Machinery changes should be exercised on **both shells** (bash and Windows PowerShell 5.1) before merging — the template's audience includes both, and most field bugs have been shell-specific.
