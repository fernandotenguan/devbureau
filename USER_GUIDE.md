# 📚 DevBureau - Complete User Guide

> **Welcome!** This guide shows you how to use DevBureau from scratch. If you're new here, start with **[Step 1](#quick-start)**.

---

## 📑 Table of Contents (Click to Jump)

1. [Quick Start](#quick-start) — Set up in 2 minutes
2. [What is DevBureau?](#what-is-devbureau) — Understand the basics
3. [Your First Steps](#your-first-steps) — Choose your path
4. [How to Use (By Task)](#how-to-use-by-task) — Practical examples
5. [All Commands](#all-commands) — Quick reference
6. [Available Specialists](#available-specialists) — Who does what
7. [Frequently Asked Questions](#frequently-asked-questions)
8. [Advanced Configuration](#advanced-configuration)

---

## Quick Start

### ⚡ Set Up in 2 Minutes

You downloaded DevBureau? Great! Now run **ONE COMMAND** to activate everything:

```bash
python .agent/scripts/sync_ide.py --target all
```

**Done!** Your IDE (Cursor, Claude, VS Code) now understands DevBureau's powers automatically.

### ✅ Verify It Works

To confirm everything is operational:

```bash
check kit
```

or

```bash
python .agent/scripts/doctor.py
```

If you see green checkmarks with "✅ OK", it means your **agents and skills are ready**. You're good to go!

---

## What is DevBureau?

### 🤖 The Simple Idea

Imagine you have a **team of specialists** working for you:

- 🎨 Frontend Designer (visuals, colors, layout)
- ⚙️ Backend Engineer (server, APIs, logic)
- 💾 Database Architect (data organization)
- 🧪 QA Tester (quality assurance)
- 🛡️ Security Expert
- 🚀 DevOps Specialist
- ...and many others

**You never have to do anything alone.** You describe what you want, they build it.

### 💡 How It Works

```
You: "I want a login system with Google"
              ↓
DevBureau analyzes: "Do I need backend? Frontend? Security?"
              ↓
Relevant specialists work together
              ↓
You approve the plan
              ↓
Code is generated automatically
              ↓
You publish
```

---

## Your First Steps

### Choose Your Current Situation

Where are you right now? Click below:

#### 1️⃣ I Don't Have a Project Folder Yet

**Situation:** I have an idea, but I haven't created the project folder yet.

**Command:**

```
/new-project
```

**What happens:**

- DevBureau creates a new folder with all the intelligence
- You get a "map" with first steps
- Ready to use in 30 seconds

---

#### 2️⃣ I Have the Folder, But My Idea is Vague

**Situation:** I created the folder, but I'm not sure exactly what to build.

**Command:**

```
/brainstorm
```

**What happens:**

- DevBureau asks 5-7 strategic questions
- You answer simply (target audience, problem, main features)
- Result: Clear and structured idea
- Time: ~10 minutes

**Example conversation:**

```
DevBureau: Who will use this?
You: Personal trainers who want to manage their clients

DevBureau: What's their biggest problem today?
You: They can't see all clients' progress in one place

DevBureau: What's the most important feature?
You: A dashboard showing all clients and their individual progress
```

---

#### 3️⃣ My Idea is Clear, I Want to Design the System

**Situation:** I have a clear idea. I want to know how to build it before coding.

**Command:**

```
/build-saas [describe your idea in one sentence]
```

**Example:**

```
/build-saas An app for personal trainers to manage clients, workouts, and physical evolution
```

**What happens:**

- DevBureau guides you through **7 planning stages**
- You answer one question at a time (not technical, just simple)
- Result: **3 ready-to-implement documents**
- You SEE everything before one line of code is written

**The 7 Stages:**

1. **Discovery** — Who uses it? What problem does it solve?
2. **Requirements** — What are the main features?
3. **Database** — What's the data structure?
4. **Backend** — What's the server structure?
5. **Frontend** — What screens and components?
6. **Security** — How to protect the data?
7. **Documentation** — Generates the 3 final documents

**Total time:** ~30-45 minutes

---

#### 4️⃣ I Want Everything Automated (Hands-Free)

**Situation:** I don't want to answer questions. I want the agent to do everything.

**Command:**

```
/ade [describe your idea with details]
```

**Example:**

```
/ade Create an app for personal trainers to manage clients and workouts. I need:
- Dashboard with client list
- Workout history per client
- Weight evolution tracking
- Google login
- Responsive interface for mobile and desktop
```

**What happens (Autonomous Pipeline):**

```
1. Discovery — DevBureau understands your idea
2. Spec — Creates the detailed plan
3. ⏸️  YOU APPROVE (before coding)
4. Code — Implements everything automatically
5. Tests — Verifies it works
6. ✅ Ready to use
```

**Advantage:** You approve ONCE, and the agent does everything. Time: ~2-4 hours.

---

#### 5️⃣ I Want to Build Together, Step by Step

**Situation:** I want to see the process happen. I want to learn or follow closely.

**Command:**

```
/create [describe what you want]
```

**Example:**

```
/create a dashboard for personal trainers with client list and workout history
```

**What happens:**

- DevBureau talks with you as it creates files
- You approve each step
- You learn what's being done
- Time: ~3-5 hours

---

### Which One Should I Choose?

| Your Situation     | Command        | Time      | Best For             |
| ------------------ | -------------- | --------- | -------------------- |
| No project created | `/new-project` | 30 sec    | Getting started      |
| Vague idea         | `/brainstorm`  | 10 min    | Want clarity first   |
| Clear idea         | `/build-saas`  | 30-45 min | Want to see the plan |
| Want automation    | `/ade`         | 2-4 hours | Want fast results    |
| Want to learn      | `/create`      | 3-5 hours | Like to follow along |

---

## How to Use (By Task)

### 🎯 Do You Want to Do This? Click Here

#### Create a New System (SaaS, App, Website)

**You say:** I want to create a salon booking app

**You use:** `/build-saas` or `/ade` or `/create`

**Step by step:**

1. Choose one of the commands above (see "Your First Steps")
2. Describe your idea
3. Answer the questions (simple, no tech needed)
4. Approve the plan
5. Code is generated automatically

**Complete example:**

```
/build-saas A salon booking system with client management, services, and time slots
```

---

#### Add a New Feature

**You say:** I want to add an email notification system when someone books an appointment

**You use:** `/ade [describe the feature]`

**Example:**

```
/ade Add an email notification system when a client books an appointment.
The email should contain: service name, time, responsible professional.
Also send a reminder 1 day before the appointment.
```

**What you get:**

- Detailed plan (you approve)
- Implemented code
- Passing tests
- Ready to use

---

#### Fix a Bug (Something Doesn't Work)

**You say:** Login doesn't work in Chrome

**You use:** `/debug [describe the problem]`

**Example:**

```
/debug The login button doesn't work in Chrome. Works perfectly in Firefox.
When I click, the screen goes white and nothing happens. This started happening
after I updated the dependencies.
```

**What happens:**

1. Specialist investigates
2. Finds the cause
3. Fixes it
4. Tests it
5. Done

---

#### Improve Something Existing

**You say:** The landing page design looks old. I want something more modern.

**You use:** `/enhance [describe the improvement]`

**Examples:**

```
/enhance Make the landing page design more modern. Add:
- Smooth animations
- Modern color palette (blue + white + orange)
- Cards with shadows
- Larger fonts in titles
```

or

```
/enhance Our dashboard performance needs improvement. It's taking 5 seconds to load.
Reduce it to less than 2 seconds.
```

---

#### Test Quality

**You say:** Before publishing, I want to make sure everything works

**You use:**

```
final check
```

or

```
run all tests
```

**What happens:**

1. ✅ Security — Any vulnerabilities?
2. ✅ Linting — Clean code?
3. ✅ Types — TypeScript correct?
4. ✅ Tests — Everything passes?
5. ✅ Performance — Lighthouse OK?
6. ✅ UX — Responsive interface?

If everything passes, you get "✅ Ready to publish"

---

#### Publish to Production

**You say:** Ready! I want to go live.

**You use:**

```
/deploy
```

**What happens:**

1. Automatic security checklist
2. Verifies all tests pass
3. Confirms environment variables
4. Guides you step by step through deploy
5. Publishes safely

---

#### See Your App Running

**You say:** I want to see my app running now

**You use:**

```
/preview
```

**What happens:**

- Local server starts automatically
- Opens your browser
- You see the app running in real-time
- Can test, click, fill forms

---

#### See Project Progress

**You say:** How's the progress? What's left?

**You use:**

```
/status
```

**What you see:**

- ✅ Completed features
- 🔄 In progress
- ⏳ Planned
- Completion percentage

---

### 🤖 Activate a Specific Specialist

Beyond quick commands, you can activate a specific specialist by writing `@name`:

**How to use:**

```
@frontend-specialist: improve the design of this page, make it more modern

@backend-specialist: create a route to save customer data

@security-auditor: check if the app is secure

@database-architect: create the users table with the right fields
```

**All available specialists:**

| Specialist               | Use when...                             | Command                   |
| ------------------------ | --------------------------------------- | ------------------------- |
| 🎨 Frontend Designer     | Want to improve visuals, colors, layout | `@frontend-specialist`    |
| ⚙️ Backend Engineer      | Want to create APIs, server, routes     | `@backend-specialist`     |
| 💾 Database Architect    | Want to structure data, create tables   | `@database-architect`     |
| 📱 Mobile Developer      | Want to create iOS/Android app          | `@mobile-developer`       |
| 🔍 Debugger              | Have a bug, want to fix it              | `@debugger`               |
| 🛡️ Security Auditor      | Want to verify security                 | `@security-auditor`       |
| 🧪 Test Engineer         | Want to test and ensure quality         | `@test-engineer`          |
| 🚀 DevOps Engineer       | Want to deploy or manage infrastructure | `@devops-engineer`        |
| ⚡ Performance Optimizer | Want to make it faster                  | `@performance-optimizer`  |
| 🌐 SEO Specialist        | Want to rank on Google                  | `@seo-specialist`         |
| 📋 Project Planner       | Want to plan tasks                      | `@project-planner`        |
| 🎮 Game Developer        | Want to create a game                   | `@game-developer`         |
| 📄 Documentation Writer  | Want to document the project            | `@documentation-writer`   |
| 🔬 Explorer              | Want to analyze codebase                | `@explorer-agent`         |
| 🔧 Code Archaeologist    | Have old code, want to refactor         | `@code-archaeologist`     |
| 🧪 QA Automation         | Want automated tests                    | `@qa-automation-engineer` |
| 🕵️ Penetration Tester    | Want to test security (attacks)         | `@penetration-tester`     |
| 🤖 Orchestrator          | Want multiple specialists               | `@orchestrator`           |
| 📊 Product Manager       | Want to think about requirements        | `@product-manager`        |
| 📚 Content Creator       | Want to create content/posts            | `@content-creator`        |
| ♿ Accessibility Specialist | Want the app usable by everyone (WCAG) | `@accessibility-specialist` |
| 🔌 API Designer          | Want to design the API contract         | `@api-designer`           |
| 👨‍💼 SRE Engineer          | Want observability and monitoring       | `@sre-engineer`           |

---

## All Commands

### 📋 Complete Reference

#### Creation and Planning Commands

| Command        | What it does                                  | Example                    |
| -------------- | --------------------------------------------- | -------------------------- |
| `/new-project` | Creates a new folder with the complete kit    | `/new-project`             |
| `/brainstorm`  | Asks strategic questions to clarify your idea | `/brainstorm`              |
| `/build-saas`  | Plans a SaaS in 7 stages                      | `/build-saas delivery app` |
| `/plan`        | Plans a feature without coding                | `/plan payment system`     |
| `/create`      | Creates something from scratch, step by step  | `/create landing page`     |
| `/ade`         | Autonomous pipeline (does everything)         | `/ade create Google login` |

#### Development Commands

| Command    | What it does                | Example                            |
| ---------- | --------------------------- | ---------------------------------- |
| `/enhance` | Improves something existing | `/enhance make design more modern` |
| `/debug`   | Finds and fixes bugs        | `/debug login doesn't work`        |
| `/test`    | Creates and runs tests      | `/test`                            |
| `/preview` | Opens local server          | `/preview`                         |
| `/status`  | Shows project progress      | `/status`                          |

#### Deploy and Publishing Commands

| Command         | What it does                    |
| --------------- | ------------------------------- |
| `/deploy`       | Security checklist and publish  |
| `final check`   | Run all tests before publishing |
| `run all tests` | Execute test suite              |

#### Kit Health Commands

| Command          | What it does                               |
| ---------------- | ------------------------------------------ |
| `check kit`      | Complete diagnosis (all agents, skills, and workflows) |
| `diagnostics`    | Same as above                              |
| `everything ok?` | Check integrity                            |

#### Premium Design Command

| Command          | What it does                   | Time      |
| ---------------- | ------------------------------ | --------- |
| `/ui-ux-pro-max` | 50 premium visual styles ready | 2-3 hours |

---

## Available Specialists

### 🎨 Design (Frontend + Mobile)

#### **Frontend Specialist** — Web Designer

- **When to use:** Visuals, colors, layout, buttons, responsiveness
- **Examples:** "improve design", "dark mode", "make it modern"
- **Command:** `@frontend-specialist`

#### **Mobile Developer** — App Developer

- **When to use:** iOS, Android, React Native, Flutter apps
- **Examples:** "create mobile app", "interface for phone"
- **Command:** `@mobile-developer`

---

### ⚙️ Backend (Servers and Logic)

#### **Backend Specialist** — Server Engineer

- **When to use:** APIs, routes, server, authentication, business logic
- **Examples:** "create a route", "connect frontend with backend"
- **Command:** `@backend-specialist`

#### **Database Architect** — Database Expert

- **When to use:** Data structure, tables, SQL, migrations
- **Examples:** "model data", "create users table"
- **Command:** `@database-architect`

---

### 🛡️ Quality and Security

#### **Security Auditor** — Security Expert

- **When to use:** Vulnerabilities, encryption, data protection
- **Examples:** "is the site secure?", "check vulnerabilities"
- **Command:** `@security-auditor`

#### **Test Engineer** — Tester

- **When to use:** Tests, coverage, quality validation
- **Examples:** "test it", "check quality"
- **Command:** `@test-engineer`

#### **Debugger** — Bug Expert

- **When to use:** Something doesn't work, error, bug, white screen
- **Examples:** "it doesn't work", "it's broken", "404 error"
- **Command:** `@debugger`

---

### 🚀 Deploy and Performance

#### **DevOps Engineer** — Infrastructure Expert

- **When to use:** Deploy, CI/CD, Docker, server, publishing
- **Examples:** "go live", "deploy", "server is down"
- **Command:** `@devops-engineer`

#### **Performance Optimizer** — Speed Optimizer

- **When to use:** Site is slow, optimization, cache, large bundles
- **Examples:** "it's slow", "improve speed", "Core Web Vitals"
- **Command:** `@performance-optimizer`

---

### 📊 Strategy and Content

#### **Project Planner** — Project Planner

- **When to use:** Planning, requirements, discovery, roadmap
- **Examples:** "plan it", "what are the requirements?"
- **Command:** `@project-planner`

#### **Product Manager** — Product Manager

- **When to use:** User stories, requirements, backlog
- **Examples:** "user stories", "app requirements"
- **Command:** `@product-manager`

#### **Content Creator** — Content Creator

- **When to use:** Posts, carousels, social media content
- **Examples:** "create a post", "carousel design"
- **Command:** `@content-creator`

---

### 🔬 Analysis and Specialties

#### **Orchestrator** — Orchestrator

- **When to use:** Complex task involving multiple specialists
- **Examples:** "complex task", "do everything"
- **Command:** `@orchestrator`

#### **Explorer Agent** — Codebase Explorer

- **When to use:** Analyze code, understand project, list files
- **Examples:** "analyze code", "project overview"
- **Command:** `@explorer-agent`

#### **Code Archaeologist** — Code Archaeologist

- **When to use:** Refactor old code, clean code, reorganize
- **Examples:** "refactor", "old code", "clean code"
- **Command:** `@code-archaeologist`

---

### 📖 Documentation and Specific

#### **Documentation Writer** — Documentor

- **When to use:** README, documentation, guides, API docs
- **Examples:** "document it", "write README"
- **Command:** `@documentation-writer`

#### **SEO Specialist** — SEO Expert

- **When to use:** Rank on Google, rankings, visibility
- **Examples:** "appear on Google", "improve SEO"
- **Command:** `@seo-specialist`

#### **QA Automation Engineer** — E2E Tester

- **When to use:** Automated tests, Playwright, test pipelines
- **Examples:** "test the whole app", "E2E test"
- **Command:** `@qa-automation-engineer`

---

### 🎮 Additional Specializations

#### **Game Developer** — Game Developer

- **When to use:** Create 2D, 3D, multiplayer games
- **Examples:** "create a game", "game mechanic"
- **Command:** `@game-developer`

#### **Penetration Tester** — Security Tester

- **When to use:** Penetration test, red team, security testing
- **Examples:** "simulate attack", "penetration test"
- **Command:** `@penetration-tester`

---

## Frequently Asked Questions

### ❓ Common Questions

#### Q: Do I need to know how to code to use DevBureau?

**A:** No. The kit codes for you. Your job is to describe what you want and approve the result.

#### Q: Will the agent ask me technical questions?

**A:** No. Questions are strategic (target audience, features, monetization). Technical decisions are automatic.

#### Q: What if I want to change something later?

**A:** Just ask naturally. "Change the color scheme to blue" or "Add a FAQ page".

#### Q: Can I use this for any type of project?

**A:** Yes. Works for SaaS, landing pages, mobile apps, games, APIs, e-commerce, and much more.

#### Q: What's the difference between `/build-saas`, `/create`, and `/ade`?

**A:**

- **`/build-saas`** — Plan in 7 stages, you answer questions. Best to understand everything before coding.
- **`/create`** — Build step by step, talking with you. Best if you want to learn.
- **`/ade`** — Do everything autonomously, you approve ONCE. Best if you want speed.

#### Q: Can the agent get stuck in a loop?

**A:** Yes, but the kit has protection. If you notice, just say "stop", "cancel", or "reset". The agent will stop.

#### Q: How do I backup my code?

**A:** Everything is saved in Git. Each change can be saved with `git commit`. Your code is protected.

#### Q: How much does it cost?

**A:** DevBureau is free. You use your Claude account (Cursor, claude.ai, or IDE extension).

#### Q: Can I safely delete something?

**A:** Everything is version-controlled in Git. If you delete something, you can recover it with `git revert` or `git restore`.

#### Q: What's the maximum project size I can build?

**A:** No limit. DevBureau works from MVPs to complex applications with millions of users.

#### Q: What is a "Skill"?

**A:** A skill is a superpower. Examples: "humanizer" (removes AI-writing tells from text), "content-creator" (creates social media posts).

#### Q: What is a "Squad"?

**A:** A squad is a specialized team for a specific process. Example: "content production squad" to automatically create posts, images, emails.

---

## Advanced Configuration

### 🔧 For Experienced Users

#### Configure Your IDE (VSCode, Cursor, JetBrains)

Already ran the setup command?

```bash
python .agent/scripts/sync_ide.py --target all
```

If not, run it now. It creates:

- `.cursorrules` — Rules for Cursor
- `.clauderules` — Rules for Claude
- Automatic IDE configuration

---

#### Use DevBureau with Google Gemini

If you use **Gemini Code Assist** (VS Code or IntelliJ):

- No special commands needed
- Gemini analyzes the `.agent/` folder automatically
- Still recommended to run `sync_ide.py`

If you use **Google AI Studio or Gemini Advanced** (web):

1. Open [.agent/rules/DEVBUREAU.md](./.agent/rules/DEVBUREAU.md)
2. Copy all content
3. Paste in your chat's "System Instructions" section
4. Done!

---

#### Read Technical Details

For users who want to understand the architecture:

**Read in this order:**

1. `.agent/ARCHITECTURE.md` — Overview of agents and skills
2. `.agent/rules/DEVBUREAU.md` — All detailed rules
3. `.agent/SCRIPTS_REGISTRY.md` — List of all available scripts

---

#### Create a Custom Skill

If you want to create a new superpower:

```bash
/skillify
```

This guides you to create your own reusable skill.

---

#### Create a Squad (Specialized Team)

If you want to assemble a team for a specific process:

```
/squad [describe the process]
```

**Example:**

```
/squad Create an automated system that:
1. Researches marketing news
2. Selects the 5 best
3. Creates Instagram posts
4. Creates LinkedIn posts
5. Publishes automatically
```

DevBureau creates a `squads/marketing-automation/` folder with all the setup.

---

#### Check Kit Integrity

If something seems wrong:

```bash
python .agent/scripts/doctor.py
```

It checks:

- ✅ Are all agents ready?
- ✅ Do all skills work?
- ✅ Are scripts configured?
- ✅ Are dependencies OK?

---

### 📚 Recommended Additional Reading

If you want to learn more:

| Interest            | File                         |
| ------------------- | ---------------------------- |
| Skills Guide        | `.agent/skills/*/SKILL.md`   |
| Agent Documentation | `.agent/agents/*/[name].md`  |
| Scripts Registry    | `.agent/SCRIPTS_REGISTRY.md` |
| Kit Architecture    | `.agent/ARCHITECTURE.md`     |
| All Rules           | `.agent/rules/DEVBUREAU.md`  |

---

## 🚀 Next Steps

### Start Now!

1. **Run the setup:**

    ```bash
    python .agent/scripts/sync_ide.py --target all
    ```

2. **Verify:**

    ```bash
    check kit
    ```

3. **Choose your path** (go back to the beginning):
    - Vague idea → `/brainstorm`
    - Clear idea → `/build-saas`
    - Want speed → `/ade`
    - Want to learn → `/create`

4. **Leverage the specialists** by mentioning `@name` when you need them

---

## 📞 Need Help?

### For Errors or Questions

1. **Try first:** `check kit` (automatic diagnosis)
2. **If unresolved:** Check the **[Frequently Asked Questions](#frequently-asked-questions)** above
3. **If still unresolved:** Open an issue or check the documentation in `.agent/rules/DEVBUREAU.md`

---

> **Congratulations!** You now know how to use DevBureau.
>
> Remember: **You own the product. DevBureau is your development team.**
>
> 🎉 Happy coding!
