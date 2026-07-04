# Squads

Reusable multi-agent teams for repeatable business processes. Each squad is a folder with:

- `squad.md` — the definition (pipeline, roles, checkpoints). Created via `/squad create`.
- `state.json` — current run state (created by `/squad run <name>`; safe to delete to reset).
- `output/` — deliverables produced by runs (PRDs, proposals, briefs, reports).

Engine: `.agent/skills/squad-forge/SKILL.md` · Command: `/squad` (create / run / list / status / edit).

Included example: **web-agency** — full client-website delivery, from PRD to deploy.
