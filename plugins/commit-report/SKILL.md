---
name: commit-report
description: >
  Generates a comprehensive .xlsx PR/commit report for any type of Unity game commit —
  balance data, code, prefabs, scenes, animations, or VFX. Adapts the report automatically
  based on what changed. Use for any request involving reviewing what a commit or PR did,
  summarizing for DEV/QA/GD/Producer, or finding team member commits.
  Triggers on: "ดู commit", "สรุป PR", "commit เปลี่ยนอะไร", "ทำ report จาก commit",
  "PR นี้มีอะไรบ้าง", "หา commit ของ [ชื่อ]", "commit ล่าสุดของ designer",
  "what changed in this PR", "summarize this commit for QA", "PR report",
  "commit ของ [ชื่อคน]", or any request to review or report on what a commit/PR changed.
---

# Commit Report Skill

Pulls any commit from the project's git history and generates a **`.xlsx` report** tailored to
what actually changed — balance values, code, prefabs, scenes, animations, or VFX.
The report adapts automatically: only sheets relevant to the commit's content are included.

**Repo:** `/sessions/modest-relaxed-albattani/mnt/project-rp`  
**Script:** `/sessions/modest-relaxed-albattani/mnt/rp-data-analysis/.claude/skills/commit-report/scripts/generate_xlsx.py`  
**Config:** `/sessions/modest-relaxed-albattani/mnt/rp-data-analysis/.claude/skills/commit-report/config.json`

---

## ⚙️ Step 0 — Check Config

Read `config.json`. If it doesn't exist, ask the user:
1. Designer/team member names (as they appear in git)
2. Repo path (default: `/sessions/modest-relaxed-albattani/mnt/project-rp`)
3. Output folder (default: `/sessions/modest-relaxed-albattani/mnt/rp-data-analysis/`)

Save to `config.json` and confirm to the user.

---

## 🔍 Step 1 — Find the commit

**If user gives a commit hash** → skip to Step 2.

**If user mentions a name or says "ล่าสุด"** → run:
```bash
cd <repo_path>
git log --merges --format="%h | %an | %ad | %s" --date=short --all | head -20
```
Filter by the person's name (from config `designer_team` or what the user said).  
Auto-select the most recent match. Show the list only if nothing matches.

---

## 🔎 Step 2 — Detect what type of commit this is

Run the script with `--detect` to see what file types changed:

```bash
python .../generate_xlsx.py --repo <path> --commit <hash> --detect
```

This prints a summary like:
```
FILE TYPES CHANGED:
  .asset    : 23 files  → Balance / Game Data
  .cs       :  5 files  → Code / Feature
  .prefab   :  2 files  → Prefab / Scene
  .anim     :  0 files
  .vfxgraph :  0 files
```

Use this to decide which sheets to generate.

---

## 📊 Step 3 — Generate the .xlsx (main output)

```bash
python .../generate_xlsx.py \
  --repo <repo_path> \
  --commit <hash> \
  --output-dir <output_folder from config>
```

The script **auto-detects** which file types are present and generates only relevant sheets:

| Sheet | When included | Audience |
|---|---|---|
| 📋 PR Overview | Always | Producer / Lead |
| ⚖️ Balance Changes | `.asset` files with RawValues | Game Designer, QA |
| 💻 Code Changes | `.cs` files | DEV, QA |
| 🎮 Prefab / Scene | `.prefab` or `.unity` files | DEV, QA |
| 🎬 Animation / VFX | `.anim`, `.controller`, `.vfxgraph` files | QA, GD |
| ✅ QA Checklist | Always | QA |

**Sheet contents by type:**

### 📋 PR Overview (always)
- Commit hash, ticket, branch, author, date, approved-by
- Table: file type → count of files changed → key summary
- Risk level: 🔴 High / 🟡 Medium / 🟢 Low (based on scope + types changed)

### ⚖️ Balance Changes
- Asset name, field name, before → after value (converted from Fixed-Point ÷ 65536)
- Color coded: red = harder, green = easier, blue = new field

### 💻 Code Changes
- File path (shortened to `System/Domain/ClassName.cs`)
- Lines added / removed
- Classes and systems affected (extracted from diff)
- Type: Modified / Added / Deleted

### 🎮 Prefab / Scene Changes
- Prefab/scene name
- Type: Modified / Added / Deleted
- Objects added or removed (from `m_Name:` in Unity YAML)
- Components changed

### 🎬 Animation / VFX Changes
- Clip/graph name (from file path)
- File type (.anim / .controller / .vfxgraph)
- Type: Modified / Added

### ✅ QA Checklist
Auto-generated from ALL change types:
- Balance → test value ranges and feel
- Code → test affected systems/features
- Prefab → test object placement and components
- Animation → play-test relevant animations
- Priority: 🔴 High / 🟡 Medium / 🟢 Low

---

## 📄 Naming Convention

| Situation | Format | Example |
|---|---|---|
| Single commit with ticket | `{TICKET}_{YYYYMMDD}.xlsx` | `RP-7088_20260326.xlsx` |
| Single commit no ticket | `balancing_{COMMIT}_{YYYYMMDD}.xlsx` | `balancing_9754bea_20260326.xlsx` |
| Comparison (2 commits) | `compare_{A}_vs_{B}_{YYYYMMDD}.xlsx` | `compare_RP-6894_vs_RP-7088_20260317.xlsx` |

---

## 📤 Step 4 — Share the result

Give the user a `computer://` link to open the file. Then give a 2–3 sentence summary:
- What type of commit this was (balance / code / mixed)
- The biggest changes (top 2–3)
- Any risk flags for QA

---

## Unity Fixed-Point (for Balance sheet)

Divide `RawValue` by **65536**. E.g. `491520000 → 7500`, `11796480 → 180s`

---

## Comparison mode

Run script twice → combine with a custom comparison script. Save as `compare_{A}_vs_{B}_{DATE}.xlsx`.
Always include a QA Checklist sheet with a "Commit" column.

---

## Edge cases

- **Code-only commit** → no Balance sheet, show Code + QA only
- **No `.asset` RawValues found** → note it; may be structural Unity data, not balance
- **Script fails** → fix error and retry; never skip to manual xlsx
- **"setup" or "reconfigure"** → delete config.json and re-run setup
