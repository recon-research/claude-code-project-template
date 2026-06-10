# AUTOMATION.md — The Operator Console (attended setup, once)

Everything on this page extends the autopilot loop but **requires the human once** — either because it edits permission machinery (`.claude/settings.json` is owner-approved by policy; the agent must not change it without your explicit, in-your-own-words instruction) or because it needs credentials/UI. Each item is tiered like a research note. Lazy-read: nothing here loads into sessions.

## 1. Hooks — zero-token mechanical gates `[production-proven]`

Two hook scripts ship in [`.claude/hooks/`](../.claude/hooks/) (inert until wired; each file's header documents its contract; docs: https://code.claude.com/docs/en/hooks, accessed 2026-06-10):

| Hook | Event | What it does |
|---|---|---|
| [`block_naked_todos.py`](../.claude/hooks/block_naked_todos.py) | `PreToolUse` (Bash) | Blocks `git commit` while the staged diff adds a naked TODO/FIXME — local CI parity at the moment of commit, zero tokens. Blocking hooks take precedence over the allowlist, so the pre-approved `git commit:*` can't bypass it. |
| [`session_start_banner.py`](../.claude/hooks/session_start_banner.py) | `SessionStart` (startup\|resume + compact) | Injects a 1–3 line banner: Status-anchor staleness (As-of sha vs HEAD) + the open decision queue. The `compact` matcher re-grounds the agent right after a surprise compaction. ~100 tokens. |

Don't add a **blocking** PreCompact hook — wedging compaction at full context is worse than anything it could check.

## 2. The proposed `settings.json` delta (owner-applied)

Merge this into `.claude/settings.json` by hand, or paste it to the agent **with explicit instructions in your own words** (permission-machinery edits are deliberately not self-serve):

```jsonc
{
  // ADD to permissions.allow (preflight is the most frequent loop command):
  //   "Bash(scripts/preflight.sh:*)", "Bash(bash scripts/preflight.sh:*)",
  //   "Bash(python research/tools/_audit_research.py:*)"
  // (The textbook-audit entries already work — the scripts are cwd-independent.)

  // ADD permissions.deny — narrow tripwires for the policy-forbidden forms
  // (prefix grammar can't catch every flag position; policy + branch
  // protection with "include administrators" are the real guards):
  //   "Bash(git push --force:*)", "Bash(git push -f:*)", "Bash(gh pr merge --admin:*)"

  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command", "command": "python .claude/hooks/block_naked_todos.py" } ] }
    ],
    "SessionStart": [
      { "matcher": "startup|resume",
        "hooks": [ { "type": "command", "command": "python .claude/hooks/session_start_banner.py" } ] },
      { "matcher": "compact",
        "hooks": [ { "type": "command", "command": "python .claude/hooks/session_start_banner.py" } ] }
    ]
  }

  // OPTIONAL: "fallbackModel" — tried in order when the primary is
  // unavailable (changelog v2.1.166) — keeps an overnight run alive through
  // a model-availability blip. Verify the current key shape in the docs
  // before setting. [published]
}
```

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
