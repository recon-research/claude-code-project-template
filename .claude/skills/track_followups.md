---
name: track_followups
description: Make sure deferred work and unresolved review findings live in the durable backlog (GitHub issues) — not only in chat, a PR / issue comment, or a memory note, which are lost between sessions and on compaction. Use whenever you consciously defer a finding or follow-up, before closing an issue / epic that has deferred items, and before compaction. Say "track this", "file a follow-up", "are we tracking X", "don't lose this". The companion to adversarial_review's deferral step.
---

# Track Follow-ups (Durable Backlog Discipline)

Anything worth doing later must become a **GitHub issue** — the live backlog. Chat scrolls off, memory notes drift, and a comment on a *closed* issue never appears in `gh issue list`. If a follow-up only lives in those places, it is effectively gone next session. Read the repo + label set from `PROJECT_CONVENTIONS.md`; use the project's `gh` CLI.

## When to run

- You finished a change but consciously **deferred** something (a perf cleanup, a missing test, an edge case, a "do this once X lands").
- An `adversarial_review` (or `/code-review`) produced findings you won't fix now.
- **Before closing an issue or a multi-PR epic** that has deferred items — a closed issue's comment does *not* track them.
- **Before compaction / end of session** — sweep for "we should later…" items that live only in the conversation.

## Procedure

1. **Decide append vs new.** Check `gh issue list` first. If an open issue already covers the area, **append** a checklist item to it. Otherwise **file a new issue** (`gh issue create`) with the project's labels and a back-reference to the originating PR / issue / epic.
2. **Write it to be actioned cold.** A future session has none of this context. Include *what*, *why it was deferred*, the **file paths**, the originating PR / epic number, and any grounding / citation. One checkbox per item.
3. **Cross-link both ways.** Reference the new ticket from where the work came from — the PR description, the closing comment on the parent issue, and the relevant memory note (so memory reads "tracked in #N", not "documented somewhere").
4. **Gate on it before closing / compacting.** Don't close an epic until `gh issue list` shows its follow-ups as **open** tickets — consolidate several into one if needed. Don't end a session with deferred work parked only in chat.

## Output

- The ticket number(s) created or updated.
- The cross-links done (PR body / parent-issue comment / memory now name the ticket).

## Verification

- `gh issue list` shows the deferred work as open issue(s).
- The source (PR body / parent-issue comment / memory) names the ticket number.
- Nothing actionable-and-deferred remains only in the conversation or a closed-issue comment.

## Don't

- Don't treat a memory note or a comment on a *closed* issue as tracking — it isn't in the backlog.
- Don't file duplicates — check for an existing open issue first and append to it.
- Don't file noise: ticket only genuinely-worth-doing items. Trivial or low-confidence ones get done inline now, or dropped — not filed.
- Don't defer a Critical / High correctness finding to a ticket to dodge fixing it — tickets are for *non-blocking* work.
