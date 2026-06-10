# PROJECT_CONVENTIONS.md — Project-Specific Settings For The Skills

The drop-in skills describe *what* to do; the project-specific *where* and *how* live here. **Every skill reads this file first** for paths, commands, and stack, so the same skills work on any project without editing each one. Fill it in once per project — or run the [`configure_project`](.claude/skills/configure_project.md) skill to auto-detect it.

> This is a **config file, not a skill** — it lives at the project root. Replace every `<…>` below during onboarding. If a skill needs a path or command not listed here, **add it here** rather than hard-coding it in the skill.

## Identity
- **Project name**: &lt;PROJECT_NAME&gt;
- **Example-system name** (the library's canonical example): &lt;EXAMPLE_SYSTEM&gt;
- **Primary language(s)**: &lt;fill in&gt;

## Build & Test
- **Build**: `<build command>`
- **Profiling build**: `<how to build with the profiler enabled>`
- **Run**: `<run command, incl. any headless / no-window flag>`
- **Test**: `<test command>` (unit + integration)
- **Format / lint**: `<formatter + linter, with warnings-as-errors if used>`

## Source Layout
- **Main source**: `<where the code lives, e.g. src/ or crates/>`
- **The project's main unit types**: `<where the recurring "things" live — the analogue of components/passes/modules — so add_* skills know where to put them>`
- **Tests**: `<where tests live>`
- **Experiment harness**: `<where research-experiment code lives — read by run_experiment>`
- **Design docs**: `docs/` · **Reference library**: `textbooks/` · **Frontier layer**: `research/`

## Stack
- **Core frameworks / libraries**: &lt;fill in&gt;
- **Data / serialization**: &lt;fill in&gt;
- **Profiler**: &lt;fill in — read by `profile_subsystem` / `optimize_loop`&gt;
- **Other key tools**: &lt;fill in&gt;

## Conventions
- **Naming**: &lt;type / file / local naming conventions&gt;
- **Determinism / reproducibility**: &lt;if the project has a deterministic core, describe the boundary; else "n/a"&gt;
- **Domain conventions**: &lt;units, coordinate systems, formats, invariants worth stating once&gt;

## Agent / Tooling
- **MCP server name(s)**: &lt;the MCP servers the agent/project exposes, if any — read by `add_agent_tool`&gt;
- **CI + gate command**: &lt;the CI system and the merge-gating command — read by `definition_of_done` / `validate_headless_mode`&gt;

## Tracker & Hygiene
- **Issue tracker**: &lt;e.g. GitHub Issues on `<org>/<repo>`&gt; — the live backlog; **defer = file now** (`track_followups`).
- **Labels**: `slice` (a unit of roadmap work) · `decision` (fork awaiting the human) · `followup` (deferred work) · `idea` · `debt` · `bug` · `blocked` · `research` (frontier question to survey). Created once at repo setup (`onboard` Mode A); the issue templates apply them.
- **Branch naming**: `slice/<issue#>-<slug>` · **PR title**: `M<n> <slice>: <imperative summary> (closes #<issue>)`.
- **TODO convention**: a TODO entering code must reference a filed ticket — `TODO(#NN): …`. Naked `TODO`/`FIXME` fails `definition_of_done` and the CI hygiene job.
- **Merge policy**: &lt;squash / merge-commit — pick one&gt;; PRs require green CI; `main` is never pushed directly.
- **Decision flow**: fork → `decision` issue (template) → human picks (async) → recorded as `D-NN` in `docs/ARCHITECTURE.md` Appendix A → issue closed. Reversible forks may proceed provisionally per `CLAUDE.md` §3.
