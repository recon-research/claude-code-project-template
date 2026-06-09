# Skills — &lt;PROJECT_NAME&gt;

Drop-in procedures Claude Code follows when invoked (or when a request matches a skill's `description`). These are **domain-agnostic**: they read project specifics (paths, build/test commands, stack) from [`PROJECT_CONVENTIONS.md`](../../PROJECT_CONVENTIONS.md), so the same skills work on any project. Domain-specific execution skills (the recurring "add a `<thing>`" ops) are **derived during onboarding** and added here.

## The session loop

| Skill | When |
|-------|------|
| [onboard.md](onboard.md) | "welcome back" / "let's onboard and continue" — start or resume a session. |
| [prepare_compaction.md](prepare_compaction.md) | "let's prepare for compaction" — checkpoint to the docs + tracker before context is lost. |
| [build_library.md](build_library.md) | "build the library" / "write the textbooks" — author/extend `textbooks/`. |

## Setup, planning & review

| Skill | When |
|-------|------|
| [configure_project.md](configure_project.md) | Inspect the repo → fill `PROJECT_CONVENTIONS.md`. |
| [plan_work.md](plan_work.md) | "plan" / "design" / "what approach" — library-grounded plan; the planning front-end. |
| [review_against_library.md](review_against_library.md) | "audit this design vs the library" — cited Must-fix/Consider; `--fix` applies mechanical fixes. |
| [adversarial_review.md](adversarial_review.md) | Before merge on a substantial change — N independent reviewers prompted to falsify claims. |

## Verification

| Skill | When |
|-------|------|
| [definition_of_done.md](definition_of_done.md) | "is this done" — orchestrates the full gate with evidence. |
| [build_and_test.md](build_and_test.md) | "build" / "run tests" — full build + test cycle. |
| [add_test.md](add_test.md) | "add a test" — unit / integration / property / golden. |
| [snapshot_restore_test.md](snapshot_restore_test.md) | State round-trip for any subsystem that owns state. |
| [validate_headless_mode.md](validate_headless_mode.md) | CI gate: runs with no window / device / human. |
| [profile_subsystem.md](profile_subsystem.md) | "profile" / "find slow" — capture + analyze with the project's profiler. |
| [optimize_loop.md](optimize_loop.md) | "optimize" — profile-driven optimization of a hot path. |

## Build & instrument

| Skill | When |
|-------|------|
| [generate_content.md](generate_content.md) | "generate with an LLM" — agentic content-gen pipeline with validation. |
| [add_agent_tool.md](add_agent_tool.md) | "add an MCP / agent tool" — typed, validated, permission-filtered. |
| [add_telemetry_event.md](add_telemetry_event.md) | "add telemetry" — event with schema + sampling. |

## Discipline

| Skill | When |
|-------|------|
| [track_followups.md](track_followups.md) | Sweep deferred work into the tracker (run inside `prepare_compaction`). |

---

## Config files (NOT skills — they live at the project root)

- [`PROJECT_CONVENTIONS.md`](../../PROJECT_CONVENTIONS.md) — paths / commands / stack. **Every skill reads it first.** Fill it via `configure_project`.
- [`PROJECT_BACKLOG.md`](../../PROJECT_BACKLOG.md) — lightweight Now/Next/Blocked/Done continuity. Defers to GitHub Issues at scale.

## Authoring conventions

- **Frontmatter is required** — `name:` must equal the filename (no `.md`); `description:` carries the explicit triggers Claude reads to decide when to invoke. A skill without valid frontmatter silently fails to load.
- **Shape:** `# Title` → `## Procedure` (numbered, actionable) → `## Verification` → `## Don't`.
- **Never hard-code** project paths/commands/the example-system name — read them from `PROJECT_CONVENTIONS.md`.
- If a skill misfires (fires when it shouldn't, or is skipped when it should), tighten its `description`.
