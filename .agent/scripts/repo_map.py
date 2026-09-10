#!/usr/bin/env python3
"""
repo_map.py — A compact symbol map of a codebase, so an agent can find the
right file on the first try instead of spending 10 to 20 exploratory tool
calls on list/grep/read.

docs/prd-2026-09/PRD_final_Gemini_10_09_26.md, E2.1. Python is parsed with the stdlib `ast`;
TypeScript/JavaScript with targeted regex, because the kit stays dependency
free and a full TS parser is not worth a runtime dependency here. Files are
ranked by how many other files import them, so the most connected modules
survive the token budget.

Known limit of the regex path: TypeScript/JavaScript classes are listed by
name only, without their methods, and only `export`ed top-level declarations
are seen. Python, parsed properly, expands class methods.

Usage:
  python .agent/scripts/repo_map.py                 # current directory
  python .agent/scripts/repo_map.py src --budget 800
  python .agent/scripts/repo_map.py --json
"""

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

SKIP_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    "venv",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    "coverage",
    "vendor",
}

PY_SUFFIXES = {".py"}
TS_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".mjs"}

# chars-per-token heuristic, same one token_footprint.py uses: good enough to
# hold a budget, not meant to match a provider's tokenizer.
CHARS_PER_TOKEN = 4
DEFAULT_BUDGET_TOKENS = 1024
MAX_MEMBERS = 8
MAX_FILE_BYTES = 400_000

TS_EXPORTED = re.compile(
    r"^\s*export\s+(?:default\s+)?(?:async\s+)?"
    r"(?:function|class|const|let|var|interface|type|enum)\s+([A-Za-z_$][\w$]*)",
    re.MULTILINE,
)
TS_ROUTE = re.compile(
    r"\b(?:app|router|server)\.(get|post|put|patch|delete)\s*\(\s*[\"'`]([^\"'`]+)",
    re.IGNORECASE,
)
IMPORT_TOKEN = re.compile(r"""(?:from|import|require)\s*\(?\s*["']?([\w./@-]+)""")

CYAN = "\033[96m"
DIM = "\033[2m"
RESET = "\033[0m"
BOLD = "\033[1m"


# ── collection ────────────────────────────────────────────────────────────────


def iter_source_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            path = Path(current) / name
            if path.suffix in PY_SUFFIXES or path.suffix in TS_SUFFIXES:
                yield path


def read_source(path: Path) -> str:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def python_symbols(source: str) -> list:
    """Top-level classes (with their methods) and functions, in file order."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return []

    symbols = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = [
                child.name
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                and not child.name.startswith("_")
            ]
            symbols.append({"name": node.name, "kind": "class", "members": methods})
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                symbols.append({"name": node.name, "kind": "function", "members": []})
    return symbols


def ts_symbols(source: str) -> list:
    symbols = [
        {"name": name, "kind": "export", "members": []}
        for name in dict.fromkeys(TS_EXPORTED.findall(source))
    ]
    routes = [
        f"{verb.upper()} {path}"
        for verb, path in dict.fromkeys(TS_ROUTE.findall(source))
    ]
    if routes:
        symbols.append({"name": "routes", "kind": "routes", "members": routes})
    return symbols


def imported_tokens(source: str) -> set:
    """Bare module names referenced by imports, used only for ranking."""
    tokens = set()
    for raw in IMPORT_TOKEN.findall(source):
        tokens.add(Path(raw.rstrip("/")).name.split(".")[0])
    return tokens


def collect(root: Path) -> list:
    entries = []
    for path in iter_source_files(root):
        source = read_source(path)
        if not source.strip():
            continue
        parser = python_symbols if path.suffix in PY_SUFFIXES else ts_symbols
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "stem": path.stem,
                "symbols": parser(source),
                "imports": imported_tokens(source),
            }
        )
    return entries


def rank(entries: list) -> list:
    """Most-imported files first; ties broken by how much they define.

    A cheap stand-in for the graph ranking Aider does: enough to keep the
    modules everything else depends on inside the budget.
    """
    inbound = {}
    for entry in entries:
        for token in entry["imports"]:
            inbound[token] = inbound.get(token, 0) + 1

    for entry in entries:
        entry["inbound"] = inbound.get(entry["stem"], 0)
        entry.pop("imports", None)

    return sorted(
        entries,
        key=lambda e: (-e["inbound"], -len(e["symbols"]), e["path"]),
    )


# ── rendering ─────────────────────────────────────────────────────────────────


def render_entry(entry: dict) -> str:
    parts = []
    for symbol in entry["symbols"]:
        if symbol["members"]:
            members = symbol["members"][:MAX_MEMBERS]
            suffix = ", …" if len(symbol["members"]) > len(members) else ""
            if symbol["kind"] == "routes":
                parts.append(f"[{', '.join(members)}{suffix}]")
            else:
                parts.append(f"{symbol['name']} [{', '.join(members)}{suffix}]")
        else:
            parts.append(symbol["name"])
    return f"{entry['path']}: {', '.join(parts)}" if parts else ""


def render(entries: list, budget_tokens: int) -> tuple:
    budget_chars = budget_tokens * CHARS_PER_TOKEN
    lines, used, shown = [], 0, 0
    for entry in entries:
        line = render_entry(entry)
        if not line:
            continue
        if used + len(line) + 1 > budget_chars:
            break
        lines.append(line)
        used += len(line) + 1
        shown += 1
    return lines, shown, used


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Project directory")
    parser.add_argument(
        "--budget",
        type=int,
        default=DEFAULT_BUDGET_TOKENS,
        help=f"Approximate token ceiling for the map (default {DEFAULT_BUDGET_TOKENS})",
    )
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        sys.exit(1)

    entries = rank(collect(root))
    lines, shown, used = render(entries, args.budget)
    with_symbols = sum(1 for e in entries if e["symbols"])

    if args.json:
        print(
            json.dumps(
                {
                    "root": str(root),
                    "files_with_symbols": with_symbols,
                    "files_shown": shown,
                    "approx_tokens": used // CHARS_PER_TOKEN,
                    "entries": entries[:shown],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return

    print(f"\n{BOLD}🗺️  Repo map — {root.name}{RESET}")
    print(f"{DIM}ranked by inbound imports; ~{used // CHARS_PER_TOKEN} tokens{RESET}\n")
    for line in lines:
        path, _, symbols = line.partition(": ")
        print(f"  {CYAN}{path}{RESET}: {symbols}")

    hidden = with_symbols - shown
    if hidden > 0:
        print(
            f"\n{DIM}  … {hidden} more file(s) with symbols omitted to stay under "
            f"the {args.budget}-token budget. Raise it with --budget.{RESET}"
        )
    print()


if __name__ == "__main__":
    main()
