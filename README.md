# jojo-in-runtime-skill-hub

A **Claude Code plugin marketplace** — a curated collection of skills and plugins I've created and used, shared for anyone to install and use.

## What is this?

This repository hosts plugins and skills for [Claude Code](https://claude.ai/code) that extend its capabilities in areas like lead generation, game development, brand guidelines, and more.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| **lead-gen-plugin** | Full lead generation system — prospect research, enrichment, scoring, outreach writing, CRM updates |
| **emily-unreal-explorer** | Skill hub for Unreal Engine development — UE features, C++ patterns, Sequencer, game architecture |
| **emily-brand-unified-guidelines** | Unified color system for UI, presentation, and data visualization |
| **emily-presentation-system** | Data-driven and sprint presentation deck generator |
| **playwright-cli** | Automate browser interactions, test web pages with Playwright (requires Node.js) |
| **nextjs-web** | Complete Next.js web development — React 18+, App Router, Server Components, TypeScript, Tailwind CSS, Supabase Auth, Turbopack |

## Installation

```bash
# Add this marketplace
/plugin marketplace add jojo-in-runtime/jojo-in-runtime-skill-hub

# Install a plugin
/plugin install lead-gen-plugin@jojo-in-runtime-marketplace
/plugin install emily-unreal-explorer@jojo-in-runtime-marketplace
/plugin install playwright-cli@jojo-in-runtime-marketplace
/plugin install nextjs-web@jojo-in-runtime-marketplace
```

## Available Skills

### Lead Generation
- `lead-scoring` — Score leads (Hot/Warm/Cool/Low)
- `lead-enrichment` — Enrich lead data
- `prospect-research` — Research target companies
- `outreach-writer` — Draft personalized emails
- `crm-update` — Update CRM records

### Web Development (via nextjs-web)
- `nextjs-turbopack` — Turbopack optimization and dev speed
- `nextjs-supabase-auth` — Supabase Auth integration
- `react-nextjs-development` — Full React/Next.js workflow

### Game Development (via emily-unreal-explorer)
- `unreal-engine-53-feature-knowledge` — UE 5.3 features
- `unreal-engine-cpp-pro` — C++ best practices
- `unreal-sequencer` — Cinematics and cutscenes
- `game-developer` — General game dev patterns

## How Plugins Work

Plugins in this marketplace are designed to be used directly in Claude Code conversations. Simply invoke the skill or command and Claude will use the plugin's guidance.

## License

MIT