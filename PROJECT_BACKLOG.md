# PROJECT_BACKLOG.md — Cross-Session Continuity (a convention, not a tracker)

> Copy this to your **project root** (next to `PROJECT_CONVENTIONS.md`). It is a *convention*, **not** an issue tracker. For real backlog management at scale, use GitHub Issues / Linear / Jira (or the harness's task tools). This file exists only to carry **milestone state across sessions** — so an agent picking the work back up knows what's done, what's next, and what's blocked — keyed to the `STARTER_KIT.md` milestone roadmap.

## How this file is used

- **`plan_work`** appends newly-planned work here under **Next**, each item linked to its plan and the STARTER_KIT milestone it advances.
- **`definition_of_done`** moves an item to **Done** (with the date and the milestone exit-criterion it met) — only once every applicable gate passed.
- The agent reads **Now** first at the start of a session to resume context.

Item format:

```
- [ ] <short-id> — <description> — milestone M<n> — plan: <note/link> — gate: <not-started | in-progress | blocked: why | done YYYY-MM-DD>
```

## Now / In progress
<!-- the one or two items actively being worked; the current STARTER_KIT milestone -->
- (none yet)

## Next
<!-- queued, planned-but-not-started; plan_work appends here -->
- (none yet)

## Blocked
<!-- item + the blocker + what would unblock it -->
- (none yet)

## Done
<!-- definition_of_done moves items here, with date + the milestone exit-criterion met -->
- (none yet)

---
*Keep this short. If it grows past roughly a screen, that's the signal to move to a real tracker. This is continuity, not project management.*
