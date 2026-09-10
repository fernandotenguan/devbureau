#!/usr/bin/env python3
"""
guard_main_branch.py - Claude Code PreToolUse hook.

Stops file edits made directly on main/master and asks for a working branch
first, so shared history stays reviewable.

Deliberately narrow, because DEVBUREAU.md's Decision Matrix treats a local
reversible edit as automatic: it only fires when there is something shared to
protect, meaning a git repo whose branch is main/master AND that has a remote
configured. A purely local repo with no remote is left alone.

Escape hatches, both documented:
  - DEVBUREAU_ALLOW_MAIN_EDITS=1 in the environment (one session)
  - an .agent/.allow-main-edits file in the repo (permanent, per project)

Registered in .claude/settings.json by sync_ide.py's generate_claude_config().
"""

import json
import os
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

PROTECTED = {"main", "master"}
TIMEOUT_SECONDS = 5


def git(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def main() -> None:
    if os.environ.get("DEVBUREAU_ALLOW_MAIN_EDITS") == "1":
        sys.exit(0)

    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    if payload.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    repo_root = git("rev-parse", "--show-toplevel")
    if not repo_root:
        sys.exit(0)  # not a git repo, nothing to protect

    if (Path(repo_root) / ".agent" / ".allow-main-edits").exists():
        sys.exit(0)

    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if branch not in PROTECTED:
        sys.exit(0)

    if not git("remote"):
        sys.exit(0)  # local-only repo: no shared history at stake

    print(
        f"Blocked: editing files directly on '{branch}', which is pushed to a "
        "remote. Create a working branch first:\n"
        "    git checkout -b <descriptive-name>\n"
        "Then re-run the edit. To turn this guard off, set "
        "DEVBUREAU_ALLOW_MAIN_EDITS=1 or create .agent/.allow-main-edits.",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
