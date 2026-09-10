#!/usr/bin/env python3
"""
memory_rotate.py — Keeps the memory layer from growing without a ceiling.

docs/prd-2026-09/PRD_final_Gemini_10_09_26.md, A14. `pattern-mining-log.md` and
`benchmark-log.md` had grown past 100 KB each. Nothing is ever deleted: the
oldest dated entries move to `.agent/memory/archive/<name>.md` and stay
searchable through `memory_recall.py`, they just leave the default read path.

Only dated entries (`## YYYY-MM-DD — ...`) are eligible. The preamble and any
structural section, such as "Formato de entrada" or the literal
`## YYYY-MM-DD` template line, always stay in the active file.

Usage:
  python .agent/scripts/memory_rotate.py --check     # report, exit 1 if over
  python .agent/scripts/memory_rotate.py --dry-run   # show what would move
  python .agent/scripts/memory_rotate.py             # rotate
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

REPO_ROOT = Path(__file__).resolve().parents[2]
MEMORY_DIR = REPO_ROOT / ".agent" / "memory"
ARCHIVE_DIR = MEMORY_DIR / "archive"
INDEX_PATH = ARCHIVE_DIR / "INDEX.md"

THRESHOLD_BYTES = 50 * 1024
DATED_HEADING = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\b")
SECTION_START = re.compile(r"^##\s+")

GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def read(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(content)


def split_sections(text: str) -> tuple:
    """Returns (preamble, [(heading_line, full_section_text), ...])."""
    lines = text.split("\n")
    preamble, sections, current = [], [], None
    for line in lines:
        if SECTION_START.match(line):
            if current:
                sections.append(current)
            current = [line]
        elif current is not None:
            current.append(line)
        else:
            preamble.append(line)
    if current:
        sections.append(current)
    return "\n".join(preamble), [("\n".join(s)) for s in sections]


def entry_date(section: str) -> str:
    match = DATED_HEADING.match(section.split("\n", 1)[0])
    return match.group(1) if match else ""


def plan_rotation(path: Path) -> dict:
    """Which dated sections must move for this file to fit under the ceiling."""
    text = read(path)
    preamble, sections = split_sections(text)
    dated = [(i, entry_date(s)) for i, s in enumerate(sections) if entry_date(s)]

    # Oldest first; ties keep file order, so a same-day pair rotates predictably.
    dated.sort(key=lambda pair: (pair[1], pair[0]))

    size = len(text.encode("utf-8"))
    moving = []
    for index, _ in dated:
        if size <= THRESHOLD_BYTES:
            break
        section_size = len(sections[index].encode("utf-8")) + 1
        moving.append(index)
        size -= section_size

    return {
        "path": path,
        "preamble": preamble,
        "sections": sections,
        "moving": sorted(moving),
        "original_size": len(text.encode("utf-8")),
        "projected_size": size,
        "dated_total": len(dated),
    }


def apply_rotation(plan: dict) -> None:
    sections = plan["sections"]
    moving = set(plan["moving"])
    kept = [s for i, s in enumerate(sections) if i not in moving]
    archived = [sections[i] for i in plan["moving"]]

    body = "\n".join([plan["preamble"], *kept]) if kept else plan["preamble"]
    write(plan["path"], body.rstrip("\n") + "\n")

    stem = plan["path"].stem
    archive_path = ARCHIVE_DIR / f"{stem}.md"
    header = (
        f"# {stem} — archive\n\n"
        f"> Entries rotated out of `.agent/memory/{stem}.md` by `memory_rotate.py` "
        f"to keep the active file under {THRESHOLD_BYTES // 1024} KB. Nothing was "
        f"deleted; `memory_recall.py` still searches this file.\n"
    )
    existing = read(archive_path) if archive_path.exists() else header
    write(
        archive_path,
        existing.rstrip("\n") + "\n\n" + "\n".join(archived).rstrip("\n") + "\n",
    )


def archive_summary() -> list:
    if not ARCHIVE_DIR.exists():
        return []
    rows = []
    for path in sorted(ARCHIVE_DIR.glob("*.md")):
        if path.name == "INDEX.md":
            continue
        text = read(path)
        _, sections = split_sections(text)
        dates = sorted(d for d in (entry_date(s) for s in sections) if d)
        rows.append(
            {
                "name": path.name,
                "entries": len(dates),
                "first": dates[0] if dates else "—",
                "last": dates[-1] if dates else "—",
                "kb": len(text.encode("utf-8")) // 1024,
            }
        )
    return rows


def write_index() -> None:
    rows = archive_summary()
    if not rows:
        return
    lines = [
        "# Memory Archive — Index",
        "",
        "> Rotated by `memory_rotate.py` when an active memory file passes "
        f"{THRESHOLD_BYTES // 1024} KB. Nothing here was deleted, and "
        "`memory_recall.py` searches these files alongside the active ones.",
        "",
        f"_Last updated: {date.today().isoformat()}_",
        "",
        "| File | Entries | Oldest | Newest | Size |",
        "|---|---:|---|---|---:|",
    ]
    lines += [
        f"| `{r['name']}` | {r['entries']} | {r['first']} | {r['last']} | {r['kb']} KB |"
        for r in rows
    ]
    write(INDEX_PATH, "\n".join(lines) + "\n")


def oversized_files() -> list:
    if not MEMORY_DIR.exists():
        return []
    return [
        p for p in sorted(MEMORY_DIR.glob("*.md")) if p.stat().st_size > THRESHOLD_BYTES
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Report only; exit 1 if any file is over"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show the plan without writing"
    )
    args = parser.parse_args()

    print(f"\n{BOLD}🗄️  DevBureau — Memory Rotation{RESET}")
    over = oversized_files()

    if not over:
        print(
            f"  {GREEN}✔{RESET} No active memory file above "
            f"{THRESHOLD_BYTES // 1024} KB.\n"
        )
        sys.exit(0)

    if args.check:
        print(f"  {YELLOW}⚠{RESET} Over the ceiling ({len(over)}):")
        for path in over:
            print(f"    - {path.name}: {path.stat().st_size // 1024} KB")
        print("  Run: python .agent/scripts/memory_rotate.py\n")
        sys.exit(1)

    for path in over:
        plan = plan_rotation(path)
        if not plan["moving"]:
            print(
                f"  {YELLOW}⚠{RESET} {path.name}: {plan['original_size'] // 1024} KB but "
                "no dated entry can be rotated (all content is structural)."
            )
            continue
        verb = "Would move" if args.dry_run else "Moved"
        print(
            f"  {CYAN}{path.name}{RESET}: {verb} {len(plan['moving'])} of "
            f"{plan['dated_total']} dated entries "
            f"({plan['original_size'] // 1024} KB -> {plan['projected_size'] // 1024} KB)"
        )
        if not args.dry_run:
            apply_rotation(plan)

    if not args.dry_run:
        write_index()
        print(f"  {GREEN}✔{RESET} Archive index: {INDEX_PATH.relative_to(REPO_ROOT)}")
    print()


if __name__ == "__main__":
    main()
