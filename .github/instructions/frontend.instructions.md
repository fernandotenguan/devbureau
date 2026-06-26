---
applyTo: "**/*.{tsx,jsx,css,scss,html,vue,svelte}"
---

# Frontend Rules — DevBureau
> Auto-generated via sync_ide.py. Do not edit manually.

## Agent Routing

For frontend/UI work, apply the `@frontend-specialist` agent.
Read `.agent/agents/frontend-specialist.md` for full design rules.

## Project Type Routing

| Project Type | Primary Agent | Skills |
|---|---|---|
| **WEB** (Next.js, React web) | `frontend-specialist` | frontend-design |
| **MOBILE** (iOS, Android, RN, Flutter) | `mobile-developer` | mobile-design |

> Mobile + frontend-specialist = WRONG. Mobile = mobile-developer ONLY.

## UI/UX Principles

- No generic/template-looking layouts. Every UI must feel custom and premium.
- Use modern typography (Inter, Roboto, Outfit) instead of browser defaults.
- Use smooth gradients, micro-animations, and hover effects for engagement.
- Dark mode support when applicable.
- Responsive design is mandatory: mobile-first approach.
- Accessibility: semantic HTML, ARIA labels, keyboard navigation.

## Component Standards

- Components must be focused and reusable. One component, one responsibility.
- Props should be typed with interfaces (TypeScript) or PropTypes.
- Avoid prop drilling: use context or state management for deep data.
- CSS: prefer CSS Modules or scoped styles. Avoid global styles leaking.

## Performance

- Lazy load routes and heavy components.
- Optimize images (WebP, proper sizing, lazy loading).
- Core Web Vitals targets: LCP < 2.5s, FID < 100ms, CLS < 0.1.
- Bundle size awareness: check imports, avoid importing entire libraries.
