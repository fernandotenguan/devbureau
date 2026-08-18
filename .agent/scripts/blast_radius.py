#!/usr/bin/env python3
"""
blast_radius.py — DevBureau File Dependency Awareness Checker
Given one or more changed files, finds which other files reference them
(imports, requires, relative paths, or plain-text mentions), so "File
Dependency Awareness" (DEVBUREAU.md TIER 0) is backed by a real scan instead
of the agent trying to recall dependents from memory.

Usage:
  python .agent/scripts/blast_radius.py <file> [<file> ...]
  python .agent/scripts/blast_radius.py --diff          # scan files changed vs HEAD
  python .agent/scripts/blast_radius.py <file> --json    # machine-readable output

Exit codes: 0 = report produced, 1 = usage/input error (no git repo, no
targets, target not found). This is an advisory report, not a pass/fail
gate — a nonzero reference count is not itself a failure.
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
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Directories never worth scanning: dependency trees, build output, VCS internals.
EXCLUDED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    ".next", ".turbo", ".cache", ".pytest_cache", "coverage", "graphify-out",
}

# Text extensions worth searching for references. Binary/asset files are
# skipped — a blast radius on those would only ever be filename mentions.
SEARCHABLE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".md", ".mdx", ".json", ".yml", ".yaml", ".toml",
}

# Filenames too generic to search for on their own — the parent directory
# name is the meaningful identity instead (every skill has a SKILL.md).
GENERIC_STEMS = {"index", "__init__", "main", "skill", "readme"}


def resolve_search_term(target: Path) -> tuple[str, str]:
    """Returns (search_term, kind) — kind explains what the term represents."""
    stem = target.stem.lower()
    if stem in GENERIC_STEMS:
        return target.parent.name, "parent directory (generic filename)"
    return target.stem, "filename stem"


def iter_searchable_files(root: Path):
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in SEARCHABLE_EXTENSIONS:
            continue
        yield path


def find_references(target: Path, root: Path) -> list[dict]:
    term, _ = resolve_search_term(target)
    pattern = re.compile(r"\b" + re.escape(term) + r"\b")
    target_resolved = target.resolve()
    references: list[dict] = []

    for candidate in iter_searchable_files(root):
        if candidate.resolve() == target_resolved:
            continue
        try:
            text = candidate.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                references.append({
                    "file": str(candidate.relative_to(root)).replace("\\", "/"),
                    "line": lineno,
                    "snippet": line.strip()[:160],
                })
    return references


def classify_risk(target: Path, reference_count: int) -> str:
    in_agent = ".agent" in target.parts
    if reference_count >= 10 or (in_agent and reference_count >= 5):
        return "HIGH"
    if reference_count >= 3 or in_agent:
        return "MEDIUM"
    return "LOW"


# Path fragments that mark a file as touching a critical domain — auth, money,
# schema migrations, secrets. A change here deserves more verification depth
# regardless of how many other files reference it (DEVBUREAU.md, "Verification
# depth matches change risk").
CRITICALITY_KEYWORDS = {
    "auth", "login", "senha", "password", "session", "token",
    "payment", "pagamento", "checkout", "billing", "invoice", "fatura",
    "migration", "migração", "migrations", "schema",
    "secret", "credential", "credencial", ".env",
}


def path_criticality(target: Path) -> list[str]:
    haystack = str(target).lower().replace("\\", "/")
    return sorted(kw for kw in CRITICALITY_KEYWORDS if kw in haystack)


def git_churn(target: Path, root: Path) -> int:
    """Number of commits touching this file in the last 90 days — a proxy for
    how often this file has historically needed a follow-up fix. 0 on any git
    failure (shallow clone, file never committed) rather than raising."""
    result = subprocess.run(
        ["git", "log", "--since=90.days", "--oneline", "--", str(target.relative_to(root))],
        cwd=root, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def suggest_verification_depth(risk_score: int) -> str:
    if risk_score >= 6:
        return "Written failure scenario (race/retry/partial-failure) before calling this done."
    if risk_score >= 3:
        return "Manual trace through the changed path with real inputs."
    return "Syntax/type check is likely sufficient."


def compute_diff_risk(target: Path, root: Path, reference_count: int) -> dict:
    criticality = path_criticality(target)
    churn = git_churn(target, root)
    # Score: reference fan-out (capped) + 3 per critical-domain keyword hit + churn (capped).
    score = min(reference_count, 10) + 3 * len(criticality) + min(churn, 5)
    return {
        "reference_count": reference_count,
        "criticality_keywords": criticality,
        "commits_last_90d": churn,
        "risk_score": score,
        "suggested_verification": suggest_verification_depth(score),
    }


def git_diff_targets(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=root, capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reports which files reference a given file before you change it."
    )
    parser.add_argument("files", nargs="*", help="File paths (relative to repo root) to check.")
    parser.add_argument("--diff", action="store_true", help="Use files changed vs HEAD as targets.")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON output.")
    parser.add_argument("--risk", action="store_true",
                         help="Add a composite diff-risk score (reference fan-out + critical-domain keywords + "
                              "90-day commit churn) and a suggested verification depth per target.")
    args = parser.parse_args()

    targets = list(args.files)
    if args.diff:
        targets.extend(git_diff_targets(REPO_ROOT))
    targets = sorted(set(targets))

    if not targets:
        print(f"{RED}No target files given and --diff found nothing changed.{RESET}", file=sys.stderr)
        return 1

    report = []
    for rel_path in targets:
        target = REPO_ROOT / rel_path
        if not target.exists() or not target.is_file():
            print(f"{RED}Skipping {rel_path}: not found under {REPO_ROOT}{RESET}", file=sys.stderr)
            continue
        term, term_kind = resolve_search_term(target)
        refs = find_references(target, REPO_ROOT)
        risk = classify_risk(target, len(refs))
        entry = {
            "target": rel_path.replace("\\", "/"),
            "search_term": term,
            "search_term_kind": term_kind,
            "reference_count": len(refs),
            "risk": risk,
            "references": refs,
        }
        if args.risk:
            entry["diff_risk"] = compute_diff_risk(target, REPO_ROOT, len(refs))
        report.append(entry)

    if not report:
        print(f"{RED}No valid target files to scan.{RESET}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    risk_color = {"HIGH": RED, "MEDIUM": YELLOW, "LOW": GREEN}
    for entry in report:
        color = risk_color[entry["risk"]]
        print(f"\n{BOLD}{entry['target']}{RESET}  (search term: {CYAN}{entry['search_term']}{RESET} — {entry['search_term_kind']})")
        print(f"  Risk: {color}{entry['risk']}{RESET}  |  Referenced by {entry['reference_count']} file(s)")
        if "diff_risk" in entry:
            dr = entry["diff_risk"]
            crit = ", ".join(dr["criticality_keywords"]) or "none"
            print(f"  Diff risk score: {BOLD}{dr['risk_score']}{RESET}  "
                  f"(critical-domain keywords: {crit}; commits last 90d: {dr['commits_last_90d']})")
            print(f"  Suggested verification: {dr['suggested_verification']}")
        for ref in entry["references"][:15]:
            print(f"    {ref['file']}:{ref['line']}  {ref['snippet']}")
        if entry["reference_count"] > 15:
            print(f"    ... and {entry['reference_count'] - 15} more (use --json for the full list)")

    print(f"\n{BOLD}Scanned {len(report)} target(s) against {REPO_ROOT}{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
