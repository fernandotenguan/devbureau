#!/usr/bin/env python3
"""
reinject_on_compact.py - Claude Code SessionStart hook (matcher: "compact").

When a long session hits the context ceiling and gets compacted, the P0 rules
loaded from CLAUDE.md can be summarized away, and the agent quietly reverts to
generic behavior. This reprints a minimal kernel of those rules plus the
current task state, so the next turn still knows it's operating under DevBureau.

Registered on SessionStart, not PreCompact, on purpose: per Claude Code's hook
reference, PreCompact stdout goes to the debug log only, while SessionStart is
one of the events whose plain-text stdout is added back as context.

Advisory-only: any failure exits 0 silently. A broken hook must never cost the
user a session.
"""

import json
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

REPO_ROOT = Path(__file__).resolve().parents[3]
MAX_LISTED_FILES = 10

# Deliberately terse. This is paid on every compaction, so it carries only the
# rules whose absence changes behavior — the full set stays in CLAUDE.md.
KERNEL = """\
[DevBureau — P0 kernel reinjected after context compaction]

The full rule set is in .claude/CLAUDE.md and is still authoritative. Do not
re-read .agent/rules/DEVBUREAU.md: it is the same content by another name.

1. Open every reply with the tag `DevBureau: Active`.
2. Classify first: QUESTION / SURVEY-INTEL / SIMPLE CODE take the Fast-Track
   (no Socratic Gate, no agent announcement). COMPLEX CODE / DESIGN-UI / full
   orchestration take the full flow: Socratic Gate, then announce
   `🤖 Applying knowledge of @[agent-name]...`, then apply that agent's rules.
3. Evidence before claims. "Tests pass", "build works", "bug fixed" require
   fresh output from a command run in THIS message. No "should work now".
4. Approval matrix. Local and reversible (edit, create, local commit) is
   automatic. Push, delete, drop, deploy, prod secrets require asking first,
   translated into business terms. Force-push to main is refused.
5. Surgical changes. Touch only what the request requires; mention adjacent
   problems instead of fixing them.
6. Loop protection. Same failing action 3x, or no progress for 5 tool calls:
   stop, state what was tried, offer alternatives, wait for the user.
7. Style: no preamble, no em-dash in Portuguese, business language first,
   technical detail only if asked."""


def task_state() -> str:
    """Branch plus uncommitted files, so the reinjected turn knows where it is."""
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""

    if not branch:
        return ""

    lines = [line.strip() for line in status.splitlines() if line.strip()]
    parts = [f"\n[Task state] branch: {branch}"]
    if lines:
        shown = lines[:MAX_LISTED_FILES]
        parts.append(f"uncommitted ({len(lines)}):")
        parts.extend(f"  {entry}" for entry in shown)
        if len(lines) > len(shown):
            parts.append(f"  ... and {len(lines) - len(shown)} more")
    else:
        parts.append("working tree clean")
    return "\n".join(parts)


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    # The matcher already filters this, but a hand-edited settings.json could
    # register it broadly — don't pay the kernel on every ordinary startup.
    if payload.get("reason") != "compact":
        sys.exit(0)

    print(KERNEL)
    print(task_state())
    sys.exit(0)


if __name__ == "__main__":
    main()
