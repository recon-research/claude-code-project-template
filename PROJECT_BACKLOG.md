# PROJECT_BACKLOG.md — Pre-Repo Continuity Only (delete once the tracker exists)

> This file carries work items across sessions **only during the window before the GitHub repo exists** (intake → library building). **The moment `origin` is live, migrate every item here to tracker issues and delete this file** — `onboard` (Mode A) and `prepare_compaction` both enforce that. Two backlogs is a staleness machine; the tracker is the only durable one (truth order: git/CI > tracker > docs > chat).

## How this file is used

- Items land under **Next** when planned (`plan_work`'s Backlog step routes here while no `origin` exists), move to **Now** when started, and to **Done** when the `definition_of_done` gates pass (its tracker gate routes here pre-repo).
- The agent reads **Now** first at the start of a session to resume context.
- **Post-repo exception — `## Unfiled`:** if `gh` is briefly unreachable, `track_followups` parks items under an `## Unfiled` heading here (recreating this file if it was retired); `onboard` / `prepare_compaction` drain that section into real issues at the next checkpoint.

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
