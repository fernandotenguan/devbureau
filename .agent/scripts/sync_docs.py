#!/usr/bin/env python3
"""
sync_docs.py — Recount agents/skills/workflows from disk and update the docs
that quote those numbers (README badges, ARCHITECTURE.md headers and stats).

Adding or removing an agent, skill or workflow makes TestDocsSync fail until
four files are edited by hand. Counting files is deterministic work, so it
belongs in a script, not in an agent's reasoning budget.

Usage:
  python .agent/scripts/sync_docs.py            # rewrite the docs in place
  python .agent/scripts/sync_docs.py --check    # report only, exit 1 if stale
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
AGENT_DIR = REPO_ROOT / ".agent"
READMES = ["README.md", "README_pt-BR.md"]
ARCHITECTURE = AGENT_DIR / "ARCHITECTURE.md"

GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def read_text(path: Path) -> str:
    """newline="" keeps CRLF/LF exactly as found — this script edits numbers,
    it must never rewrite a whole file's line endings as a side effect."""
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text(path: Path, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(content)


class DocSyncError(RuntimeError):
    """A doc could not be updated — the caller decides whether that blocks."""


def disk_counts() -> dict[str, int]:
    agents = AGENT_DIR / "agents"
    skills = AGENT_DIR / "skills"
    workflows = AGENT_DIR / "workflows"
    return {
        "Agents": len(list(agents.glob("*.md"))) if agents.exists() else 0,
        "Skills": len([d for d in skills.iterdir() if d.is_dir()])
        if skills.exists()
        else 0,
        "Workflows": len(list(workflows.glob("*.md"))) if workflows.exists() else 0,
    }


def package_version() -> str:
    package_json = REPO_ROOT / "package.json"
    if not package_json.exists():
        raise DocSyncError("package.json not found — cannot resolve the version badge")
    return json.loads(package_json.read_text(encoding="utf-8"))["version"]


def sync_readme(path: Path, counts: dict[str, int], version: str) -> list[str]:
    """Rewrite the shields.io badge numbers. Returns a list of change labels."""
    content = read_text(path)
    original = content
    changes: list[str] = []

    for kind, count in counts.items():
        # badge/Agents-23-green  ->  badge/Agents-<disk count>-green
        pattern = re.compile(rf"(badge/{kind}-)(\d+)(-)")
        found = pattern.search(content)
        if found and found.group(2) != str(count):
            changes.append(f"{kind}: {found.group(2)} -> {count}")
        content = pattern.sub(rf"\g<1>{count}\g<3>", content)

    version_pattern = re.compile(r"(badge/DevBureau-v)([\d.]+?)(-)")
    found = version_pattern.search(content)
    if found and found.group(2) != version:
        changes.append(f"version: {found.group(2)} -> {version}")
    content = version_pattern.sub(rf"\g<1>{version}\g<3>", content)

    if content != original:
        write_text(path, content)
    return changes


def sync_architecture(counts: dict[str, int]) -> list[str]:
    """Rewrite the section headers and the statistics table."""
    content = read_text(ARCHITECTURE)
    original = content
    changes: list[str] = []

    for kind, count in counts.items():
        # "## 🤖 Agents (23)" — the emoji varies, so anchor on the word.
        header = re.compile(rf"(^##[^\n]*\b{kind} \()(\d+)(\))", re.MULTILINE)
        found = header.search(content)
        if found and found.group(2) != str(count):
            changes.append(f"{kind} header: {found.group(2)} -> {count}")
        content = header.sub(rf"\g<1>{count}\g<3>", content)

        # "| **Total Agents**     | 23   |" — keep any trailing note after the
        # number (e.g. "78 (+ 10 nested under `game-development`)") intact.
        stats = re.compile(rf"(\*\*Total {kind}\*\*\s*\|\s*)(\d+)")
        found = stats.search(content)
        if found and found.group(2) != str(count):
            changes.append(f"Total {kind}: {found.group(2)} -> {count}")
        content = stats.sub(rf"\g<1>{count}", content)

    if content != original:
        write_text(ARCHITECTURE, content)
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift without writing; exit 1 if any doc is stale",
    )
    args = parser.parse_args()

    print(f"\n{BOLD}📚 DevBureau — Doc Sync{RESET}")
    counts = disk_counts()
    version = package_version()
    print(
        f"  {CYAN}Disk:{RESET} {counts['Agents']} agents, {counts['Skills']} skills, "
        f"{counts['Workflows']} workflows, v{version}"
    )

    if args.check:
        # Compare without writing by snapshotting, syncing, then restoring.
        targets = [REPO_ROOT / name for name in READMES if (REPO_ROOT / name).exists()]
        if ARCHITECTURE.exists():
            targets.append(ARCHITECTURE)
        snapshots = {p: read_text(p) for p in targets}
        drift: list[str] = []
        for name in READMES:
            path = REPO_ROOT / name
            if path.exists():
                drift += [f"{name}: {c}" for c in sync_readme(path, counts, version)]
        if ARCHITECTURE.exists():
            drift += [f"ARCHITECTURE.md: {c}" for c in sync_architecture(counts)]
        for path, text in snapshots.items():
            write_text(path, text)

        if drift:
            print(f"  {YELLOW}⚠{RESET} Out of sync ({len(drift)}):")
            for item in drift:
                print(f"    - {item}")
            print("  Run: python .agent/scripts/sync_docs.py\n")
            sys.exit(1)
        print(f"  {GREEN}✔{RESET} Docs already match disk.\n")
        sys.exit(0)

    all_changes: list[str] = []
    for name in READMES:
        path = REPO_ROOT / name
        if not path.exists():
            print(f"  {YELLOW}⚠{RESET} {name} not found — skipped")
            continue
        changes = sync_readme(path, counts, version)
        all_changes += [f"{name}: {c}" for c in changes]

    if ARCHITECTURE.exists():
        all_changes += [f"ARCHITECTURE.md: {c}" for c in sync_architecture(counts)]
    else:
        print(f"  {YELLOW}⚠{RESET} .agent/ARCHITECTURE.md not found — skipped")

    if not all_changes:
        print(f"  {GREEN}✔{RESET} Already in sync — nothing to write.\n")
        sys.exit(0)

    print(f"  {GREEN}✔{RESET} Updated ({len(all_changes)}):")
    for item in all_changes:
        print(f"    - {item}")
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
