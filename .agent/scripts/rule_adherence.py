#!/usr/bin/env python3
"""
rule_adherence.py — Measures which DEVBUREAU.md rules the model actually
follows, so pruning the rule set is driven by evidence instead of guesswork.

docs/prd-2026-09/PRD_final_Gemini_10_09_26.md, E2.2. The kit carries ~40 KB of always-loaded
rules and nobody knows which of them change behavior. Before cutting anything,
measure. Six rules are mechanically verifiable from the session transcript;
each session contributes one row, and `report` aggregates them.

Only verdicts are stored, never message content, per DEVBUREAU.md's Context
Hygiene rule.

Usage:
  python .agent/scripts/rule_adherence.py record   # SessionEnd hook (stdin)
  python .agent/scripts/rule_adherence.py report   # aggregate scorecard
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
LEDGER = REPO_ROOT / ".agent" / "memory" / "rule-adherence.jsonl"

EDIT_TOOLS = {"Edit", "Write", "MultiEdit"}
COMPLEX_FILE_THRESHOLD = 3  # DEVBUREAU.md: "3+ arquivos" marks a non-trivial task
LOW_ADHERENCE = 0.5

OPENING_TAG = "DevBureau: Active"
ANNOUNCEMENT = "Applying knowledge of"
VERIFY_COMMAND = re.compile(
    r"\b(pytest|npm (?:test|run build)|pnpm (?:test|build)|yarn (?:test|build)"
    r"|tsc\b|ruff\b|doctor\.py|checklist\.py|verify_all\.py|go test|cargo test)",
    re.IGNORECASE,
)
PORTUGUESE = re.compile(
    r"\b(não|também|então|você|porque|apenas|sobre)\b", re.IGNORECASE
)

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

PASS, FAIL, NA = "pass", "fail", "n/a"

RULE_LABELS = {
    "opening_tag": ("Opening tag `DevBureau: Active`", "high"),
    "agent_announced": ("Agent announced on a complex task", "high"),
    "fresh_evidence": ("Verification command run after editing", "medium"),
    "auto_fixer_run": ("auto_fixer.py run before finishing", "medium"),
    "gate_before_edit": ("A question was asked before the first edit", "low"),
    "no_emdash_pt": ("No em-dash in Portuguese prose", "medium"),
}


# ── transcript parsing ────────────────────────────────────────────────────────


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


def content_blocks(entry: dict) -> list:
    content = entry.get("message", {}).get("content")
    return content if isinstance(content, list) else []


def is_human_turn(entry: dict) -> bool:
    """A real user message, as opposed to a tool result echoed back as 'user'."""
    if entry.get("type") != "user":
        return False
    content = entry.get("message", {}).get("content")
    if isinstance(content, str):
        return True
    return not any(b.get("type") == "tool_result" for b in content_blocks(entry))


class Session:
    """Everything the checks need, collected in a single pass."""

    def __init__(self) -> None:
        self.openings: list = []
        self.texts: list = []
        self.bash_commands: list = []
        self.edited_files: set = set()
        self.asked_before_edit = False
        self.announced = False
        self._expecting_opening = False
        self._edited_yet = False

    @property
    def is_complex(self) -> bool:
        return len(self.edited_files) >= COMPLEX_FILE_THRESHOLD

    def feed(self, entry: dict) -> None:
        if is_human_turn(entry):
            self._expecting_opening = True
            return
        if entry.get("type") != "assistant":
            return
        for block in content_blocks(entry):
            self._feed_block(block)

    def _feed_block(self, block: dict) -> None:
        kind = block.get("type")
        if kind == "text":
            self._feed_text(block.get("text", ""))
        elif kind == "tool_use":
            self._feed_tool(block)

    def _feed_text(self, text: str) -> None:
        if not text.strip():
            return
        self.texts.append(text)
        if self._expecting_opening:
            self.openings.append(text)
            self._expecting_opening = False
        if ANNOUNCEMENT in text:
            self.announced = True
        if not self._edited_yet and text.rstrip().endswith("?"):
            self.asked_before_edit = True

    def _feed_tool(self, block: dict) -> None:
        name = block.get("name", "")
        tool_input = block.get("input", {})
        if name == "AskUserQuestion" and not self._edited_yet:
            self.asked_before_edit = True
        if name == "Bash":
            self.bash_commands.append(str(tool_input.get("command", "")))
        if name in EDIT_TOOLS:
            path = tool_input.get("file_path")
            if path:
                self.edited_files.add(str(path))
            self._edited_yet = True


# ── the six checks ────────────────────────────────────────────────────────────


def tagged_openings(session: Session) -> int:
    return sum(1 for text in session.openings if text.lstrip().startswith(OPENING_TAG))


def check_opening_tag(session: Session) -> str:
    # A ratio, not all-or-nothing: one untagged interjection in a long session
    # says something different from never using the tag at all.
    if not session.openings:
        return NA
    return PASS if tagged_openings(session) / len(session.openings) >= 0.8 else FAIL


def check_agent_announced(session: Session) -> str:
    if not session.is_complex:
        return NA
    return PASS if session.announced else FAIL


def check_fresh_evidence(session: Session) -> str:
    if not session.edited_files:
        return NA
    return (
        PASS if any(VERIFY_COMMAND.search(c) for c in session.bash_commands) else FAIL
    )


def check_auto_fixer(session: Session) -> str:
    if not session.edited_files:
        return NA
    return PASS if any("auto_fixer.py" in c for c in session.bash_commands) else FAIL


def check_gate_before_edit(session: Session) -> str:
    if not session.is_complex:
        return NA
    return PASS if session.asked_before_edit else FAIL


def check_no_emdash_pt(session: Session) -> str:
    portuguese = [t for t in session.texts if PORTUGUESE.search(t)]
    if not portuguese:
        return NA
    return PASS if not any("—" in t for t in portuguese) else FAIL


CHECKS = {
    "opening_tag": check_opening_tag,
    "agent_announced": check_agent_announced,
    "fresh_evidence": check_fresh_evidence,
    "auto_fixer_run": check_auto_fixer,
    "gate_before_edit": check_gate_before_edit,
    "no_emdash_pt": check_no_emdash_pt,
}


def evaluate(entries: list) -> dict:
    session = Session()
    for entry in entries:
        session.feed(entry)
    return {
        "edited_files": len(session.edited_files),
        "complex": session.is_complex,
        "openings_tagged": tagged_openings(session),
        "openings_total": len(session.openings),
        "rules": {name: check(session) for name, check in CHECKS.items()},
    }


# ── commands ──────────────────────────────────────────────────────────────────


def command_record() -> None:
    """SessionEnd hook. Silent and never blocking: its output is ignored anyway."""
    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return

    entries = load_entries(payload.get("transcript_path", ""))
    if not entries:
        return

    row = evaluate(entries)
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
    print(f"\n{BOLD}📊 DevBureau — Rule Adherence{RESET}")
    if not rows:
        print(
            f"  {YELLOW}⚠{RESET} No sessions recorded yet. The SessionEnd hook writes "
            f"to {LEDGER.relative_to(REPO_ROOT)} as sessions end.\n"
        )
        return

    tally = defaultdict(lambda: {PASS: 0, FAIL: 0, NA: 0})
    for row in rows:
        for name, verdict in row.get("rules", {}).items():
            tally[name][verdict] += 1

    complex_sessions = sum(1 for r in rows if r.get("complex"))
    print(
        f"  {CYAN}Sessions:{RESET} {len(rows)} ({complex_sessions} complex)   "
        f"{CYAN}Ledger:{RESET} {LEDGER.relative_to(REPO_ROOT)}"
    )
    print(f"\n  {'Rule':<44} {'Rate':>7}  {'n':>4}  Confidence")
    print(f"  {'-' * 44} {'-' * 7}  {'-' * 4}  ----------")

    weak = []
    for name, (label, confidence) in RULE_LABELS.items():
        counts = tally[name]
        judged = counts[PASS] + counts[FAIL]
        if judged == 0:
            print(f"  {label:<44} {'n/a':>7}  {0:>4}  {confidence}")
            continue
        rate = counts[PASS] / judged
        color = GREEN if rate >= 0.8 else YELLOW if rate >= LOW_ADHERENCE else RED
        print(f"  {label:<44} {color}{rate:>6.0%}{RESET}  {judged:>4}  {confidence}")
        if rate < LOW_ADHERENCE:
            weak.append(label)

    if weak:
        print(f"\n  {RED}Below 50%:{RESET} {', '.join(weak)}")
        print(
            "  A rule the model ignores is not a rule, it is context cost. Either\n"
            "  turn it into a deterministic hook or remove it (PRD Onda 3).\n"
        )
    else:
        print(f"\n  {GREEN}✔{RESET} No rule below 50%.\n")

    if len(rows) < 20:
        print(
            f"  {YELLOW}⚠{RESET} {len(rows)} of 20 sessions. The PRD gates the "
            "Slim-Core pruning on 20 real sessions.\n"
        )


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
