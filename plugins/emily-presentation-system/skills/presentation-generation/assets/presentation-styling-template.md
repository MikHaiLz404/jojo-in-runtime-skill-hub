# Emily Brand Styling

## Overview

To access Emily's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Emily brand, visual formatting, visual design

## Brand Guidelines

### Colors (Brand Palette Update)

**Main Colors:**
- **Dark (Text Primary)**: `#333333` — main content   
- **Light (Main Background)**: `#F4F5F0` — main background (Pantone 2026 Cloud Dancer)    
- **Card Background**: `#FFFFFF` — card element background    
- **Secondary Text**: `#777777` — description or taglines

```palette
#333333, #F4F5F0, #FFFFFF, #777777
```

**Accent Colors (Semantic — 4 roles only):**
- **Mint Green (ACTIVE)**: `#A7D7C5` — interactive states: 
  active tabs, selected filters, progress fills, card borders
- **Blue (POSITIVE)**: `#4A80C4` — healthy data, on-track metrics, 
  LOW-risk items, completion values, TODAY marker  
- **Gold (MILESTONE)**: `#C9A227` — key dates, milestones, 
  deadlines, IN-PROGRESS status tags
- **Coral (ALERT)**: `#ED7D63` — concerns, HIGH-risk, 
  stats that need attention

```palette
#A7D7C5, #4A80C4, #C9A227, #ED7D63
```

**Neutral Decorative (backgrounds only — not used as a 5th signal color):**
- **Mint Light** `#C8E6C9` — tint for interactive surface backgrounds
- **Gold Light** `#F5E6B0` — warm tint for milestone area backgrounds

```palette
#C8E6C9, #F5E6B0
```

---
### Typography
- **Headings**: **Inter** or **Poppins** (Bold 700) - Color: `#5D2036` (Dusky Plum)
- **Body Text**: **Inter** or **Lora** (Regular) - Color: `#333333`
- **Technical/Code**: **Fira Code** or **Courier New** - Color: `#4af626` (on dark)

```palette
#5D2036, #333333, #4af626
```

---

### Visual Features (Layout & UI)

- **Card-Based Design**: Each section is wrapped in a card with `border-radius: 16px` and a `shadow-soft` to create a sense of depth
- **Status Badges**: Uses `Mint Light (#C8E6C9)` with dark green text to indicate statuses like "Active" or "Success"    
- **Progress Indicators**: Category-based colors (Peach/Blue/Lavender) are used to display progress bars 
- **Interactive Hover**: On hover, elements slightly lift with `translateY(-2px)` and gain additional shadow to mimic a real button feel

---

### Trend Palette)
**Main Canvas & Surfaces:**
- **Primary BG**: `#F4F5F0` (Cloud Dancer) - Main background
- **Card BG**: `#FFFFFF` (Pure White) - Section backgrounds
- **Soft UI Highlight**: `#F4E5C3` (Lemon Icing) - For subtle highlights

```palette
#F4F5F0, #FFFFFF, #F4E5C3
```

**Accent & Status Colors:**
- **Active/Uptime**: `#A7D7C5` (Mint Green) - Primary accent
- **CPU/Trend Up**: `#D27D56` (Sunlit Terracotta) - Warning/High load
- **RAM/Memory**: `#BDE0FE` (Baby Blue) - System data
- **Disk/Storage**: `#A89ACD` (Digital Lavender) - Tech/Future feel
- **Special Accent**: `#2E7F7F` (Transformative Teal) - Deep interaction

```palette
#A7D7C5, #D27D56, #BDE0FE, #A89ACD, #2E7F7F
```

---

## Color Usage Mapping

### Layout & Surface
- **Main Background**: Use `#F4F5F0` for the entire canvas.
- **Sectioning**: Use `#FFFFFF` for cards with `16px` border-radius and `0 4px 12px rgba(0,0,0,0.03)` shadow.

```palette
#F4F5F0, #FFFFFF
```

### Typography & Hierarchy
- **Title/Header**: Use `#5D2036` to create a "Quiet Luxury" look for main titles.
- **Content**: Use `#333333` for high readability.
- **Secondary Info**: Use `#777777` for captions and timestamps.

```palette
#5D2036, #333333, #777777
```
### System & Interaction
- **Success States**: Apply `#A7D7C5` for active agents or completed tasks.
- **Data Points**: 
	- CPU Metrics -> `#D27D56`
	- Memory Usage -> `#BDE0FE`
	- Disk Space -> `#A89ACD`
- **Buttons/Skills**: Use `#C8E6C9` (Mint Light) with `#276948` text.

```palette
#A7D7C5, #D27D56, #BDE0FE, #A89ACD, #C8E6C9, #276948
```

---

### Dashboard Color Rules

**Rule 1 — One hue per role, always:**  
- All colors must be in 4 roles related from **Accent Colors** 
- Add new hue is not allow even though decorative

**Rule 2 — Surface vs. value:**  
- Light tint (`#C8E6C9`, `#F5E6B0`) = use for background / icon bg  
- Full color (`#A7D7C5`, `#4A80C4`, `#C9A227`, `#ED7D63`) = use for text / border / chart line

```palette
#C8E6C9, #F5E6B0, #A7D7C5, #4A80C4, #C9A227, #ED7D63
```

**Rule 3 — Gantt / chart discipline colors:**  
- Character / Art tracks → Mint Green  
- Programming / Tech tracks → Mint Light  
- Design / UX tracks → Gold Light  
- Animation tracks → Gold  
- Milestone diamonds → Gold  

**Rule 4 — Status text colors:**  
- ACHIEVED / MOSTLY DONE / PROGRESSING → Blue `#4A80C4`  
- IN PROGRESS / STARTED → Gold `#C9A227`  
- STUCK / BLOCKED → Coral `#ED7D63`  
- WON'T DO / DESCOPED → Gray `#9ca3af`

```palette
#4A80C4, #C9A227, #ED7D63, #9ca3af
```

---

### Technical Implementation

- **Border Radius**: Keep it soft with a fixed value of `16px`    
- **Spacing**: Use a single-column grid Layout for Mobile, and two columns for desktop (min-width: 768px)    
- **Shadows**: Keep it minimal with `0 4px 12px rgba(0, 0, 0, 0.03)`

---