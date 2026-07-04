---
name: content-production
goal: Produce and publish a piece of social media content — carousel, single post, or story — from a topic/angle to a live, published post.
checkpoint-mode: key-points
version: "1.0.0"
---

# Content Production Squad

## When to run
A client (or your own content calendar) needs a social media piece produced end to end:
research, copy, design, and publishing, with your approval before it goes live.

## Inputs (asked at the start of every run)
- Client/brand name and one-sentence context (audience, tone, existing brand colors if any).
- Topic, angle, or the trending news to base the content on (or ask content-creator to
  find one via research).
- Target platform and format (Instagram carousel, single post, Story, LinkedIn post).
- Publishing destination: publish now, schedule, or draft-only (no publish step).

## Pipeline

| # | Step | Agent (kit) | Skills to load | Deliverable | Checkpoint after? |
|---|------|-------------|-----------------|-------------|-------------------|
| 1 | Research — angle, trend, or fact-check | content-creator | content-research | output/00-research.md | No |
| 2 | Strategy — angle, hook, structure | content-creator | brainstorming | output/01-strategy.md | **Yes — approve the angle before writing full copy** |
| 3 | Copywriting — hook, body, CTA per slide/post | content-creator | (writing, no extra skill) | output/02-draft.md | No |
| 4 | Humanize — remove AI-writing tells | content-creator | humanizer | output/03-final-copy.md | No |
| 5 | Design — design system + HTML slides | content-creator | carousel-design-system | output/slides/*.html | No |
| 6 | Render — HTML to PNG | content-creator | visual-renderer | output/slides/*.png | **Yes — approve the rendered visuals + final copy together** |
| 7 | Publish (skipped if Inputs = draft-only) | content-creator | social-publisher | live post URL in output/07-published.md | **Yes — BEFORE publishing (irreversible)** |

## Checkpoints (business language)
1. **After step 2 — Strategy:** you approve the content angle and hook before any full
   copy is written. Cheaper to redirect here than after a full draft exists.
2. **After step 6 — Rendered visuals:** you see the exact images and final copy exactly as
   they would appear on the platform. This is the last point to catch a typo, a wrong
   color, or an off-brand claim before it is public.
3. **Before step 7 — Publish:** publishing puts the content live in front of the client's
   real audience; it cannot be quietly undone. Mandatory even in autonomous mode.

## Done means
- All non-skipped steps `done` in `state.json`; deliverables 00-03 and rendered slides
  exist in `output/`.
- If publishing: a live post URL recorded in `output/07-published.md`.
- If draft-only: final rendered assets delivered, no publish attempted.

## Out of scope
- Video editing/clipping (not covered by this kit yet).
- Email campaigns — use `email-sender` directly or build a dedicated squad for a
  multi-touch sequence.
- SEO-optimized blog articles — route to `seo-specialist` instead; this squad is for
  social-first, visual content.
