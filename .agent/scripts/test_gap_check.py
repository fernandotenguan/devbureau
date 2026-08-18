#!/usr/bin/env python3
"""
test_gap_check.py — DevBureau Test Gap Detector
Given the set of files changed in a diff, flags changed source files that have
no plausible corresponding test file also touched in the same diff. Deterministic
naming-convention match, not a coverage tool — it does not run the test suite,
it only checks whether a test file was touched alongside the source change.

Usage:
  python .agent/scripts/test_gap_check.py --diff            # files changed vs HEAD
  python .agent/scripts/test_gap_check.py <file> [<file>...]
  python .agent/scripts/test_gap_check.py --diff --strict   # exit 1 if any gap found
  python .agent/scripts/test_gap_check.py --diff --json

Exit codes: 0 = report produced (or --strict with zero gaps), 1 = usage error
or (--strict) at least one gap found.
"""

import argparse
import json
import re
import subprocess
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

SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}
TEST_MARKERS = {"test", "tests", "spec", "specs", "__tests__"}

# Stems that don't warrant a 1:1 test file by convention (barrels, entrypoints,
# static config) — flagging these would just be noise, not a real gap.
NON_TESTABLE_STEMS = {
    "index", "__init__", "main", "types", "constants", "config",
    "setup", "conftest", "styles",
}


def is_test_path(path: str) -> bool:
    parts = {p.lower() for p in Path(path).parts}
    stem = Path(path).stem.lower()
    if parts & TEST_MARKERS:
        return True
    return stem.endswith("_test") or stem.endswith(".test") or stem.endswith(".spec") or stem.startswith("test_")


def is_testable_source(path: str) -> bool:
    p = Path(path)
    if p.suffix.lower() not in SOURCE_EXTENSIONS:
        return False
    if is_test_path(path):
        return False
    if p.stem.lower() in NON_TESTABLE_STEMS:
        return False
    return True


def git_diff_targets(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=root, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def normalize_stem(stem: str) -> str:
    """Strips trailing test markers so 'foo_test' / 'foo.test' / 'test_foo' -> 'foo'."""
    s = stem.lower()
    s = re.sub(r"^test_", "", s)
    s = re.sub(r"(_test|\.test|\.spec|_spec)$", "", s)
    return s


def find_gaps(changed_files: list[str]) -> tuple[list[str], list[str]]:
    source_files = [f for f in changed_files if is_testable_source(f)]
    test_files = [f for f in changed_files if is_test_path(f) and Path(f).suffix.lower() in SOURCE_EXTENSIONS]
    test_stems = {normalize_stem(Path(t).stem) for t in test_files}

    gaps = []
    covered = []
    for src in source_files:
        stem = normalize_stem(Path(src).stem)
        if stem in test_stems:
            covered.append(src)
        else:
            gaps.append(src)
    return gaps, covered


def main() -> int:
    parser = argparse.ArgumentParser(description="Flags changed source files with no matching test file touched in the same diff.")
    parser.add_argument("files", nargs="*", help="Explicit changed files to check.")
    parser.add_argument("--diff", action="store_true", help="Use files changed vs HEAD.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any gap is found.")
    parser.add_argument("--json", action="store_true", help="Machine-readable output.")
    args = parser.parse_args()

    changed = list(args.files)
    if args.diff:
        changed.extend(git_diff_targets(REPO_ROOT))
    changed = sorted(set(f.replace("\\", "/") for f in changed))

    if not changed:
        print(f"{YELLOW}No target files given and --diff found nothing changed.{RESET}", file=sys.stderr)
        return 1

    gaps, covered = find_gaps(changed)

    if args.json:
        print(json.dumps({"gaps": gaps, "covered": covered}, indent=2))
        return 1 if (args.strict and gaps) else 0

    print(f"{BOLD}Test Gap Check{RESET} — {len(changed)} changed file(s) scanned")
    if covered:
        print(f"\n{GREEN}Covered ({len(covered)}):{RESET}")
        for f in covered:
            print(f"  ✔ {f}")
    if gaps:
        print(f"\n{RED}Gaps ({len(gaps)}) — changed with no test file touched in this diff:{RESET}")
        for f in gaps:
            print(f"  ✘ {f}")
    else:
        print(f"\n{GREEN}No gaps — every testable source change has a matching test file touched.{RESET}")

    if args.strict and gaps:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
