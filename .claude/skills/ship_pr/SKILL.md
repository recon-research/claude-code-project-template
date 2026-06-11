---
name: ship_pr
description: Ship a change through the PR-gated flow — preflight, feature branch, properly-formatted commit, gh PR, CI watch, merge per the project's merge policy, prune, merge-time checkpoint — encoding the gh/PowerShell gotchas so the mechanics never need rediscovering. Use whenever work is ready to land on main. Say "ship it", "open a PR", "land this", "merge this change". Direct pushes to main are policy-forbidden; this is the only path.
---

# Ship PR (the gated path to main)

The mechanics of landing work. Read the merge policy, branch naming, and PR title convention from `PROJECT_CONVENTIONS.md` › Tracker & Hygiene; the PR body shape from `.github/PULL_REQUEST_TEMPLATE.md`.

## Procedure

1. **Preflight** — `scripts/preflight.sh` (or `scripts\preflight.ps1`) must PASS. Re-run after *any* edit, however small — the classic CI failure is an edit made after the format check ran.
2. **Branch** — from up-to-date `main`: `git checkout -b <branch per conventions>` (e.g. `slice/<issue#>-<slug>`). Never commit on `main`.
3. **Commit** — stage explicitly (`git add <paths>`; check `git status` for strays). Multiline message via the **Bash tool** with a here-doc (PowerShell here-string quoting mangles git args):
   ```bash
   git commit -F - <<'EOF'
   <type>: <imperative summary ≤ 72 chars> (closes #NN)

   <what + why; cite Book NN §X / research note; name the gates run>
   EOF
   ```
4. **Push + PR** — `git push -u origin <branch>`, then `gh pr create --body-file <tempfile>` with a body following the PR template (what & why · DoD evidence · tracker hygiene). Write the tempfile UTF-8. **Always `--body-file`, never inline `--body`** (Windows PowerShell 5.1 splits inline bodies at embedded double quotes; body-file is portable everywhere). Building on an unratified decision default? The body carries `Provisional on #NN` — the overrule path greps for it.
5. **Watch CI** — `gh pr checks <n> --watch` (or poll `gh pr checks <n>`). Expect **one** run per commit (push CI is main-only by design). All checks green before merge; a red check routes back to step 1 via preflight — a clean preflight with a red CI is environmental (read the log, don't guess).
6. **Merge + prune** — `gh pr merge <n> --squash --delete-branch` (or the project's merge mode per conventions). Known behavior, not errors: it also deletes the **local** branch and fast-forwards local `main` — so a later `git branch -d` says "not found" and `git pull` says "Already up to date". Finish with `git remote prune origin` and verify `git log --oneline -1` on `main` shows the merge commit.
7. **Checkpoint (mandatory, same breath as the merge)** — the merge-time checkpoint: update the `CLAUDE.md` Status line (one line for what just merged + the **Resume** line) and the ROADMAP slice/milestone state. Pre-`origin`, tick the item in `PROJECT_BACKLOG.md` instead. Compaction can then strike at any time and lose at most the in-flight slice.

## Output

The PR URL, the merged commit hash on `main`, and the CI result (which checks ran, their states).

## Verification

- Preflight PASS precedes the push (evidence: its final line).
- CI green on the PR before merge; `main` fast-forwarded to the merge commit; no leftover branch, local or remote.
- The PR body names the gates actually run; any validation only a specific machine could perform is declared with its evidence link (see conventions › Validation machines, if used).
- The Status line + ROADMAP reflect the merge (gate: definition_of_done's merge-time-checkpoint).

## Don't

- Don't push to `main` directly — policy-forbidden regardless of what the permission grammar allows; don't retry it expecting otherwise.
- Don't `--no-verify`, don't amend published commits, don't force-push shared branches — a broken branch gets a new branch.
- Don't `gh pr merge --admin` — it bypasses the required checks; if a green PR won't merge, merge `main` *into* the branch, re-preflight, wait for green.
- Don't merge with a failing or still-running check "because it's probably fine".
- Don't inline multiline bodies/messages on PowerShell — body-file / here-doc only (conventions › PR / commit mechanics).
