#!/usr/bin/env python3
"""
scan_secrets_on_write.py - Claude Code PreToolUse hook.

DEVBUREAU.md says secrets live in .env and never in code. security_scan.py can
find them, but only after they are already on disk and often already committed.
This blocks the write itself.

Only high-confidence, structurally distinctive credentials are matched (key
formats with fixed prefixes and lengths, private key headers, JWTs). Generic
patterns like `password = "..."` are deliberately excluded: a gate that fires
on ordinary code gets disabled within a day, and the deeper scan in
security_scan.py still covers those.

Skips .agent/ (the kit's own tooling carries these patterns as data) and files
named .example/.sample, which exist precisely to show placeholder shapes.

Escape hatch: DEVBUREAU_ALLOW_SECRETS=1 in the environment.

Registered in .claude/settings.json by sync_ide.py's generate_claude_config().
"""

import json
import os
import re
import sys

if sys.platform == "win32":
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (
        re.compile(
            r"aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*[\"'][A-Za-z0-9/+=]{40}[\"']",
            re.IGNORECASE,
        ),
        "AWS secret access key",
    ),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"sk_live_[0-9a-zA-Z]{16,}"), "Stripe live secret key"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"), "GitHub token"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{50,}"), "GitHub fine-grained token"),
    (re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"), "Slack token"),
    (re.compile(r"AIza[0-9A-Za-z_-]{35}"), "Google API key"),
    (re.compile(r"sk-ant-[A-Za-z0-9_-]{20,}"), "Anthropic API key"),
    (
        re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
        "JWT",
    ),
]

SKIPPED_SUFFIXES = (".example", ".sample", ".template", ".dist")


def skipped(file_path: str) -> bool:
    normalized = file_path.replace("\\", "/")
    if "/.agent/" in normalized or normalized.startswith(".agent/"):
        return True
    return normalized.endswith(SKIPPED_SUFFIXES)


def first_match(text: str):
    for pattern, label in SECRET_PATTERNS:
        if pattern.search(text):
            return label
    return None


def main() -> None:
    if os.environ.get("DEVBUREAU_ALLOW_SECRETS") == "1":
        sys.exit(0)

    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool = payload.get("tool_name")
    if tool not in ("Edit", "Write", "MultiEdit"):
        sys.exit(0)

    tool_input = payload.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    if skipped(file_path):
        sys.exit(0)

    if tool == "Write":
        candidates = [tool_input.get("content", "")]
    elif tool == "Edit":
        candidates = [tool_input.get("new_string", "")]
    else:
        candidates = [e.get("new_string", "") for e in tool_input.get("edits", [])]

    for text in candidates:
        label = first_match(text or "")
        if not label:
            continue
        print(
            f"Blocked: this write puts what looks like a {label} into "
            f"{file_path or 'a file'}. Move the value to .env (and add a "
            "placeholder to .env.example), then reference it from there. "
            "If it is a fabricated example, set DEVBUREAU_ALLOW_SECRETS=1.",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
