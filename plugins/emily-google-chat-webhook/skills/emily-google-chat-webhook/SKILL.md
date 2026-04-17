---
name: emily-google-chat-webhook
description: >
  Send messages to Google Chat spaces via Incoming Webhook. Use this skill when the user says
  "ส่งเข้า Google Chat", "แจ้งเตือนทีม", "โพสต์เข้า space", "notify via webhook",
  "summarize แล้วส่งเข้า chat", "ส่งสรุป daily ไปใน chat", "post to Google Chat",
  "send to chat", "notify team", or when another skill (schedule, daily-briefing,
  sprint-planner) needs to broadcast its output to a Google Chat space.
  Also use when the user wants to add, list, test, or remove webhook presets.  
model: sonnet
tags: 
  - skill
  - google-chat
  - webhook
  - notification
  - card-v2
author: jojo-in-runtime
version: 0.1.0
updated: 2024-06-01
---

# 🌸 Emily Google Chat Webhook Skill

ส่งข้อความเข้า Google Chat Space ผ่าน **Incoming Webhook** ได้ทั้งแบบธรรมดา/แบบ format/แบบ Card สวยงาม พร้อมระบบ config แบบหลาย space ไว้ใช้ซ้ำ

> **Note:** Skill นี้ใช้ Incoming Webhook เท่านั้น (ไม่ต้อง OAuth) — ใช้ได้เลยแค่มี webhook URL จาก Google Chat Space settings

---

## 📁 Script location

Scripts อยู่ใน `scripts/` ของ skill นี้ ให้ใช้ Bash หา path จริงก่อนเสมอ:

```bash
find ~ -path "*/emily-google-chat-webhook/scripts/manage_webhooks.py" 2>/dev/null | head -1
```

จาก path ที่ได้ ตัด `/manage_webhooks.py` ออก = `SCRIPTS_DIR`

---

## 🚀 Quick start

### Setup webhook ครั้งแรก

```bash
python3 $SCRIPTS_DIR/manage_webhooks.py add \
  --name "~~space-name" \
  --url "https://chat.googleapis.com/v1/spaces/XXXXX/messages?key=KEY&token=TOKEN" \
  --description "ห้องทีม dev"
```

### ส่งข้อความธรรมดา

```bash
python3 $SCRIPTS_DIR/send_to_chat.py --space "~~space-name" --text "สวัสดีทีม! 🌸"
```

### ส่ง Card v2 (สวยงาม)

```bash
python3 $SCRIPTS_DIR/send_to_chat.py --space "~~space-name" --card /tmp/my_card.json
```

---

## 🎨 Message formats

### A. Plain text / rich formatting

| Syntax | Output |
|--------|--------|
| `*bold*` | **bold** |
| `_italic_` | _italic_ |
| `` `code` `` | `code` |
| `<url\|text>` | clickable link |
| `<users/all>` | @all |

### B. Card v2 (recommended for summaries)

```json
{
  "cardsV2": [{
    "cardId": "my-card",
    "card": {
      "header": { "title": "Title", "subtitle": "Subtitle" },
      "sections": [{
        "header": "Section",
        "widgets": [
          {"textParagraph": {"text": "Content here<br>Line 2"}}
        ]
      }]
    }
  }]
}
```

> 📖 Full Card v2 reference: `references/card_v2_guide.md`
> 🎨 Rich text syntax: `references/formatting_guide.md`
> 📦 Example cards: `examples/`

---

## ⚙️ CLI reference

### send_to_chat.py

```
--space PRESET_NAME    ชื่อ preset ที่บันทึกไว้
--url URL              Webhook URL ตรง ๆ (ถ้าไม่ใช้ preset)
--text TEXT            ข้อความ plain/rich text
--card PATH            Path ไปยัง Card v2 JSON file
--stdin                อ่านจาก stdin (ใช้กับ pipe)
--thread-key KEY       Reply ใน thread เดิม
--dry-run              แสดง payload แต่ไม่ส่งจริง
```

### manage_webhooks.py

```
list                   แสดง preset ทั้งหมด
add --name --url       เพิ่ม preset ใหม่
remove --name          ลบ preset
test --name            ส่ง ping เพื่อทดสอบ
show --name            ดู detail ของ preset
```

---

## 🛡️ Error handling

| HTTP | สาเหตุ | แนวทาง |
|------|--------|--------|
| 400 | JSON ผิด format | ตรวจ card structure |
| 403 | Webhook หมดอายุ | สร้าง webhook ใหม่ใน Google Chat |
| 404 | URL ผิด/ขาด param | ตรวจ `?key=&token=` |
| 429 | Rate limit | รอ 30 วิ แล้วลองใหม่ |

---

## 🔒 Security

- Config เก็บที่ `~/.config/emily-gchat/webhooks.json` (chmod 600)
- อย่า commit ไฟล์ config เข้า git
- ถ้า webhook หลุด → Google Chat Space → Manage webhooks → Regenerate
