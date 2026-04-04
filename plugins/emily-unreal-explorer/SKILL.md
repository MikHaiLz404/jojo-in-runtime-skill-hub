---
name: emily-unreal-explorer
description: A skill base to calling all unreal epic related skill sets
tools: Read
tags:
  - skill
  - unreal
  - gamedev
author: emily club
version: 1.0.0
updated: 2026-03-23
constraints:
  - Works standalone but best experience requires unreal-mcp for direct editor interaction
  - Without MCP: provides guidance, code examples, and best practices only
---

# ⚠️ IMPORTANT: Requirements

## Full Experience (Recommended)

| Requirement | Purpose |
|-------------|---------|
| **unreal-mcp** | MCP server for direct Unreal Editor integration |

With `unreal-mcp` configured, this skill can directly:
- Create and modify Blueprints/C++ classes
- Interact with Sequencer
- Manage actors and components
- Access editor state

## Limited Mode (Without MCP)

If `unreal-mcp` is not installed, the skill still works but provides:
- ✅ Code examples and templates
- ✅ Best practices and guidance
- ✅ Architecture recommendations
- ❌ Cannot directly interact with Unreal Editor

## Setup

To enable full functionality, configure the Unreal MCP server in Claude Code settings.

---

# Rules
สกิลในการทำงาน Unreal engine จะมี 5 สกิล จะให้เรียกใช้ตามเนื้อหาที่พูดคุย ให้ดูรายละเอียดของ skill ข้างล่างก่อนที่จะไปเรียกใช้

## Skills definition
- unreal-engine-53-feature-knowledge
	- ถาม feature
	- compare version
	- upgrade
- game-developer
	- design game system
	- ECS
	- multiplayer
	- performance
- unreal-engine-cpp-pro
	- implement class
	- optimize
	- engine-level logic
- unreal-sequencer
	- camera
	- timeline
	- animation sequencing

---
