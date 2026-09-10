#!/usr/bin/env python3
"""
context_cost.py — Attributes the cost of tool output back to the files that
produced it, so "read narrowly" stops being advice with no price tag.

PRD_final_Gemini_10_09_26.md, A13. DEVBUREAU.md's Context Scoping Discipline
asks for narrow reads and never shows what a read actually cost. This walks
the session transcript once at SessionEnd, pairs each tool result with the
file its call targeted, and records the five most expensive ones.

Only file paths and sizes are stored, never command text or file content:
a command can carry a credential and this ledger is committed.

Usage:
  python .agent/scripts/context_cost.py record   # SessionEnd hook (stdin)
  python .agent/scripts/context_cost.py report   # recurring context hogs
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

REPO_ROOT = Path(__file__).resolve().parents[2]
LEDGER = REPO_ROOT / ".agent" / "memory" / "context-cost.jsonl"

CHARS_PER_TOKEN = 4
TOP_N = 5
FILE_TOOLS = {"Read", "Edit", "Write", "MultiEdit", "NotebookEdit"}
SEARCH_TOOLS = {"Grep", "Glob"}

# Path-shaped tokens inside a shell command. Extensions only, so a bare flag or
# a credential never looks like a file.
PATH_TOKEN = re.compile(
    r"[\w./\\-]+\.(?:py|ts|tsx|js|jsx|md|json|ya?ml|toml|css|scss|html|sh|sql)\b"
)

GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def load_entries(transcript_path: str) -> list:
    try:
        raw = Path(transcript_path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    entries = []
    for line in raw.splitlines():
        try:
            entries.append(json.loads(line))
        except (json.JSONDecodeError, ValueError):
            continue
    return entries


def blocks(entry: dict) -> list:
    content = entry.get("message", {}).get("content")
    return content if isinstance(content, list) else []


def targets_of(name: str, tool_input: dict) -> list:
    """Which files this call should be billed to. Empty means unattributable."""
    if name in FILE_TOOLS:
        path = tool_input.get("file_path")
        return [str(path)] if path else []
    if name in SEARCH_TOOLS:
        path = tool_input.get("path")
        return [str(path)] if path else ["(repo-wide search)"]
    if name == "Bash":
        command = str(tool_input.get("command", ""))
        return list(dict.fromkeys(PATH_TOKEN.findall(command)))
    return []


def normalize(target: str) -> str:
    try:
        return Path(target).resolve().relative_to(REPO_ROOT).as_posix()
    except (ValueError, OSError):
        return target.replace("\\", "/")


def measure(entries: list) -> dict:
    """Sum result size per target, splitting a result across its targets."""
    pending = {}
    cost = defaultdict(lambda: {"tokens": 0, "calls": 0})
    total = 0

    for entry in entries:
        for block in blocks(entry):
            kind = block.get("type")
            if kind == "tool_use":
                found = targets_of(block.get("name", ""), block.get("input", {}))
                if found:
                    pending[block.get("id")] = found
            elif kind == "tool_result":
                size = len(json.dumps(block.get("content"), default=str))
                total += size
                found = pending.pop(block.get("tool_use_id"), [])
                if not found:
                    continue
                share = size // len(found)
                for target in found:
                    slot = cost[normalize(target)]
                    slot["tokens"] += share // CHARS_PER_TOKEN
                    slot["calls"] += 1

    ranked = sorted(cost.items(), key=lambda kv: -kv[1]["tokens"])
    return {
        "total_result_tokens": total // CHARS_PER_TOKEN,
        "attributed": [
            {"target": target, "tokens": data["tokens"], "calls": data["calls"]}
            for target, data in ranked[:TOP_N]
        ],
    }


def command_record() -> None:
    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return

    entries = load_entries(payload.get("transcript_path", ""))
    if not entries:
        return

    row = measure(entries)
    if not row["attributed"]:
        return
    row["session_id"] = payload.get("session_id", "")
    row["recorded_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    try:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with open(LEDGER, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    except OSError:
        return


def load_rows() -> list:
    if not LEDGER.exists():
        return []
    rows = []
    for line in LEDGER.read_text(encoding="utf-8", errors="ignore").splitlines():
        try:
            rows.append(json.loads(line))
        except (json.JSONDecodeError, ValueError):
            continue
    return rows


def command_report() -> None:
    rows = load_rows()
    print(f"\n{BOLD}💸 DevBureau — Context Cost{RESET}")
    if not rows:
        print(
            f"  {YELLOW}⚠{RESET} No sessions recorded yet. The SessionEnd hook writes "
            f"to {LEDGER.relative_to(REPO_ROOT)} as sessions end.\n"
        )
        return

    totals = defaultdict(lambda: {"tokens": 0, "sessions": 0})
    for row in rows:
        for item in row.get("attributed", []):
            slot = totals[item["target"]]
            slot["tokens"] += item["tokens"]
            slot["sessions"] += 1

    session_total = sum(r.get("total_result_tokens", 0) for r in rows)
    print(
        f"  {CYAN}Sessions:{RESET} {len(rows)}   "
        f"{CYAN}Tool output across them:{RESET} ~{session_total:,} tokens"
    )
    print(f"\n  {'Target':<52} {'Tokens':>9}  {'Sessions':>8}")
    print(f"  {'-' * 52} {'-' * 9}  {'-' * 8}")

    ranked = sorted(totals.items(), key=lambda kv: -kv[1]["tokens"])[:10]
    for target, data in ranked:
        label = target if len(target) <= 52 else "…" + target[-51:]
        print(f"  {label:<52} {data['tokens']:>9,}  {data['sessions']:>8}")

    repeat = [t for t, d in ranked if d["sessions"] >= 3]
    if repeat:
        print(
            f"\n  {YELLOW}Recurring:{RESET} {', '.join(repeat[:3])}\n"
            "  A file that lands here every session is a candidate for splitting,\n"
            "  or for a summary an agent can read instead of the whole thing.\n"
        )
    else:
        print(f"\n  {GREEN}✔{RESET} No file is a hog across 3+ sessions yet.\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["record", "report"])
    args = parser.parse_args()

    if args.command == "record":
        command_record()
    else:
        command_report()


if __name__ == "__main__":
    main()
