# Project Template — Claude-Code-on-Autopilot

A reusable starting point for any new project built primarily by Claude Code. It bundles four things that work together:

1. **A vendored RAG knowledge library** (`textbooks/`) — you grow an exhaustive, self-validating "textbook series" for the project's domain, with machine indexes (`MANIFEST.json` / `SECTIONS.json`) so the agent can route to and cite exact sections.
2. **A frontier research pipeline** (`research/`) — bleeding-edge topics surveyed online into sourced+tiered notes (real fetched paper links, never recalled citations), tested via pre-registered experiments with plottable results, and published as paper-style report artifacts — all audited and CI-gated.
3. **A reusable, domain-agnostic skill set** (`.claude/skills/`) — planning, review, verification, build/test, research, onboarding, and compaction procedures that read project specifics from `PROJECT_CONVENTIONS.md` (so the same skills work on any project).
4. **An autopilot project harness** (`CLAUDE.md`, `docs/`, `.github/`) — a Status/onboard/compaction loop, a decision log, milestone roadmap, and CI gates, so Claude Code can ticket → implement → verify → PR → merge with the human only making decisions.

It's the generalized, blank-slate version of a proven setup: a domain "textbook" library plus a real codebase that consumes it and runs itself.

## The lifecycle this template supports

```
0. Discuss with Claude Chat → download planning docs (brief, architecture, roadmap, domain notes)
1. Copy this template into a new folder → drop those docs in _intake/ → say "let's onboard"
2. Claude Code writes the domain textbooks in textbooks/ (RAG setup), iterating until well-covered
3. Skills + conventions get tuned for the domain (configure_project, derive domain skills)
4. Create a private GitHub repo → push → run on autopilot (ticket / merge / verify), deferring decisions
   ↳ daily: "welcome back, onboard and continue" · "prepare for compaction" · pick a decision
```

## Starting a new project

1. **Copy the folder.** Copy this entire `project_template/` to your new project location and rename it.
2. **Drop your planning docs** from Claude Chat into [`_intake/`](_intake/) (see its README for what to include).
3. **Onboard.** Open Claude Code in the folder and say *"let's onboard"* (runs [`onboard`](.claude/skills/onboard.md)). It reads the brief, fills in [`CLAUDE.md`](CLAUDE.md) Status + [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) + [`docs/ROADMAP.md`](docs/ROADMAP.md), and proposes the textbook outline.
4. **Build the library.** Say *"let's build the library"* (runs [`build_library`](.claude/skills/build_library.md), which drives [`textbooks/LIBRARY_SEED.md`](textbooks/LIBRARY_SEED.md)). Iterate on coverage until the audits are green.
5. **Configure.** Run [`configure_project`](.claude/skills/configure_project.md) to fill [`PROJECT_CONVENTIONS.md`](PROJECT_CONVENTIONS.md) with real paths/commands/stack.
6. **Go on autopilot.** `git init`, create the private repo, and start the daily loop in [`CLAUDE.md`](CLAUDE.md) § *How we work*.

## Directory map

| Path | What it is |
|------|------------|
| [`CLAUDE.md`](CLAUDE.md) | Master onboarding + the daily loop + the Status anchor. **The agent reads this first.** |
| [`_intake/`](_intake/) | Drop-zone for the Claude Chat planning docs; onboarding reads it, then it's archived. |
| [`docs/`](docs/) | The operating manual: `ARCHITECTURE.md` (shape + invariants + decision log), `ROADMAP.md` (milestones). |
| [`PROJECT_CONVENTIONS.md`](PROJECT_CONVENTIONS.md) | Per-project paths / commands / stack. Every skill reads it. |
| [`PROJECT_BACKLOG.md`](PROJECT_BACKLOG.md) | **Pre-repo continuity only** — migrated to issues and deleted once the GitHub repo exists. |
| [`textbooks/`](textbooks/) | The vendored RAG library: `LIBRARY_SEED.md` (how to build it), `MANIFEST`/`SECTIONS`/`ROUTING_EVAL` (machine indexes), `books/` `reference/` `vision/` `tools/`. |
| [`research/`](research/) | The frontier layer: sourced+tiered survey notes, pre-registered experiments (`EXP-NN`), paper-style reports (`RR-NN`), and its own audit. Settled findings graduate into `textbooks/`. |
| [`.claude/skills/`](.claude/skills/) | The reusable skill set (see [its README](.claude/skills/README.md)). |
| [`.github/`](.github/) | CI gates (build / test / lint / **library audits** / **TODO hygiene**) + issue templates (`slice` / `decision` / `followup`) and the PR template that keep the tracker uniform and cold-readable. |

## The two layers, and why they're separate

- **The library (`textbooks/`) is domain knowledge** — rebuilt per project. It is *not* code; it's the exhaustive reference the agent consults and cites.
- **The skills are domain-agnostic procedures** — reused as-is. They never hard-code paths; they read `PROJECT_CONVENTIONS.md`.

This separation is the whole trick: the human writes the architecture and the domain knowledge once, and the agent executes against it with high fidelity, citing its sources and verifying its work.

## Maintaining this template itself

Improvements you make on a real project (a sharper skill, a better doc template, a new universal skill) are worth back-porting here. Keep the domain-specific bits out — anything that names a real stack or domain belongs in a project, not the template.
