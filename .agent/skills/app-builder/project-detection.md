# Project Type Detection

> Analyze user requests to determine project type and template.

## Keyword Matrix

| Keywords | Project Type | Template |
|----------|--------------|----------|
| blog, post, article | Blog | astro-static |
| e-commerce, product, cart, payment | E-commerce | nextjs-saas |
| dashboard, panel, management | Admin Dashboard | nextjs-fullstack |
| api, backend, service, rest | API Service | express-api |
| python, fastapi, django | Python API | python-fastapi |
| mobile, android, ios, react native | Mobile App (RN) | react-native-app |
| flutter, dart | Mobile App (Flutter) | flutter-app |
| portfolio, personal, cv | Portfolio | nextjs-static |
| crm, customer, sales | CRM | nextjs-fullstack |
| saas, subscription, stripe | SaaS | nextjs-saas |
| landing, promotional, marketing | Landing Page | nextjs-static |
| docs, documentation | Documentation | astro-static |
| extension, plugin, chrome | Browser Extension | chrome-extension |
| desktop, electron | Desktop App | electron-desktop |
| cli, command line, terminal | CLI Tool | cli-tool |
| monorepo, workspace | Monorepo | monorepo-turborepo |

## Skill Profile by Project Family

Once the project type resolves, this narrows which skill family to reach for first — a routing shortcut, not an installation/loading restriction (skills already load on demand, so this doesn't reduce their footprint; it reduces search time when picking one). Skills outside a project's profile are still available on request (e.g. a Web project that later needs `mobile-design` for a companion app) — never refuse a skill just because it's outside the detected profile.

| Project Family | Project Types | Core Skill Set |
|---|---|---|
| Web | Blog, Portfolio, Landing Page, Admin Dashboard, CRM, Documentation | `frontend-design`, `tailwind-patterns`, `nextjs-react-expert`, `accessibility-standards`, `seo-fundamentals` |
| Mobile | Mobile App (RN), Mobile App (Flutter) | `mobile-design`, `accessibility-standards` |
| Backend/API | API Service, Python API | `api-patterns`, `nodejs-best-practices`, `database-design`, `python-patterns` |
| SaaS (full-stack) | SaaS, E-commerce | `saas-stack-rules`, `app-builder`, `api-patterns`, `database-design`, `frontend-design` |
| Desktop/CLI/Extension | Desktop App, Browser Extension, CLI Tool | `nodejs-best-practices`, `deployment-procedures` |
| Content/Marketing | (no code project — social/content requests) | `humanizer`, `carousel-design-system`, `social-publisher`, `seo-fundamentals`, `geo-fundamentals` |

## Detection Process

```
1. Tokenize user request
2. Extract keywords
3. Determine project type
4. Detect missing information → forward to conversation-manager
5. Suggest tech stack
```
