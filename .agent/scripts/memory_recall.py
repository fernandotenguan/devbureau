#!/usr/bin/env python3
"""
memory_recall.py — DevBureau Memory Recall & Decay Tracker
Searches lessons.md/gotchas.md by keyword (matching the "Gatilho" field convention
already used in both files), and flags entries nobody has recalled in a long time
so the memory layer doesn't just grow forever without anyone checking whether an
entry is still earning its place.

Usage:
  python .agent/scripts/memory_recall.py recall <keyword>            # search by trigger/content
  python .agent/scripts/memory_recall.py stale [--days N]            # entries never recalled, N+ days old (default 180)
  python .agent/scripts/memory_recall.py mark <file> <entry-date> <title-slug>  # record a recall

Exit codes: 0 = report produced, 1 = usage/input error. Advisory tool, not a gate.
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

REPO_ROOT = Path(__file__).resolve().parents[2]
MEMORY_DIR = REPO_ROOT / ".agent" / "memory"
DEFAULT_FILES = ["lessons.md", "gotchas.md"]

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

ENTRY_HEADING = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — (.+)$")
FIELD_LINE = re.compile(r"^\*\*([^*:]+):\*\*\s*(.*)$")


def split_entries(text: str) -> list[dict]:
    """Splits a memory file into dated entries (## YYYY-MM-DD — Title blocks)."""
    lines = text.splitlines()
    entries = []
    current = None
    for line in lines:
        heading = ENTRY_HEADING.match(line)
        if heading:
            if current:
                entries.append(current)
            current = {
                "date": heading.group(1),
                "title": heading.group(2).strip(),
                "fields": {},
                "body_lines": [line],
            }
            continue
        if current is not None:
            current["body_lines"].append(line)
            field = FIELD_LINE.match(line.strip())
            if field:
                key = field.group(1).strip()
                current["fields"].setdefault(key, field.group(2).strip())
    if current:
        entries.append(current)
    return entries


def load_all_entries() -> list[tuple[Path, dict]]:
    result = []
    for name in DEFAULT_FILES:
        path = MEMORY_DIR / name
        if not path.exists():
            continue
        for entry in split_entries(path.read_text(encoding="utf-8", errors="ignore")):
            result.append((path, entry))
    return result


def cmd_recall(keyword: str) -> int:
    keyword_lower = keyword.lower()
    matches = []
    for path, entry in load_all_entries():
        haystack = " ".join(
            [entry["title"], entry["fields"].get("Gatilho", ""),
             entry["fields"].get("Padrão identificado", ""),
             entry["fields"].get("Sintoma", "")]
        ).lower()
        if keyword_lower in haystack:
            matches.append((path, entry))

    if not matches:
        print(f"{YELLOW}No entries match '{keyword}'.{RESET}")
        return 0

    print(f"{BOLD}{len(matches)} match(es) for '{keyword}':{RESET}\n")
    for path, entry in matches:
        print(f"{CYAN}{path.name}{RESET} — {BOLD}{entry['date']} — {entry['title']}{RESET}")
        gatilho = entry["fields"].get("Gatilho")
        if gatilho:
            print(f"  Gatilho: {gatilho}")
        confianca = entry["fields"].get("Confiança")
        if confianca:
            print(f"  Confiança: {confianca}")
        ultima = entry["fields"].get("Última recuperação")
        print(f"  Última recuperação: {ultima or '(nunca registrada)'}")
        print()
    return 0


def _days_since(date_str: str) -> int | None:
    try:
        entry_date = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None
    return (datetime.now(timezone.utc) - entry_date).days


def cmd_stale(days: int) -> int:
    stale_entries = []
    for path, entry in load_all_entries():
        age = _days_since(entry["date"])
        if age is None or age < days:
            continue
        if "Última recuperação" not in entry["fields"]:
            stale_entries.append((path, entry, age))

    if not stale_entries:
        print(f"{GREEN}No entries older than {days} days without a recorded recall.{RESET}")
        return 0

    print(f"{BOLD}{len(stale_entries)} entr{'y' if len(stale_entries) == 1 else 'ies'} "
          f"never recalled, {days}+ days old:{RESET}\n")
    for path, entry, age in sorted(stale_entries, key=lambda x: -x[2]):
        print(f"  {YELLOW}{path.name}{RESET} — {entry['date']} ({age}d) — {entry['title']}")
    print(f"\n{BOLD}Review these:{RESET} still useful (start recording recalls with "
          f"'mark') or safe to fold/remove via config-gc.")
    return 0


def cmd_mark(file_name: str, entry_date: str, title_slug: str) -> int:
    path = MEMORY_DIR / file_name
    if not path.exists():
        print(f"{RED}File not found: {path}{RESET}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines(keepends=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    target_idx = None
    for i, line in enumerate(lines):
        heading = ENTRY_HEADING.match(line.rstrip("\n"))
        if heading and heading.group(1) == entry_date and title_slug.lower() in heading.group(2).lower():
            target_idx = i
            break

    if target_idx is None:
        print(f"{RED}No entry found matching date={entry_date} title contains '{title_slug}' in {file_name}{RESET}", file=sys.stderr)
        return 1

    # Find end of this entry block (next "## " heading or EOF).
    end_idx = len(lines)
    for j in range(target_idx + 1, len(lines)):
        if lines[j].startswith("## "):
            end_idx = j
            break

    block = lines[target_idx:end_idx]
    updated = False
    for k, line in enumerate(block):
        if line.strip().startswith("**Última recuperação:**"):
            block[k] = f"**Última recuperação:** {today}\n"
            updated = True
            break

    if not updated:
        # Insert right after the heading line.
        block.insert(1, f"**Última recuperação:** {today}\n")

    lines[target_idx:end_idx] = block
    path.write_text("".join(lines), encoding="utf-8")
    print(f"{GREEN}Recorded recall ({today}) for '{title_slug}' in {file_name}.{RESET}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Search and track recall of DevBureau memory entries.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_recall = sub.add_parser("recall", help="Search entries by keyword.")
    p_recall.add_argument("keyword")

    p_stale = sub.add_parser("stale", help="List entries never recalled, N+ days old.")
    p_stale.add_argument("--days", type=int, default=180)

    p_mark = sub.add_parser("mark", help="Record a recall timestamp on an entry.")
    p_mark.add_argument("file", choices=DEFAULT_FILES)
    p_mark.add_argument("entry_date", help="YYYY-MM-DD of the entry heading")
    p_mark.add_argument("title_slug", help="Substring of the entry title to identify it")

    args = parser.parse_args()

    if not MEMORY_DIR.exists():
        print(f"{RED}Memory directory not found: {MEMORY_DIR}{RESET}", file=sys.stderr)
        return 1

    if args.command == "recall":
        return cmd_recall(args.keyword)
    if args.command == "stale":
        return cmd_stale(args.days)
    if args.command == "mark":
        return cmd_mark(args.file, args.entry_date, args.title_slug)
    return 1


if __name__ == "__main__":
    sys.exit(main())
