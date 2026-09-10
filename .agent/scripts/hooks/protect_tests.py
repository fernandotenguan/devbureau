#!/usr/bin/env python3
"""
protect_tests.py - Claude Code PreToolUse hook.

DEVBUREAU.md's Zero-Break protocol says a passing suite must reflect a general
solution, never a fit to the visible cases. The cheapest way to fake a green
suite is to delete, empty or skip the test that fails, and nothing enforced
that until now. This blocks the three mechanical forms of it:

  - deleting or renaming a test file from Bash
  - adding a skip/xfail marker that wasn't there before
  - rewriting a test file down to a fraction of its previous size

Only fires on paths that look like tests. Creating new tests is always allowed.
Escape hatch, when the user genuinely wants a test gone:
set DEVBUREAU_ALLOW_TEST_EDITS=1 in the environment.

Registered in .claude/settings.json by sync_ide.py's generate_claude_config().
"""

import json
import os
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

TEST_PATH = re.compile(
    r"(^|[/\\])(tests?|__tests__|spec|specs)([/\\])"
    r"|(^|[/\\])test_[^/\\]+\.py$"
    r"|_test\.py$"
    r"|\.(test|spec)\.[jt]sx?$",
    re.IGNORECASE,
)

# Deleting a path that looks like a test, from the shell.
DELETE_COMMAND = re.compile(
    r"(?:^|[;&|]\s*)(?:rm|del|erase)\s+[^;&|]*|(?:^|[;&|]\s*)git\s+rm\s+[^;&|]*",
    re.IGNORECASE,
)

SKIP_MARKERS = (
    "@pytest.mark.skip",
    "@pytest.mark.xfail",
    "@unittest.skip",
    "pytest.skip(",
    "it.skip(",
    "test.skip(",
    "describe.skip(",
    "xit(",
    "xdescribe(",
    "@Ignore",
)

# A rewrite this much smaller than the original is a gutting, not an edit.
SHRINK_RATIO = 0.4


def looks_like_test(path: str) -> bool:
    return bool(path) and bool(TEST_PATH.search(path.replace("\\", "/")))


def block(message: str) -> None:
    print(f"Blocked: {message}", file=sys.stderr)
    print(
        "If the user explicitly asked for this, say so and ask them to confirm, "
        "or set DEVBUREAU_ALLOW_TEST_EDITS=1. Never disable a test to make a "
        "suite go green (DEVBUREAU.md, Zero-Break protocol).",
        file=sys.stderr,
    )
    sys.exit(2)


def check_bash(command: str) -> None:
    for fragment in DELETE_COMMAND.findall(command):
        target = fragment if isinstance(fragment, str) else " ".join(fragment)
        for token in target.split():
            if token.startswith("-"):
                continue
            if looks_like_test(token):
                block(f"this command deletes a test path ({token}).")


def added_markers(old: str, new: str) -> list:
    return [m for m in SKIP_MARKERS if m in new and m not in old]


def check_edit(file_path: str, old: str, new: str) -> None:
    markers = added_markers(old, new)
    if markers:
        block(f"this edit adds {markers[0]} to a test file ({file_path}).")


def check_write(file_path: str, content: str) -> None:
    path = Path(file_path)
    if not path.exists():
        return  # creating a new test file is always fine

    try:
        previous = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return

    markers = added_markers(previous, content)
    if markers:
        block(f"this rewrite adds {markers[0]} to a test file ({file_path}).")

    if previous.strip() and len(content) < len(previous) * SHRINK_RATIO:
        block(
            f"this rewrite shrinks a test file from {len(previous)} to "
            f"{len(content)} characters ({file_path})."
        )


def main() -> None:
    if os.environ.get("DEVBUREAU_ALLOW_TEST_EDITS") == "1":
        sys.exit(0)

    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool = payload.get("tool_name")
    tool_input = payload.get("tool_input", {})

    if tool == "Bash":
        check_bash(tool_input.get("command", ""))
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not looks_like_test(file_path):
        sys.exit(0)

    if tool == "Edit":
        check_edit(
            file_path,
            tool_input.get("old_string", ""),
            tool_input.get("new_string", ""),
        )
    elif tool == "MultiEdit":
        for edit in tool_input.get("edits", []):
            check_edit(
                file_path, edit.get("old_string", ""), edit.get("new_string", "")
            )
    elif tool == "Write":
        check_write(file_path, tool_input.get("content", ""))

    sys.exit(0)


if __name__ == "__main__":
    main()
