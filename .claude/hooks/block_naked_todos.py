# PreToolUse hook (matcher: Bash): blocks `git commit` while the STAGED diff
# adds a naked TODO/FIXME — the zero-token local twin of ci.yml's hygiene job
# (same exemptions, same per-occurrence rule). Blocking-hook decisions take
# precedence over the allowlist, so the pre-approved `git commit:*` grant
# can't bypass this.
#
# Wiring (see docs/AUTOMATION.md — settings.json changes are owner-applied):
#   "hooks": { "PreToolUse": [ { "matcher": "Bash",
#     "hooks": [ { "type": "command", "command": "python .claude/hooks/block_naked_todos.py" } ] } ] }
#
# Contract: stdin = tool-call JSON; exit 0 = allow, exit 2 = block (stderr
# becomes the reason shown to the agent). Any internal error → allow (exit 0):
# a hygiene hook must never wedge the loop — CI still gates.
# Note: `git commit -a` stages at commit time, so this sees only what was
# staged beforehand — stage-then-commit is the convention anyway.
import json, re, subprocess, sys

EXEMPT = [":!*.md", ":!.github", ":!textbooks", ":!scripts/preflight.sh", ":!scripts/preflight.ps1"]
TICKETED = re.compile(r"(?i)\b(todo|fixme)\(#\d+\)")
NAKED = re.compile(r"(?i)\b(todo|fixme)\b")

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    command = str(payload.get("tool_input", {}).get("command", ""))
    if not re.match(r"\s*git\s+commit\b", command):
        return 0
    try:
        diff = subprocess.run(
            ["git", "diff", "--cached", "--"] + ["."] + EXEMPT,
            capture_output=True, text=True, timeout=15, encoding="utf-8", errors="replace",
        ).stdout
    except Exception:
        return 0
    naked = []
    for line in diff.splitlines():
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if NAKED.search(TICKETED.sub("", line)):
            naked.append(line[:200])
    if not naked:
        return 0
    sys.stderr.write(
        "BLOCKED: staged diff adds naked TODO/FIXME (every occurrence needs a ticket: TODO(#NN)):\n"
        + "\n".join(naked[:10])
        + "\nFile the issue first (track_followups), annotate, restage, retry. CI enforces the same rule.\n"
    )
    return 2

if __name__ == "__main__":
    sys.exit(main())
