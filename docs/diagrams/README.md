# Diagrams

Generated with [drawio-skill](https://github.com/Agents365-ai/drawio-skill) (MIT) — a Claude Code Agent Skill that writes `.drawio` XML and exports it via the draw.io desktop CLI. Not bundled into DevBureau itself (it needs the draw.io desktop app installed locally, and it's a generic diagramming tool, not DevBureau IP) — same "optional, documented, not shipped" pattern as the Headroom MCP integration.

| File | What it shows |
|---|---|
| `devbureau-architecture.drawio(.png)` | Macro view: request → DEVBUREAU.md rules → routing → the 4 catalogs (agents/skills/workflows/scripts) → verification → memory |
| `ade-pipeline.drawio(.png)` | The `/ade` 6-phase pipeline, including the approval gate (Fase 3) and the QA retry loop (Fase 5 → `@debugger`) |

Each `.png` has the diagram XML embedded (`-e` export) — open it directly in draw.io desktop to edit, no need to track down the `.drawio` source separately (though it's here too, for convenience and smaller diffs).

## Regenerating or editing

1. Install draw.io desktop: https://github.com/jgraph/drawio-desktop/releases
2. Re-install the skill locally (gitignored, not tracked — see `.gitignore`):
   ```bash
   git clone https://github.com/Agents365-ai/drawio-skill.git .claude/skills/drawio-skill
   ```
3. Ask your agent to edit the `.drawio` file directly, or open it in draw.io desktop by hand.
4. Re-export: `"draw.io" -x -f png -e -s 2 -o name.drawio.png name.drawio`, then run `python .claude/skills/drawio-skill/scripts/repair_png.py name.drawio.png` (draw.io's CLI truncates the PNG's IEND chunk on `-e` exports — see the skill's `references/troubleshooting.md`).
