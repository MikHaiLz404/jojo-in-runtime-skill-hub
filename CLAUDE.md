# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **plugin marketplace** for Claude Code containing skills and plugins for lead generation, game development, brand guidelines, and presentation systems.

## Project Structure

```
jojo-in-runtime-skill-hub/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace catalog
├── plugins/                      # Available plugins
│   ├── lead-gen-plugin/          # Lead generation automation
│   ├── emily-unreal-explorer/    # Unreal Engine skill hub
│   ├── emily-brand-unified-guidelines/  # Design system
│   ├── emily-presentation-system/  # Presentation generator
│   └── playwright-cli/          # Browser automation with Playwright
├── auto-lead-gen-template/       # Lead gen template (separate repo)
└── README.md
```

## Marketplace

This repo is a Claude Code plugin marketplace. Install with:
```
/plugin marketplace add jojo-in-runtime/jojo-in-runtime-skill-hub
/plugin install <plugin-name>@jojo-in-runtime-marketplace
```

## Available Plugins

| Plugin | Description |
|--------|-------------|
| `lead-gen-plugin` | Complete lead gen system: prospect research → enrichment → scoring → outreach → CRM |
| `emily-unreal-explorer` | Skill hub for Unreal Engine: UE features, C++ patterns, Sequencer, game architecture |
| `emily-brand-unified-guidelines` | Unified color system: UI + Presentation + Data visualization |
| `emily-presentation-system` | Data-driven presentation deck generator |
| `playwright-cli` | Browser automation with Playwright (requires Node.js) |

## Plugin Structure

Each plugin follows Claude Code plugin conventions:
- `.claude-plugin/plugin.json` — Plugin manifest
- `SKILL.md` or `skills/` — Skill definitions
- `commands/` — Custom slash commands (if applicable)

## Key Commands

- `/lead-gen-plugin:full-pipeline [number]` — Run full lead generation pipeline
- `/schedule` — Set up scheduled tasks in Claude Cowork

## MCP Connectors (for lead-gen-plugin)

- **Gmail** — Send and read emails
- **Google Drive** — Store documents
- **Google Calendar** — Schedule meetings
- **HubSpot/Salesforce** (optional) — CRM integration

## Important Rules

- All emails must be approved by a human before sending
- Verify company data from reliable sources
- Comply with PDPA for personal data handling
- Computer must be on and Claude Desktop must be running for scheduled tasks

## Validate Plugins

```bash
claude plugin validate plugins/<plugin-name>
```