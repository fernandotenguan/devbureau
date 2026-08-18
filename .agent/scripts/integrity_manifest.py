#!/usr/bin/env python3
"""
integrity_manifest.py — DevBureau Rule Integrity Manifest
Generates and verifies a SHA-256 manifest of the kit's P0/agent/workflow layer
(.agent/rules/, .agent/agents/, .agent/workflows/). DevBureau's own source repo
already has git history to detect changes to these files — the real value is
for a DERIVED project that received a copy of .agent/ and has no way to tell
whether its local rules were edited (by hand, by a bad merge, or by injected
content) since the copy was made. `generate` is run by kit maintainers before
a release; `verify` is run by (or for) a derived project against that shipped
baseline.

Usage:
  python .agent/scripts/integrity_manifest.py generate
  python .agent/scripts/integrity_manifest.py verify
  python .agent/scripts/integrity_manifest.py verify --json

Exit codes: 0 = generated, or verified with no drift. 1 = usage error, missing
baseline, or (verify) drift found. Verify's nonzero exit is informational for
CI-style use — a derived project customizing its own rules on purpose is
legitimate; this is a "did anything change" signal, not a correctness gate.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / ".agent" / "INTEGRITY_MANIFEST.json"
WATCHED_DIRS = [".agent/rules", ".agent/agents", ".agent/workflows"]

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def collect_files() -> dict[str, str]:
    """Maps repo-relative path -> sha256 hex digest, for every file under the watched dirs."""
    hashes: dict[str, str] = {}
    for rel_dir in WATCHED_DIRS:
        base = REPO_ROOT / rel_dir
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_dir():
                continue
            rel = path.relative_to(REPO_ROOT).as_posix()
            hashes[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def cmd_generate() -> int:
    hashes = collect_files()
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "watched_dirs": WATCHED_DIRS,
        "file_count": len(hashes),
        "files": hashes,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    print(f"{GREEN}Generated manifest for {len(hashes)} file(s) → {MANIFEST_PATH.relative_to(REPO_ROOT)}{RESET}")
    return 0


def cmd_verify(as_json: bool) -> int:
    if not MANIFEST_PATH.exists():
        msg = f"No baseline manifest found at {MANIFEST_PATH.relative_to(REPO_ROOT)} — run 'generate' first."
        if as_json:
            print(json.dumps({"error": msg}))
        else:
            print(f"{YELLOW}{msg}{RESET}")
        return 1

    baseline = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    baseline_files: dict[str, str] = baseline.get("files", {})
    current_files = collect_files()

    modified = sorted(p for p in baseline_files if p in current_files and baseline_files[p] != current_files[p])
    removed = sorted(p for p in baseline_files if p not in current_files)
    added = sorted(p for p in current_files if p not in baseline_files)

    if as_json:
        print(json.dumps({"modified": modified, "removed": removed, "added": added}, indent=2))
        return 1 if (modified or removed) else 0

    print(f"{BOLD}Integrity Verify{RESET} — baseline generated {baseline.get('generated_at', '?')}, "
          f"{baseline.get('file_count', '?')} file(s)")

    if not modified and not removed and not added:
        print(f"\n{GREEN}No drift — current files match the baseline manifest exactly.{RESET}")
        return 0

    if modified:
        print(f"\n{RED}Modified ({len(modified)}) — content differs from baseline:{RESET}")
        for p in modified:
            print(f"  ✘ {p}")
    if removed:
        print(f"\n{RED}Removed ({len(removed)}) — present in baseline, missing now:{RESET}")
        for p in removed:
            print(f"  ✘ {p}")
    if added:
        print(f"\n{YELLOW}Added ({len(added)}) — new since baseline (expected on ordinary kit growth):{RESET}")
        for p in added:
            print(f"  + {p}")

    print(f"\n{YELLOW}Drift found — review 'Modified'/'Removed' entries. If this is a derived project "
          f"you customized on purpose, this is expected; if not, compare against the released source.{RESET}")

    return 1 if (modified or removed) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generates/verifies a SHA-256 manifest of the kit's rules/agents/workflows layer.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("generate", help="Write a new baseline manifest.")
    p_verify = sub.add_parser("verify", help="Compare current files against the baseline manifest.")
    p_verify.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.command == "generate":
        return cmd_generate()
    if args.command == "verify":
        return cmd_verify(args.json)
    return 1


if __name__ == "__main__":
    sys.exit(main())
