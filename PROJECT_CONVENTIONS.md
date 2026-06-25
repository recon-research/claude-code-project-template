# PROJECT_CONVENTIONS.md — Project-Specific Settings For The Skills

The drop-in skills describe *what* to do; the project-specific *where* and *how* live here. **Every skill reads this file first** for paths, commands, and stack, so the same skills work on any project without editing each one. Fill it in once per project — or run the [`configure_project`](.claude/skills/configure_project/SKILL.md) skill to auto-detect it.

> This is a **config file, not a skill** — it lives at the project root. Replace every `<…>` below during onboarding. If a skill needs a path or command not listed here, **add it here** rather than hard-coding it in the skill.

## Identity
- **Project name**: &lt;PROJECT_NAME&gt;
- **Example-system name** (the library's canonical example): &lt;EXAMPLE_SYSTEM&gt;
- **Primary language(s)**: &lt;fill in&gt;

## Build & Test
- **Preflight (every merge-blocking gate, locally, in CI order)**: `scripts/preflight.sh` / `scripts\preflight.ps1` — run before **every** push; a clean preflight means CI should be green. The scripts mirror `.github/workflows/ci.yml` by construction (change one → change the other); `configure_project` fills their TODO stages from the commands below. The CI posture (Operating posture below) paces *when CI re-runs* these gates — preflight always runs **all** of them locally, in every posture. Flags: `--quick`/`-Quick` (static gates only) · `--skip-smoke`/`-SkipSmoke`.
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

## Operating posture (set by the onboard setup interview)
The four knobs the [`onboard`](.claude/skills/onboard/SKILL.md) Mode A interview sets — recommended default first, the owner's answer recorded here. **Skills read these lines as config**; changing one later is a normal PR.
- **Repo visibility & plan**: &lt;public · private-Free · private-Pro · org&gt; — public repos get Actions minutes free **and** enforceable branch protection on any plan; free-plan private repos get 2,000 min/month and **unenforced** protection (`docs/AUTOMATION.md` §6).
- **CI posture**: &lt;light (default) · full · manual&gt; — `CI_POSTURE` (unset = light): *how much* CI runs — `light` = `static gates` only per PR, `full` = + the heavy build/test/lint matrix, `manual` = nothing automatic. Escalate any posture: `full-ci` label · `gh workflow run ci.yml` · `M*`/`v*` tag. **Preflight runs every gate locally in all postures.** Mechanics + trade-offs: [`docs/AUTOMATION.md`](docs/AUTOMATION.md) §6.
- **CI gating**: &lt;blocking (default) · advisory&gt; — `CI_GATING` (unset = blocking): *when* the heavy matrix runs under `full` — `blocking` on the PR (must be green to merge), `advisory` post-merge on main (PR merges on `static gates` + preflight; a red post-merge is fixed forward by the next `onboard`). Advisory ⇒ require only `static gates` in branch protection. §6.
- **CI path modularity** (always on, no config): doc-only changes (`*.md` / `docs/` / `_intake/`) skip the heavy matrix in any posture; `static gates` still runs. §6.
- **Review cadence**: &lt;milestone exits + risky slices (default) · every slice · on request&gt; — when `adversarial_review` **must** run; `definition_of_done` blocks a milestone exit without linked review findings. "Risky" = touches an ARCHITECTURE invariant, a data schema/migration, a security surface, or a public API.
- **Objection window**: &lt;48h (default) · 24h · 1 week&gt; — how long a reversible `decision` issue waits before silence ratifies the recommended default (`CLAUDE.md` §3); each issue may state its own window, defaulting to this.

## Tracker & Hygiene
- **Issue tracker**: &lt;e.g. GitHub Issues on `<org>/<repo>`&gt; — the live backlog; **defer = file now** (`track_followups`).
- **Labels**: `slice` (a unit of roadmap work) · `epic` (a far milestone's container issue) · `decision` (fork awaiting the human) · `followup` (deferred work) · `idea` · `debt` · `bug` · `blocked` · `research` (frontier question to survey) · `full-ci` (PR-only: escalate this PR to the heavy CI matrix — read by `ci.yml`, any posture). Created once at repo setup (`onboard` Mode A); the issue templates apply them.
- **Horizon rule (ticket granularity)**: the **near** milestone gets fine slice tickets; **far** milestones get **one `epic` issue** holding a slice checklist. At milestone start, run `plan_milestone_tickets` to refine the epic into slices — in plan mode, with the human; slicing is an architectural act. Fine tickets written months ahead are churn, not planning.
- **Branch naming**: `slice/<issue#>-<slug>` · **PR title**: `M<n> <slice>: <imperative summary> (closes #<issue>)`.
- **TODO convention**: a TODO entering code must reference a filed ticket — `TODO(#NN): …`. Naked `TODO`/`FIXME` fails `definition_of_done` and the CI hygiene gate (a `static gates` step).
- **Merge policy**: &lt;squash / merge-commit — pick one&gt;; PRs require the **posture's merge gate** (Operating posture above): *light* / *full-blocking* — required checks green (posture-skipped and doc-only-skipped jobs report "skipped", which satisfies required checks); *full-advisory* — `static gates` green + a clean preflight, heavy matrix verified **post-merge** on main (red → file a `bug`, fix forward); *manual* — a clean `scripts/preflight.*` run with its output pasted in the PR. `main` is never pushed directly.
- **Right-sized slices** (a slice is *coherent*, not merely *small*): a PR is the smallest change that stands alone and is independently verifiable — but **don't over-fragment**. Bundle tightly-coupled edits and the doc/ROADMAP updates they imply into one PR; splitting a single coherent change into a string of trivial PRs multiplies CI + review overhead for no isolation gain. (Doc-only and checkpoint commits are cheap by design now — path modularity skips their heavy CI — so ride them along with the change that motivates them rather than spinning a PR per line.) **Checkpoint path** (doc-only commits with no slice PR to ride — compaction Status rewrites, D-NN recordings): a short-lived `checkpoint/<date>` branch + PR, merged on green (`gh pr merge --auto` is pre-approved; doc-only CI is fast). **Forbidden regardless of what the permission grammar allows:** `git push --force` (a broken branch gets a new branch), `gh pr merge --admin` (bypasses the required checks — protection must "include administrators"), and `--repo <other>` overrides on any gh write. A PR that won't merge after green CI: merge main *into* the branch, re-run preflight, wait for green — never force over it.
- **PR / commit mechanics**: create PRs with `gh pr create --body-file <tempfile>` (UTF-8) — **never inline `--body`** (Windows PowerShell 5.1 splits the body at embedded double quotes; body-file is portable everywhere). Multiline commit messages likewise go through a file or stdin: `git commit -F -` with a here-doc (PowerShell here-string quoting mangles git args).
- **Decision flow**: fork → `decision` issue (template) → human picks (async, by commenting — `onboard` reads the comments) → recorded as `D-NN` in `docs/ARCHITECTURE.md` Appendix A → issue closed. Reversible forks may proceed provisionally per `CLAUDE.md` §3; silence past the stated objection window ratifies the default. **D-NN allocation**: next = max(Appendix A, open `decision` issue titles) + 1 — check both; two sessions can race.
- **Untrusted contributor code** (public repos): before running *any* repo script from a contributor branch — including the pre-approved `tools/_audit_*.py` audits — diff `tools/` and `scripts/` against main. Pre-approved commands + a malicious PR = arbitrary code execution.

## Validation machines (optional — delete if every gate runs on one machine + CI)
- **Tiers**: name each machine/environment that validates what CI can't (hardware, OS, GPU/device variants) — e.g. `Tier P` (primary dev box — also the floor: what works here must keep working) · `Tier R` (alt-vendor/secondary box) · `Tier N` (a collaborator's hardware, asks **batched**). State each tier's role; record which gates are CI-blind and which tier covers them.
- **Provenance rule**: a validation claim from a machine the merging session cannot drive must **link its evidence** — the issue comment with the pasted run output — never a bare assertion. The PR says which tier validated what ("validated on Tier P; skips in CI").
- **Golden/oracle policy**: goldens that encode machine-independent behavior are **never regenerated to make a new machine pass** — a cross-tier mismatch is a finding to investigate, not a calibration step. Environment-specific oracles (e.g. pixel output) compare like-for-like only.

## Shell gotchas (optional — keep if any contributor/agent runs Windows PowerShell 5.1; else delete)
- No `&&` / `||` pipeline chains (parser error) — sequence with `;` or `if ($?) { … }`.
- Don't pipe native commands (git, build tools) through `2>&1` — PS 5.1 wraps each stderr line in an ErrorRecord and poisons `$?` even on exit 0.
- `gh pr create` / `gh issue create`: always `--body-file` (see PR / commit mechanics above).
- Property access does **not** expand inside a larger argument token: `-f title=$m.t` passes the literal text `<typename>.t` — wrap member access in a subexpression: `-f "title=$($m.t)"`.
- Keep `.ps1` output strings ASCII — PS 5.1 reads un-BOM'd scripts as ANSI (non-ASCII becomes mojibake).
