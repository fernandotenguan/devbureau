#!/usr/bin/env python3
"""
_dead_ends.py - shared helper for hooks that persist a failed approach.
Not a hook itself (leading underscore, not registered in .claude/settings.json).

DEVBUREAU.md's Loop Protection catches a repeat inside one session, but
nothing stopped the same dead end from being tried again next week. Entries
land in .agent/memory/dead-ends.md using the same `## YYYY-MM-DD — title`
plus `Gatilho:` convention as lessons.md and gotchas.md, so
`memory_recall.py recall <keyword>` finds them before the retry.

Best-effort: any failure to write degrades to silence. A registry that
crashes the tool call it is observing would be worse than no registry.
"""

import re
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER = REPO_ROOT / ".agent" / "memory" / "dead-ends.md"

MAX_TARGET_CHARS = 120

# Same high-confidence shapes scan_secrets_on_write.py blocks. A failed command
# can carry a credential, and a memory file is committed to the repo.
SECRET_SHAPES = re.compile(
    r"AKIA[0-9A-Z]{16}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|sk_live_[0-9a-zA-Z]{16,}"
    r"|gh[pousr]_[A-Za-z0-9]{36,}"
    r"|github_pat_[A-Za-z0-9_]{50,}"
    r"|xox[baprs]-[0-9A-Za-z-]{10,}"
    r"|AIza[0-9A-Za-z_-]{35}"
    r"|sk-ant-[A-Za-z0-9_-]{20,}"
    r"|eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
)

HEADER = """# Dead Ends — DevBureau

> Abordagens que já falharam de forma repetida, registradas automaticamente
> pelo hook `detect_tool_loop.py` quando as Loop Detection Rules do
> DEVBUREAU.md disparam. Antes de repetir um comando que parece familiar,
> rode `python .agent/scripts/memory_recall.py recall <termo>`.
>
> Uma entrada aqui não é uma proibição permanente: é o registro de que aquele
> caminho exato já custou tempo. Se o contexto mudou, tente de novo e apague
> a entrada.

## YYYY-MM-DD — [Ferramenta] resumo do que falhou

- **Gatilho:** trecho do comando ou caminho do arquivo
- **O que foi tentado:** descrição em uma linha
- **Assinatura:** hash curto dos argumentos
"""


def redact(text: str) -> str:
    return SECRET_SHAPES.sub("[REDACTED]", text)


def summarize(tool_input: dict) -> str:
    """One short, secret-free line describing what was attempted."""
    raw = tool_input.get("command") or tool_input.get("file_path") or ""
    flattened = " ".join(str(raw).split())
    trimmed = flattened[:MAX_TARGET_CHARS]
    if len(flattened) > MAX_TARGET_CHARS:
        trimmed += "…"
    return redact(trimmed)


def already_registered(signature: str) -> bool:
    try:
        return f"**Assinatura:** `{signature}`" in LEDGER.read_text(
            encoding="utf-8", errors="ignore"
        )
    except OSError:
        return False


def record(tool: str, tool_input: dict, signature: str, reason: str) -> bool:
    """Append one entry unless this exact signature is already known."""
    if not LEDGER.exists():
        try:
            LEDGER.parent.mkdir(parents=True, exist_ok=True)
            LEDGER.write_text(HEADER, encoding="utf-8")
        except OSError:
            return False

    if already_registered(signature):
        return False

    target = summarize(tool_input)
    entry = (
        f"\n## {date.today().isoformat()} — [{tool}] {target[:60] or 'sem alvo'}\n\n"
        f"- **Gatilho:** `{target}`\n"
        f"- **O que foi tentado:** {reason}\n"
        f"- **Assinatura:** `{signature}`\n"
        f"- **Registrado por:** `detect_tool_loop.py` (Loop Detection Rules)\n"
    )
    try:
        with open(LEDGER, "a", encoding="utf-8") as handle:
            handle.write(entry)
    except OSError:
        return False
    return True
