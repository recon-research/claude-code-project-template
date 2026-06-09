---
name: prepare_compaction
description: Checkpoint the session before context is compacted or the session ends, so the next session can resume cleanly from the docs alone. Use when the user says "let's prepare for compaction", "prepare to compact", "checkpoint", or "wrap up the session". Rewrites the Status block, updates the roadmap and decision log, files deferred work as issues, and leaves the tree clean.
---

# Prepare For Compaction

The durable memory is the docs + the issue tracker, not the chat. This skill flushes everything in-flight to those before context is lost.

## Procedure

1. **Rewrite the Status block** at the top of [`CLAUDE.md`](../../CLAUDE.md) to reflect reality:
   - Phase · milestone · CI state.
   - **Done** (what closed this session), **In progress** (+ issue/PR #), **Next** (1–3 slices).
   - **Open decisions awaiting the human** (list `D-NN`, or "none").
   - **Resume point** — the exact next action a cold session should take. Be specific enough that onboarding needs nothing else.
2. **Update the roadmap and decision log.** Reflect milestone progress in [`docs/ROADMAP.md`](../../docs/ROADMAP.md); if a decision was made this session, record it in [`docs/ARCHITECTURE.md`](../../docs/ARCHITECTURE.md) Appendix A as `D-NN`.
3. **File deferred work.** Run [`track_followups`](track_followups.md): every actionable follow-up, TODO, or "we should later…" becomes a GitHub issue with enough context to act cold (file paths, why deferred, originating PR/issue #). Nothing actionable stays only in chat or a closed-issue comment.
4. **Update continuity.** If the project uses [`PROJECT_BACKLOG.md`](../../PROJECT_BACKLOG.md), move completed items to Done and surface the current Now/Next. (At scale, the issue tracker is authoritative; keep the backlog short.)
5. **Leave the tree clean.** Commit and push merged work; ensure CI is green or the failure is noted in Status. Don't push broken work without flagging it.
6. **If you touched the library**, regenerate `SECTIONS.json` and run the audits so it stays consistent (see [AGENT_GUIDE.md](../../textbooks/AGENT_GUIDE.md) §6).

## Verification

- A cold reader could open `CLAUDE.md`, read the Status block, and know exactly what to do next — without the chat.
- `gh issue list` shows every deferred item as an open ticket; none live only in chat.
- `git status` is clean (or the dirty state is intentional and noted in Status).

## Don't

- Don't leave the Status block stale — that's the one thing the next session relies on.
- Don't let actionable follow-ups evaporate into the chat log; file them.
- Don't push failing work silently; note CI state in Status.
- Don't write a novel — the Status block is ~10 lines. Detail belongs in the ROADMAP and issues.
