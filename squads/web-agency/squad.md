---
name: web-agency
goal: Deliver a client website end-to-end — from discovery and PRD to deployed, verified product — like a full-service web agency.
checkpoint-mode: key-points
version: "1.0.0"
---

# Web Agency Squad

## When to run
A client (or prospect) asked for a website, landing page, or web product, and you want the
full professional cycle: requirements, proposal with stack/cost, design, build, QA, SEO,
deploy, and handoff.

## Inputs (asked at the start of every run)
- Client name and business (one sentence: what they sell, to whom).
- What the client asked for, in their own words (briefing, links, references if any).
- Budget range and deadline, if known (drives the stack-sizing tier).
- Where the code project should live (folder path or new repo name).

## Pipeline

| # | Step | Agent (kit) | Skills to load | Deliverable | Checkpoint after? |
|---|------|-------------|----------------|-------------|-------------------|
| 1 | Discovery & PRD | product-manager | brainstorming, plan-writing | output/01-prd.md | No |
| 2 | Technical proposal — stack, tier, cost, timeline | project-planner | stack-sizing, effort-estimation | output/02-proposal.md | **Yes — client-facing proposal approval** |
| 3 | Design direction — layout, palette, typography, references | frontend-specialist | frontend-design (+ /ui-ux-pro-max for premium tiers) | output/03-design-brief.md | **Yes — design approval** |
| 4 | Build — implement the site in the project folder | frontend-specialist + backend-specialist + database-architect (only the ones the tier needs) | per agent frontmatter | working code in `project_path` | No |
| 5 | QA — tests, accessibility, cross-checks | qa-automation-engineer | webapp-testing, testing-patterns | checklist.py output pasted + output/05-qa-report.md | No |
| 6 | SEO & performance pass | seo-specialist | seo-fundamentals, geo-fundamentals | output/06-seo-report.md | No |
| 7 | Deploy | devops-engineer | deployment-procedures (via /deploy, verify_all.py) | live URL + verify_all.py output | **Yes — BEFORE deploying (irreversible)** |
| 8 | Handoff — client-facing summary and maintenance guide | documentation-writer | documentation-templates | output/08-handoff.md | No |

## Checkpoints (business language)
1. **After step 2 — Proposal:** you approve what will be built, with which technology
   tier, estimated effort/cost and timeline, BEFORE any design or code exists. Changing
   scope after this point costs rework.
2. **After step 3 — Design:** you approve the visual direction before the build. Cheaper
   to change a brief than a built site.
3. **Before step 7 — Deploy:** publishing puts the site live on the internet for the
   client and their users; a bad deploy is visible to them. Approval is mandatory here
   even in autonomous mode, with the risk spelled out (what goes live, rollback time).

## Done means
- All 8 steps `done` in `state.json`; deliverables 01, 02, 03, 05, 06, 08 exist in `output/`.
- `checklist.py` passing (step 5) and `verify_all.py` passing against the live URL (step 7),
  with fresh output pasted in the conversation — not claimed from memory.
- Handoff document delivered in plain language the client can read.

## Out of scope
- Ongoing content production for the site after launch (create a content squad for that).
- Mobile apps (route to `mobile-developer` directly, or a dedicated squad).
