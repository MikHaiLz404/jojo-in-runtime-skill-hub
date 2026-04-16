# 🪄 Google Chat Card v2 Guide

Card v2 คือ UI framework ของ Google Chat — ใช้สร้าง message ที่มี header, section, button, icon, image

> Reference: <https://developers.google.com/workspace/chat/api/reference/rest/v1/cards>

## Minimum viable card

```json
{
  "cardsV2": [
    {
      "cardId": "my-card-1",
      "card": {
        "sections": [
          {
            "widgets": [
              {"textParagraph": {"text": "Hello *Jojo* 🌸"}}
            ]
          }
        ]
      }
    }
  ]
}
```

> `skill-creator`: `send_to_chat.py --card` รองรับ 2 รูปแบบ — มี `cardsV2` ครอบ หรือไม่มีก็ได้ (จะ auto-wrap ให้)

## Card anatomy

```
cardsV2
  └── [card]
       ├── header           ← รูป + title + subtitle (optional)
       ├── sections[]
       │    ├── header      ← หัวข้อ section (optional)
       │    ├── collapsible: true|false
       │    └── widgets[]
       │         ├── textParagraph
       │         ├── decoratedText
       │         ├── image
       │         ├── divider
       │         ├── buttonList
       │         └── columns
       └── cardActions[]    ← menu เพิ่มเติม (optional)
```

## Header

```json
{
  "header": {
    "title": "สรุปงานรายวัน",
    "subtitle": "16 เมษายน 2026",
    "imageUrl": "https://example.com/icon.png",
    "imageType": "CIRCLE"
  }
}
```

- `imageType`: `"SQUARE"` (default) หรือ `"CIRCLE"`
- `imageUrl` ต้องเป็น HTTPS, public accessible

## Widgets ที่ใช้บ่อย

### textParagraph — ข้อความยาว

```json
{"textParagraph": {"text": "• Review scene 04<br>• Deploy build 245<br>• _Next meeting:_ 2PM"}}
```

- ใช้ `<br>` เป็น newline (ไม่ใช่ `\n`)
- Rich formatting เหมือน plain text (`*bold*`, `_italic_`, `<url|text>`)

### decoratedText — ข้อความ + icon/toggle

```json
{
  "decoratedText": {
    "startIcon": {"knownIcon": "CLOCK"},
    "topLabel": "Deadline",
    "text": "*วันนี้ 18:00*",
    "bottomLabel": "เหลือ 3 ชั่วโมง"
  }
}
```

`knownIcon` ที่มีให้ใช้: `AIRPLANE`, `BOOKMARK`, `BUS`, `CAR`, `CLOCK`, `CONFIRMATION_NUMBER_ICON`, `DOLLAR`, `DESCRIPTION`, `EDIT`, `EMAIL`, `EVENT_SEAT`, `FLIGHT_ARRIVAL`, `FLIGHT_DEPARTURE`, `HOTEL`, `HOTEL_ROOM_TYPE`, `INVITE`, `MAP_PIN`, `MEMBERSHIP`, `MULTIPLE_PEOPLE`, `OFFER`, `PERSON`, `PHONE`, `RESTAURANT_ICON`, `SHOPPING_CART`, `STAR`, `STORE`, `TICKET`, `TRAIN`, `VIDEO_CAMERA`, `VIDEO_PLAY`

### buttonList — ปุ่ม action

```json
{
  "buttonList": {
    "buttons": [
      {
        "text": "ดู Dashboard",
        "onClick": {"openLink": {"url": "https://dashboard.example.com"}}
      },
      {
        "text": "Approve",
        "color": {"red": 0.2, "green": 0.7, "blue": 0.4, "alpha": 1},
        "onClick": {"openLink": {"url": "https://approve.example.com"}}
      }
    ]
  }
}
```

### image

```json
{"image": {"imageUrl": "https://example.com/chart.png", "altText": "Sales chart"}}
```

### divider

```json
{"divider": {}}
```

## Full example — Daily summary card

```json
{
  "cardsV2": [
    {
      "cardId": "daily-summary-2026-04-16",
      "card": {
        "header": {
          "title": "🌸 สรุปงานวันนี้",
          "subtitle": "พฤหัสบดี 16 เม.ย. 2026"
        },
        "sections": [
          {
            "header": "✅ Done (3)",
            "widgets": [
              {"textParagraph": {"text": "• Review animation scene 04<br>• Sync กับทีม art<br>• ปิด Jira ART-118"}}
            ]
          },
          {
            "header": "🚧 In Progress (2)",
            "widgets": [
              {"textParagraph": {"text": "• GDD chapter 3 (70%)<br>• Build pipeline refactor"}}
            ]
          },
          {
            "header": "📌 Next",
            "widgets": [
              {
                "decoratedText": {
                  "startIcon": {"knownIcon": "CLOCK"},
                  "topLabel": "Deadline",
                  "text": "*Submit Jira tickets ก่อน EOD*"
                }
              },
              {
                "buttonList": {
                  "buttons": [
                    {"text": "เปิด Jira", "onClick": {"openLink": {"url": "https://company.atlassian.net"}}}
                  ]
                }
              }
            ]
          }
        ]
      }
    }
  ]
}
```

## Common errors

| Error | สาเหตุ |
|---|---|
| 400 "Invalid JSON payload" | Missing required field — ปกติลืม `cardsV2[].card.sections[]` |
| 400 "Unknown name 'widgets'" | widget alignment ผิด — widgets ต้องอยู่ใน section, ไม่ใช่ card |
| `text` แสดง `<br>` ตรง ๆ | ใช้ `\n` ใน Card v2 — ต้องใช้ `<br>` แทน |
| Icon ไม่ขึ้น | `knownIcon` สะกดผิด (เป็น case-sensitive, ALL_CAPS) |
| Button ไม่ render | `onClick` missing หรือ URL ไม่ใช่ HTTPS |

## Design tips

- **Section ≤ 5** — เกินนั้น scroll เยอะ user ไม่อ่าน
- **Header สั้น** — ใช้ emoji 1 ตัว + หัวข้อ 5-8 คำ
- **Hierarchy ชัด** — ใช้ `decoratedText` แทน bullet plain สำหรับ item สำคัญ
- **Action ≤ 3 ปุ่ม** — ถ้าเยอะไปใช้ `cardActions` menu แทน
- **Mobile-first** — ทดสอบว่าอ่านรู้เรื่องบน phone ด้วย
