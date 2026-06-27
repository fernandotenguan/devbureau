---
name: finishing-a-branch
description: Use when implementation is complete and tests pass, to decide how to integrate the work — guides completion with structured merge/PR/keep/discard options instead of an open-ended "what now?"
allowed-tools: Read, Bash
---

# Finishing a Branch

> Source: obra/superpowers

## Overview

Closing out finished work needs the same discipline as starting it. An open-ended "what would you like to do?" produces ambiguous answers; a structured menu doesn't.

**Core principle:** verify tests → detect the workspace environment → present exactly the right options → execute the choice → clean up.

## Step 1: Verify Tests First

Run the project's test command before presenting any options. If it fails, stop here — report the failures and do not proceed to Step 2 until they're fixed. Merging or opening a PR on a failing branch just moves the failure somewhere harder to see.

## Step 2: Detect the Environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
```

| State | Menu | Cleanup |
|---|---|---|
| `GIT_DIR == GIT_COMMON` (normal repo) | Standard 4 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 4 options | Provenance-based (Step 5) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 3 options (no local merge) | None — externally managed |

## Step 3: Present Options

**Normal repo or named-branch worktree:**

```
Implementation complete. What would you like to do?
1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is
4. Discard this work
```

**Detached HEAD:**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).
1. Push as a new branch and create a Pull Request
2. Keep as-is
3. Discard this work
```

No extra explanation — keep the menu concise.

## Step 4: Execute the Choice

**Merge locally:** `cd` to the main repo root first (CWD safety if currently inside a worktree being removed), merge, re-run the test command on the merged result, only then clean up the worktree (Step 5) and `git branch -d`.

**Push + PR:** `git push -u origin <branch>`. Do **not** clean up the worktree — the user needs it alive to iterate on review feedback.

**Keep as-is:** report the branch name and worktree path. No cleanup.

**Discard:** require a typed `discard` confirmation before deleting anything — show what will be lost (branch name, commit list, worktree path) first. On confirmation: `cd` to main repo root, clean up the worktree (Step 5), then `git branch -D` (force, since the branch may be unmerged).

## Step 5: Clean Up the Workspace

**Only for the Merge and Discard options** — Push and Keep always preserve the worktree.

```bash
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**Provenance check first:** only remove a worktree under `.worktrees/` or `worktrees/` — that's the convention `using-git-worktrees` creates, so it's safe to assume ownership. A worktree anywhere else was created by the host's own native tool or the user directly; leave it alone (use a host workspace-exit tool if one exists, otherwise leave it in place).

```bash
cd "$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)"  # main repo root
git worktree remove "$WORKTREE_PATH"
git worktree prune   # clean up any stale registrations
```

Run `git worktree remove` from the main repo root, never from inside the worktree being removed — it fails silently otherwise.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Skipping test verification | Tests fail silently downstream in the merge/PR instead |
| Open-ended "what now?" instead of the structured menu | Ambiguous answers, more back-and-forth |
| Cleaning up the worktree on the Push option | User needs it alive for PR iteration |
| Deleting the branch before removing the worktree | `git branch -d` fails — the worktree still references it |
| No confirmation before Discard | Accidental permanent loss of work |
| Removing a worktree the harness/native tool created | Provenance check exists for exactly this |

## Integration

Pairs with `using-git-worktrees` for the setup side. `/ade`'s pipeline and `codebase-audit`'s `execute`-adjacent flows hand off here once work is done — neither prescribes what happens to the branch afterward, this skill does.
