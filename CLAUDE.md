# CLAUDE.md — &lt;PROJECT_NAME&gt;

&lt;One sentence: what this project is and who it's for.&gt; Built and tested almost entirely by Claude Code, on autopilot, with the human deferring on architecture and ambition calls.

> **New, empty project?** This is the project template. Nothing has been onboarded yet. Drop the planning docs from Claude Chat into [`_intake/`](_intake/) and say **"let's onboard"** — that runs the [`onboard`](.claude/skills/onboard.md) skill, which reads the brief, fills the docs below, and proposes the textbook/RAG library outline. Then delete this blockquote.

## Status — *the onboarding & compaction anchor; keep it current*

> The 10-line summary of "where are we." Rewritten fully by `prepare_compaction`; **one-line-updated at every merge** (the merge-time checkpoint, so a surprise compaction loses nothing); verified against the tracker by `onboard`. Detail lives in [`docs/ROADMAP.md`](docs/ROADMAP.md) and the issue tracker — never here.

**As of:** &lt;date · main short-sha&gt; · **Phase:** &lt;e.g. Phase 0&gt; · **Milestone:** &lt;M0 — name&gt; · **CI:** &lt;main green?&gt;
**Done:** &lt;nothing yet — freshly templated&gt;
**In progress:** &lt;the current slice + its issue/PR #&gt;
**Next:** &lt;the next 1–3 slices, by issue #&gt;
**Decisions awaiting the human:** &lt;none&gt; *(mirror of `gh issue list --label decision`; list `D-NN`, mark any proceeding provisionally)*
**Resume:** &lt;branch&gt; · &lt;issue #&gt; · &lt;one imperative next action&gt; · verify with: &lt;command&gt;

## Read these first (in order)

1. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — the shape, the invariants, and the decision log (`D-01..`, Appendix A).
2. [docs/ROADMAP.md](docs/ROADMAP.md) — milestones `M0..`, each with goal / exit-criterion / status; the live plan.
3. [PROJECT_CONVENTIONS.md](PROJECT_CONVENTIONS.md) — paths, commands, stack, tracker conventions. **Every skill reads this.**
4. [textbooks/AGENT_GUIDE.md](textbooks/AGENT_GUIDE.md) — the build loop for turning the library into shipped work.

## Source of truth — docs are caches

Truth order: **git/CI &gt; issue tracker &gt; docs &gt; chat memory.** On any mismatch, fix the doc to match reality *before* working — cheap now, poisonous later. Ownership (who updates what, when):

| Artifact | When it's written |
|---|---|
| **Status block** (above) | one line at **every merge**; fully at `prepare_compaction` |
| **docs/ROADMAP.md** | the moment a slice/milestone changes state |
| **docs/ARCHITECTURE.md** | only when a `D-NN` decision lands |
| **Issue tracker** | continuously — **defer = file now**, never "I'll note it later" |

## The reference library — use it

[`textbooks/`](textbooks/) is this project's RAG knowledge library (built per-domain; see [textbooks/LIBRARY_SEED.md](textbooks/LIBRARY_SEED.md)). When planning or implementing:

- Route topics via [`textbooks/MANIFEST.json`](textbooks/MANIFEST.json) (`topic_to_books`, `rag_hints`); follow the loop in [`textbooks/AGENT_GUIDE.md`](textbooks/AGENT_GUIDE.md).
- **Verify every `Book NN §X` citation against [`textbooks/SECTIONS.json`](textbooks/SECTIONS.json) before asserting it** — grep it, don't load it whole. The library is audited; don't invent sections.
- Pre-mortem with `textbooks/reference/ANTI_PATTERNS.md` + `SYMPTOMS.md`; resolve architectural forks with `DECISION_TREES.md`.

## How we work — the daily loop

This project runs on autopilot. Day-to-day, the human's input is mostly three moves:

### 1. "Welcome back, let's onboard and continue" → run [`onboard`](.claude/skills/onboard.md)
Preflight (auth, clean tree, **main green**) → read Status + the current ROADMAP milestone → **reconcile docs against the tracker** (truth order above) → surface the decision queue (`gh issue list --label decision`) as a compact digest → pick up the **Resume** point and run the [build loop](textbooks/AGENT_GUIDE.md).

### 2. "Let's prepare for compaction" → run [`prepare_compaction`](.claude/skills/prepare_compaction.md)
Rewrite + stamp the Status block → **verify its claims against the tracker** (every Done has a merged PR; every In-progress an open issue) → update ROADMAP/ARCHITECTURE → sweep deferrals into tickets ([`track_followups`](.claude/skills/track_followups.md)) → clean tree, push. If merge-time checkpointing happened all along, this is verification, not archaeology.

### 3. A decision is needed → surface a fork; don't guess, don't stall
Architecture and scope are ~1× leverage (the human's judgment). When a real fork appears:
- **File it as an issue labeled `decision`** (template provided): 2–4 options, each with its trade-off and the `Book NN §X` / `DECISION_TREES Dn` behind it, **recommended default first** (per the policy below).
- **Reversible fork?** Proceed **provisionally** on the recommended default and keep working — note in the issue "proceeding provisionally; objection window until the next checkpoint." The human overrules asynchronously if they disagree.
- **Hard to reverse** (public API shape, data schema/migration, external commitments, money)? Don't guess: park the slice, pick the **next independent slice** from the tracker, and let the run stay productive.
- Once the human decides: record it as `D-NN` in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) Appendix A, reflect it in the ROADMAP, close the issue.

Other messages happen, but these three are the spine. Default to continuing the roadmap autonomously between them.

## Definition of done

Nothing is "done" until [`definition_of_done`](.claude/skills/definition_of_done.md) passes its gates **with evidence** (output, not assertion): **build · tests · &lt;domain checks&gt; · anti-patterns avoided · determinism (where required) · performance (profiled, not guessed) · milestone exit-criterion · backlog updated · no unticketed deferrals.** Skills live in [`.claude/skills/`](.claude/skills/).

## Working style — the policy the executing agent runs on

- **Ambitious destination, staged route.** Default to the most complete end-state, delivered through small, independently verifiable slices that each build *into* it. Prefer an easier-to-test intermediate **when it's a stepping stone, never as a scope cut**: a cheaper *first step* toward the same end-state is the default; a cheaper *final scope* requires an explicit `D-NN` decision.
- **Ticket-first.** No slice without an issue; the branch and PR reference it. A TODO entering code must carry a ticket — `TODO(#NN)` — a naked TODO is a defect (gated by CI and `definition_of_done`).
- **Defer = file now.** The moment work is deferred or an idea worth keeping appears, file the issue (`track_followups`) — then continue. Promises in chat don't survive compaction; tickets do.
- **Checkpoint at every merge.** Update the Status line + ROADMAP state in the same breath as the merge. Compaction can then strike at any time and lose at most the in-flight slice.
- **Token discipline.** Grep the indexes, never load them; read narrowly; delegate broad reads to read-only subagents and keep conclusions, not file dumps (cheap/fast models for mechanical sweeps, the strongest for adversarial lenses). Detail lives in skills (lazy-loaded), not in this file.
- **Follow the written system.** These docs and skills encode the judgment; prefer them over improvisation, and verify with evidence — never claim green without output. Don't re-litigate settled `D-NN` decisions.
- **Keep the library honest.** If you extend `textbooks/`, regenerate `SECTIONS.json` and run the audits (they exit non-zero; CI enforces them).
