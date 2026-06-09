# CLAUDE.md — &lt;PROJECT_NAME&gt;

&lt;One sentence: what this project is and who it's for.&gt; Built and tested almost entirely by Claude Code, on autopilot, with the human deferring on architecture and ambition calls.

> **New, empty project?** This is the project template. Nothing has been onboarded yet. Drop the planning docs from Claude Chat into [`_intake/`](_intake/) and say **"let's onboard"** — that runs the [`onboard`](.claude/skills/onboard.md) skill, which reads the brief, fills the docs below, and proposes the textbook/RAG library outline. Then delete this blockquote.

## Status — *the onboarding & compaction anchor; keep it current*

> This block is the single source of truth for "where are we." `onboard` reads it first; `prepare_compaction` rewrites it last. Keep it to ~10 lines — detail lives in [`docs/ROADMAP.md`](docs/ROADMAP.md) and the issue tracker.

**Phase:** &lt;e.g. Phase 0 / pre-release&gt; · **Milestone:** &lt;M0 — name&gt; · **CI:** &lt;not set up yet&gt;
**Done:** &lt;nothing yet — freshly templated&gt;
**In progress:** &lt;the current slice + its issue/PR #&gt;
**Next:** &lt;the next 1–3 slices&gt;
**Open decisions awaiting the human:** &lt;none&gt; *(when present, list `D-NN` from [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) Appendix A)*
**Resume point:** &lt;the exact next action a returning session should take&gt;

## Read these first (in order)

1. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — the shape, the invariants, and the decision log (`D-01..`, Appendix A).
2. [docs/ROADMAP.md](docs/ROADMAP.md) — milestones `M0..`, each with goal / exit-criterion / status; the live plan.
3. [PROJECT_CONVENTIONS.md](PROJECT_CONVENTIONS.md) — paths, build/test/run commands, stack. **Every skill reads this.**
4. [textbooks/AGENT_GUIDE.md](textbooks/AGENT_GUIDE.md) — the build loop for turning the library into shipped work.

## The reference library — use it

[`textbooks/`](textbooks/) is this project's RAG knowledge library (built per-domain; see [textbooks/LIBRARY_SEED.md](textbooks/LIBRARY_SEED.md)). When planning or implementing:

- Route topics via [`textbooks/MANIFEST.json`](textbooks/MANIFEST.json) (`topic_to_books`, `rag_hints`); follow the loop in [`textbooks/AGENT_GUIDE.md`](textbooks/AGENT_GUIDE.md).
- **Verify every `Book NN §X` citation against [`textbooks/SECTIONS.json`](textbooks/SECTIONS.json) before asserting it** — grep it, don't load it whole. The library is audited; don't invent sections.
- Pre-mortem with `textbooks/reference/ANTI_PATTERNS.md` + `SYMPTOMS.md`; resolve architectural forks with `DECISION_TREES.md`.

## How we work — the daily loop

This project runs on autopilot. Day-to-day, the human's input is mostly three moves. Recognize them and respond with the matching skill:

### 1. "Welcome back, let's onboard and continue" → resume work
Run [`onboard`](.claude/skills/onboard.md):
1. Read the **Status** block above, then [`docs/ROADMAP.md`](docs/ROADMAP.md) (current milestone + next slices) and the open issues (`gh issue list` — the live backlog).
2. Re-read [`PROJECT_CONVENTIONS.md`](PROJECT_CONVENTIONS.md) for build/test commands.
3. Pick up the **Resume point**. Run the [`textbooks/AGENT_GUIDE.md`](textbooks/AGENT_GUIDE.md) build loop on the next slice: classify → route → pre-mortem → decide → implement → verify → record.
4. When a fork needs the human, surface it as a decision (see §3) rather than guessing.

### 2. "Let's prepare for compaction" → checkpoint before context runs out
Run [`prepare_compaction`](.claude/skills/prepare_compaction.md):
1. Rewrite the **Status** block above to reflect reality (done / in-progress / next / open decisions / a precise resume point).
2. Update [`docs/ROADMAP.md`](docs/ROADMAP.md) milestone status and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) if a decision was made.
3. Run [`track_followups`](.claude/skills/track_followups.md): file every deferred item as a GitHub issue (nothing actionable lives only in chat).
4. Commit and push merged work; leave the tree clean. The next session should be able to onboard from the docs alone.

### 3. A decision is needed → surface a fork, don't guess
Architecture and scope are ~1× leverage (the human's judgment, not the agent's). When a real fork appears:
- Present it as a **question with 2–4 concrete options**, each with its trade-off and the **`Book NN §X` (or `DECISION_TREES` Dn)** behind it.
- **Lead with a recommended default that leans to the most ambitious, most complete solution** (this project's standing preference) — but make the trade-off honest.
- Once chosen, record it in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) Appendix A as `D-NN` (decision + choice + grounding) and reflect it in the ROADMAP.

Other messages happen, but these three are the spine. Default to continuing the roadmap autonomously between them.

## Definition of done

Nothing is "done" until [`definition_of_done`](.claude/skills/definition_of_done.md) passes its gates with evidence: **build · tests · &lt;domain checks&gt; · anti-patterns avoided · determinism (where required) · performance (profiled, not guessed) · milestone exit-criterion · backlog updated.** Skills live in [`.claude/skills/`](.claude/skills/); orchestrate via `definition_of_done`.

## Working style

- **Lean ambitious and complete.** When choosing scope or approach, default to the fuller solution; surface the cheaper option as the trade-off, not the default.
- **Stay textbook-grounded.** Plan with [`plan_work`](.claude/skills/plan_work.md); cite verifiable sections; pre-mortem against `ANTI_PATTERNS`/`SYMPTOMS`.
- **Defer real forks to the human** (§3) with a recommended default + citation. Don't re-litigate settled decisions in the log.
- **Run on autopilot between checkpoints.** Ticket, branch, implement, verify, PR, merge. Keep the issue tracker as the live backlog and the docs as the durable memory.
- **Keep the library honest.** If you extend `textbooks/`, regenerate `SECTIONS.json` and run the audits (see [AGENT_GUIDE](textbooks/AGENT_GUIDE.md) §maintenance).
