# DevBureau

> AI Agent templates with Skills, Agents, and Workflows

## Quick Install

```bash
npx devbureau init
```

Or install globally:

```bash
npm install -g devbureau
devbureau init
```

This installs the `.agent` folder containing all templates into your project.

## Usage

### Using Agents

**No need to mention agents explicitly!** The system automatically detects and applies the right specialist(s):

```
You: "Add JWT authentication"
AI: 🤖 Applying @security-auditor + @backend-specialist...

You: "Fix the dark mode button"
AI: 🤖 Using @frontend-specialist...

You: "Login returns 500 error"
AI: 🤖 Using @debugger for systematic analysis...
```

**How it works:**

- Analyzes your request silently
- Detects domain(s) automatically (frontend, backend, security, etc.)
- Selects the best specialist(s)
- Informs you which expertise is being applied
- You get specialist-level responses without needing to know the system architecture

**Benefits:**

- ✅ Zero learning curve - just describe what you need
- ✅ Always get expert responses
- ✅ Transparent - shows which agent is being used
- ✅ Can still override by mentioning agent explicitly

### Using Workflows

Invoke workflows with slash commands:

| Command          | Description                           |
| ---------------- | ------------------------------------- |
| `/brainstorm`    | Explore options before implementation |
| `/create`        | Create new features or apps           |
| `/debug`         | Systematic debugging                  |
| `/deploy`        | Deploy application                    |
| `/enhance`       | Improve existing code                 |
| `/orchestrate`   | Multi-agent coordination              |
| `/plan`          | Create task breakdown                 |
| `/preview`       | Preview changes locally               |
| `/status`        | Check project status                  |
| `/test`          | Generate and run tests                |
| `/ui-ux-pro-max` | Design with 50 styles                 |

Example:

```
/brainstorm authentication system
/create landing page with hero section
/debug why login fails
```

### Using Skills

Skills are loaded automatically based on task context. The AI reads skill descriptions and applies relevant knowledge.

## CLI Tool

| Command            | Description                               |
| ------------------ | ----------------------------------------- |
| `devbureau init`   | Install `.agent` folder into your project |
| `devbureau update` | Update to the latest version              |
| `devbureau status` | Check installation status                 |

### Options

```bash
devbureau init --force        # Overwrite existing .agent folder
devbureau init --path ./myapp # Install in specific directory
devbureau init --branch dev   # Use specific branch
devbureau init --quiet        # Suppress output (for CI/CD)
devbureau init --dry-run      # Preview actions without executing
```

## Documentation

- **[Online Docs](https://github.com/fernandotenguan/devbureau#readme)** - Browse all documentation online

## Support

<p align="center">
  <img src="/pix-fernando.png" alt="PIX QR Code" width="200" />
</p>

<p align="center">PIX key: fernando.tenguan@gmail.com</p>

## License

MIT © DevBureau
