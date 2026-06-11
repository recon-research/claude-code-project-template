# AUTOMATION.md — The Operator Console

The automation surfaces beyond the core loop. §1–2 are **already wired** in this template; §3–5 **require the human once** (credentials/UI). Standing rule either way: `.claude/settings.json` is permission machinery — the agent only changes it on your explicit, in-your-own-words instruction. Each item is tiered like a research note. Lazy-read: nothing here loads into sessions.

## 1. Hooks — zero-token mechanical gates `[production-proven]` *(wired)*

Two hook scripts in [`.claude/hooks/`](../.claude/hooks/), wired in [`settings.json`](../.claude/settings.json) (each file's header documents its contract; both **fail open** — any internal error allows, so a hygiene hook can never wedge the loop; docs: https://code.claude.com/docs/en/hooks, accessed 2026-06-10):

| Hook | Event | What it does |
|---|---|---|
| [`block_naked_todos.py`](../.claude/hooks/block_naked_todos.py) | `PreToolUse` (Bash\|PowerShell) | Blocks `git commit` while the staged diff adds a naked TODO/FIXME — local CI parity at the moment of commit, zero tokens. Blocking hooks take precedence over the allowlist, so the pre-approved `git commit:*` can't bypass it. The matcher covers **both shell tools** — on native Windows the agent commits via PowerShell, and a Bash-only matcher silently never fires. |
| [`session_start_banner.py`](../.claude/hooks/session_start_banner.py) | `SessionStart` (startup\|resume\|clear + compact) | Injects a 1–3 line banner: Status-anchor staleness (As-of sha vs HEAD) + the open decision queue. The `compact` matcher re-grounds the agent right after a surprise compaction; `clear` covers post-`/clear` windows, which start just as blank. ~100 tokens. |

Hook config is snapshotted at session start — edits take effect next session (or after review via `/hooks`). Don't add a **blocking** PreCompact hook — wedging compaction at full context is worse than anything it could check.

## 2. The `settings.json` posture *(wired — owner-approved 2026-06-10)*

What the committed file carries, and why:

- **allow** — the full autopilot loop in **both shell tools** (Bash *and* PowerShell — on native Windows the agent runs PowerShell, and an un-mirrored allowlist prompts at every step): read git/gh, tracker writes, branch/commit/push, PR create+checks+merge, `scripts/preflight.{sh,ps1}`, and the library/research audits (cwd-independent, so both root-relative and in-dir spellings work). The git grants are **narrowed** to the loop's actual shapes: `checkout -b` (not bare `checkout`, which would pre-approve `checkout -- .` discards), `push -u origin` / `push origin` (not bare `push`), `worktree add/list/prune` (not `remove`); `git rm` and `git stash` are deliberately absent (rescue-branch, don't stash), and PowerShell gets **no `git commit`** — commits route through the Bash here-doc path (conventions › PR / commit mechanics).
- **deny** — tripwires for the policy-forbidden forms in both shells: `git push --force` / `-f`, `gh pr merge --admin`. The prefix grammar can't catch every flag position (`git push origin --force`, `gh pr merge 12 --admin` slip the prefixes), so these are seatbelts, not the guard — the guard is branch protection with **"include administrators"** where the plan enforces it (§5, including the free-tier caveat) plus the written policy (`PROJECT_CONVENTIONS.md` › Merge policy).
- **hooks** — §1, via the braced `${CLAUDE_PROJECT_DIR}` placeholder, which Claude Code substitutes itself before any shell parses the command — so the wiring is shell-independent and works from any launch directory (the unbraced form relied on POSIX expansion and could invert the fail-open design into a fail-closed block on Windows).
- **Optional, not set:** `fallbackModel` — fallback model(s) tried when the primary is unavailable (changelog v2.1.166) — would keep an overnight run alive through an availability blip. Verify the current key shape in the docs before adding. `[published]`

## 3. `@claude` GitHub Actions — answer decision issues from your phone `[production-proven]`

`anthropics/claude-code-action@v1` responds to `@claude` mentions on issues/PRs and can implement + open PRs (https://code.claude.com/docs/en/github-actions, accessed 2026-06-10). With it, commenting `@claude go with option B` on a `decision` issue gets the re-route implemented remotely — the decision loop no longer waits for your desk.

- **Auth (Max/Pro):** run `claude setup-token` locally → repo secret `CLAUDE_CODE_OAUTH_TOKEN` → pass as `claude_code_oauth_token` (https://github.com/anthropics/claude-code-action/blob/main/docs/setup.md, accessed 2026-06-10).
- **PUBLIC-repo security** (https://github.com/anthropics/claude-code-action/blob/main/docs/security.md, accessed 2026-06-10): triggers are restricted to users with **write access** by default — keep it that way; never set `allowed_non_write_users`; leave `show_full_output` off (logs are public); third-party issue text is prompt-injection surface even with sanitization; bound cost with `claude_args: --max-turns`.
- Minimal workflow (`.github/workflows/claude.yml` — not shipped; add when you add the secret):

```yaml
name: Claude
on:
  issue_comment: { types: [created] }
  pull_request_review_comment: { types: [created] }
jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions: { contents: write, pull-requests: write, issues: write, id-token: write, actions: read }
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          claude_args: "--max-turns 30"
```

## 4. Scheduled runs — nightly hygiene without a session `[production-proven]`

- **Desktop app → Routines → New routine → Local** (https://code.claude.com/docs/en/desktop-scheduled-tasks, accessed 2026-06-10): runs a fresh session on a schedule, optionally in an isolated worktree, with per-task always-allow permissions. Suggested nightly prompt: *"Run scripts/preflight (audits + hygiene), `python research/tools/_audit_research.py --strict-staleness`, and reconcile the CLAUDE.md Status block against `gh issue list`/`gh pr list`; file a `followup` issue for anything found; change nothing else."*
- **Cloud Routines** `[experimental — research preview]` (https://code.claude.com/docs/en/routines, accessed 2026-06-10): machine-off schedules and GitHub triggers — but only `pull_request`/`release` events (not issues), so decision-issue automation still needs §3.
- **Headless CI** (`claude -p --bare --output-format json`) for scripted gates in Actions (https://code.claude.com/docs/en/headless, accessed 2026-06-10). Note: from June 15, 2026, subscription `claude -p` draws from a separate monthly Agent SDK credit pool.

## 5. Branch protection (repo setup, attended)

Require PRs + the CI checks **and enable "include administrators"** — without it, `gh pr merge --admin` (inside the pre-approved `gh pr merge:*` grant) bypasses every gate. `onboard` Mode A marks this step attended; `gh api` is deliberately not pre-approved.

**Free-tier caveat (hard-won):** on a free-plan **private** repo GitHub does not enforce branch protection or rulesets at all — the protection UI exists but the rules don't bind. Mechanical enforcement requires GitHub Pro, an org plan, or making the repo public. Until then the written merge policy (`PROJECT_CONVENTIONS.md`) plus the allowlist's narrowed grants are the *only* guard — treat the settings.json `$comment`'s honesty about prefix-matching holes as load-bearing, and revisit protection the moment the repo's plan or visibility changes.
