#!/usr/bin/env python3
"""
doc_drift_check.py — DevBureau Documentation Drift Detector
Scans the kit's own reference docs for backtick-quoted file paths and script
names, and verifies each one still exists on disk. Catches the case where a
script/agent/skill is renamed or removed but a doc still points at the old
name — the same failure mode the anti-hallucination "VERIFY:" convention
targets, applied to the docs themselves instead of generated code.

Usage:
  python .agent/scripts/doc_drift_check.py                  # scans default doc set
  python .agent/scripts/doc_drift_check.py --files a.md b.md
  python .agent/scripts/doc_drift_check.py --strict         # exit 1 if any dead ref found
  python .agent/scripts/doc_drift_check.py --json

Exit codes: 0 = report produced (or --strict with zero dead refs), 1 = usage
error or (--strict) at least one dead reference found. Advisory by default.
"""

import argparse
import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

REPO_ROOT = Path(__file__).resolve().parents[2]

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

DEFAULT_DOCS = [
    ".agent/rules/DEVBUREAU.md",
    ".agent/ARCHITECTURE.md",
    ".agent/SCRIPTS_REGISTRY.md",
    "README.md",
    "README_pt-BR.md",
    "KIT_MASTER_RULES.md",
]

# Matches backtick-quoted path-like tokens, e.g. `.agent/scripts/doctor.py`,
# `blast_radius.py`, `.agent/agents/backend-specialist.md`.
PATH_TOKEN = re.compile(r"`([A-Za-z0-9_\-./]+\.(?:py|md|json|yaml|yml|js|mjs))`")

EXCLUDED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    ".next", ".turbo", ".cache", ".pytest_cache", ".ruff_cache", "coverage",
    "graphify-out",
}

# Names that are inherently generic (appear identically in every skill dir) or
# document a filename an EXTERNAL tool writes / a DYNAMIC per-instance file
# this repo never holds statically — flagging these would be noise, not a
# real drift signal. Keep this list small and justified, not a loophole.
KNOWN_NON_REPO_REFS = {
    "SKILL.md",         # every skill directory has one; too generic to resolve to a single file
    "state.json",       # per-squad-instance runtime file (squads/<name>/state.json), not static
    ".gateguard.yml",   # written by the third-party gateguard tool into the user's project, not this repo
}


def extract_references(text: str) -> set[str]:
    return set(PATH_TOKEN.findall(text))


def build_basename_index(root: Path) -> dict[str, list[Path]]:
    """Maps a bare filename -> every path in the repo with that name, so a doc
    can reference a file without its full/exact directory prefix without being
    flagged as dead (prose often drops the prefix; the file still has to exist
    SOMEWHERE for the reference to be real)."""
    index: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        index.setdefault(path.name, []).append(path)
    return index


def resolve_reference(ref: str, basename_index: dict[str, list[Path]]) -> bool:
    """True if the reference resolves to a real file: as a direct repo-relative
    path, or as a bare/partial filename that exists somewhere in the repo."""
    if ref in KNOWN_NON_REPO_REFS:
        return True
    direct = REPO_ROOT / ref
    if direct.exists():
        return True
    basename = Path(ref).name
    return basename in basename_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Flags doc references to files that no longer exist on disk.")
    parser.add_argument("--files", nargs="*", help="Doc files to scan (repo-relative). Defaults to the kit's core reference docs.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any dead reference is found.")
    parser.add_argument("--json", action="store_true", help="Machine-readable output.")
    args = parser.parse_args()

    targets = args.files if args.files else DEFAULT_DOCS
    basename_index = build_basename_index(REPO_ROOT)
    report = []

    for rel_path in targets:
        doc_path = REPO_ROOT / rel_path
        if not doc_path.exists():
            print(f"{YELLOW}Skipping {rel_path}: not found.{RESET}", file=sys.stderr)
            continue
        text = doc_path.read_text(encoding="utf-8", errors="ignore")
        refs = extract_references(text)
        dead = sorted(r for r in refs if not resolve_reference(r, basename_index))
        report.append({"doc": rel_path, "references_checked": len(refs), "dead_references": dead})

    if args.json:
        print(json.dumps(report, indent=2))
        total_dead = sum(len(r["dead_references"]) for r in report)
        return 1 if (args.strict and total_dead) else 0

    total_dead = 0
    print(f"{BOLD}Doc Drift Check{RESET} — {len(report)} doc(s) scanned\n")
    for entry in report:
        dead = entry["dead_references"]
        total_dead += len(dead)
        if dead:
            print(f"{RED}{entry['doc']}{RESET} — {len(dead)} dead reference(s) of {entry['references_checked']} checked:")
            for ref in dead:
                print(f"    ✘ {ref}")
        else:
            print(f"{GREEN}{entry['doc']}{RESET} — {entry['references_checked']} reference(s), all resolve ✔")

    print(f"\n{BOLD}Total dead references: {total_dead}{RESET}")

    if args.strict and total_dead:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
