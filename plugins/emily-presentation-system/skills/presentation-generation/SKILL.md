---
name: presentation-generation
description: This skill is used to **structure and write presentation slides** based on given content, insights, or data
model: sonnet
tools: Read
tags:
  - skill
  - presentation
  - google
  - microsoft
  - slide
  - powerpoint
author: emily club
version: 1.1.0
updated: 2026-03-25
---
# PPT generation

## Overview

This skill is used to **structure and write presentation slides** based on given content, insights, or data.

### It focuses on:
- slide structure
- content clarity
- layout suggestion
- storytelling flow in presentation format

### File & Folder structure
- /emily-presentation-system/templates/ Template or static files required for the task

---

## Rules
- Each slide must have a title
- Use bullet points instead of paragraphs
- Keep content concise
- Maintain logical order of slides

---

> [!NOTE]
## Use When

Use this skill when:

- converting ideas into slides
- structuring presentation decks
- organizing content into sections (title, content, summary)
- preparing pitch decks, reports, or internal presentations

---

> [!IMPORTANT]
## DO NOT USE WHEN

- writing raw code or scripts  
- designing charts in detail (use visualization-expert instead)  
- creating narrative from raw data (use data-storytelling instead)  
- generating or exporting actual files (.pptx, Google Slides, etc.)  
- executing tools or automations  

---

> [!CAUTION]
## Safety Rules

This skill must NOT:

- execute code  
- create, write, or export files  
- access local or remote data sources  
- call external tools or APIs  
- retrieve secrets or system information  

This skill is **content-only** and does not perform any real-world actions.

---

## Responsibilities

### 1. Template Selection
- Use "data-driven-template" for analytical, insight-based, or strategic presentations
- Use "sprint-report-template" for team updates, sprint reports, or progress tracking

---

### 2. Presentation style
- Use presentation-styling-template for all presentations
---

### 3. Content Formatting
- concise bullet points
- clear hierarchy
- readable phrasing
- avoiding clutter

---

### 4. Layout Suggestions
- text vs visual balance
- where to place charts/images
- emphasis areas (headline, key numbers)

---

### 5. Presentation Flow
- logical progression
- pacing (1 idea per slide)
- strong opening & closing

---

## Collaboration with Other Skills

### With data-storytelling
- data-storytelling → defines narrative  
- emily-presentation-generation → converts narrative into slides  

---

### With visualization-expert
- visualization-expert → selects chart type  
- emily-presentation-generation → places chart into slide context  

---

## Modes (Optional)

- Quick Mode → 3–5 slides summary  
- Standard Mode → 6–10 slides  
- Detailed Mode → 10–15 slides full deck  

---

## Output Schema

All generated slide content must follow this structure:

```json  
{  
"slides": [  
{  
"title": "Slide title",  
"bullets": [  
"Point 1",  
"Point 2"  
]  
}  
]  
}