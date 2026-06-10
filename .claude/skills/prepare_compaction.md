---
name: prepare_compaction
description: Checkpoint the session before context is compacted or the session ends, so the next session resumes from the docs alone. Use when the user says "let's prepare for compaction", "prepare to compact", "checkpoint", or "wrap up the session". Rewrites and stamps the Status block, VERIFIES its claims against the tracker, updates roadmap/decision log, sweeps deferrals into tickets, and leaves the tree clean and pushed.
---

# Prepare For Compaction

The durable memory is the docs + the issue tracker, not the chat. This skill flushes everything in-flight to those — and **verifies** the result, because a stale checkpoint is worse than none. If you've checkpointed at every merge (the standing rule), this is mostly verification, not archaeology.

## Procedure

1. **Rewrite the Status block** in [`CLAUDE.md`](../../CLAUDE.md) to reflect reality, and **stamp it**: `As of: <today> · <main short-sha>`.
   - Phase · milestone · CI state of main.
   - **Done** (closed this session, by PR #), **In progress** (+ issue/PR #), **Next** (1–3 slices by issue #).
   - **Decisions awaiting the human** — must exactly mirror `gh issue list --label decision`; mark any proceeding provisionally.
   - **Resume** in the strict format: `<branch> · <issue #> · <one imperative next action> · verify with: <command>` — specific enough that a cold session needs nothing else.
2. **Verify the claims (anti-staleness gate).** Cross-check mechanically before moving on:
   - every **Done** item ↔ a merged PR exists (`gh pr list --state merged -L 10`);
   - every **In progress / Next** item ↔ an open issue;
   - the decision list ↔ `gh issue list --label decision`, exactly;
   - ROADMAP slice/milestone states match the above. Fix every mismatch **now** — docs are caches of the tracker.
3. **Update the durable docs.** Reflect milestone progress in [`docs/ROADMAP.md`](../../docs/ROADMAP.md); record any decision made this session as `D-NN` in [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) Appendix A. If a milestone closed, sanity-check the next milestone's slices against what was learned — re-plan via `plan_work` if stale; **plans are caches too**.
4. **Sweep deferrals.** Run [`track_followups`](track_followups.md): anything deferred, promised, or ideated that lives only in chat becomes an issue (labels: `followup` / `idea` / `debt`). This should find little if "defer = file now" was followed mid-session — treat every catch here as a near-miss.
5. **Retire the scratch backlog.** If `origin` exists and `PROJECT_BACKLOG.md` is still present, migrate its items to issues and delete the file (it's pre-repo continuity only).
6. **Leave the tree clean and pushed.** Commit merged work; push; note CI state in Status (a red CI is noted, never hidden). If `textbooks/` was touched, regenerate `SECTIONS.json` and run the audits (they exit non-zero — fix before declaring the checkpoint done).

## Verification

- A cold reader could resume from the Status block alone — branch, issue, action, verify-command.
- Step 2's cross-checks all pass: Status ↔ tracker ↔ ROADMAP agree; the As-of stamp matches today + HEAD.
- `gh issue list` shows every deferred item; nothing actionable lives only in this conversation.
- `git status` clean; pushed; CI state recorded honestly.

## Don't

- Don't write the Status block from memory of the session — derive it from `git log` + `gh issue list`/`gh pr list`, then verify (step 2 is not optional).
- Don't leave a vague Resume point ("continue M3") — name the branch, issue, action, and verify command.
- Don't let actionable follow-ups evaporate into chat; and don't keep `PROJECT_BACKLOG.md` alive once the tracker exists.
- Don't push failing work silently — note it, or don't push it.
- Don't write a novel — the Status block is ~10 lines; detail belongs in the ROADMAP and the tracker.
