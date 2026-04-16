# 🎨 Google Chat Rich Text Formatting Guide

Syntax ของ Google Chat คล้าย markdown แต่**ไม่ใช่ markdown เป๊ะ ๆ** — มี quirk หลายอย่าง

## Text styles

| Syntax | Render | Note |
|---|---|---|
| `*bold text*` | **bold text** | ใช้ `*` ไม่ใช่ `**` (ต่างจาก markdown) |
| `_italic text_` | _italic text_ | ใช้ `_` ไม่ใช่ `*` |
| `~strikethrough~` | ~~strikethrough~~ | |
| `` `inline code` `` | `inline code` | |
| ` ```code block``` ` | code block | triple backtick (ไม่ต้องขึ้นบรรทัดใหม่) |

**Combine ได้:** `*_bold italic_*` → ***bold italic***

## Links

```
<https://example.com>
<https://example.com|Click here>
```

- แบบแรก: แสดง URL เต็ม
- แบบสอง: แสดงข้อความแทน

**⚠️ Escape:** ถ้า `|` อยู่ใน URL ต้อง escape เป็น `\|`

## Mentions

| Target | Syntax |
|---|---|
| ทุกคนใน space | `<users/all>` |
| คนที่ online อยู่ | `<users/online>` (บางกรณีใช้ `@here`) |
| User เฉพาะคน | `<users/USER_ID>` |

> **Getting USER_ID**: Google Chat ไม่ expose ง่าย ๆ ต้องใช้ Chat API + OAuth หรือ parse จาก event payload ของ bot — **skill นี้ไม่ทำให้** เพราะเกินขอบเขต webhook

## Line breaks

- ใน `text` field: ใช้ `\n` ปกติ (JSON escape)
- ใน Card v2 `textParagraph`: ใช้ `<br>` (HTML-style)

## Emoji

ใช้ Unicode emoji ตรง ๆ ได้: 🌸 ✅ 🚀 ⚠️ 💧
หรือ `:smile:` format ถ้า space นั้น enable custom emoji

## Common pitfalls

1. **`**bold**` ใช้ไม่ได้** — ใช้ `*bold*`
2. **`# heading` ใช้ไม่ได้** — Google Chat ไม่มี heading ใน plain text; ใช้ Card v2 header widget แทน
3. **`- list` ไม่ render เป็น bullet** — ใช้ Unicode `•` หรือ `◦` เอง
4. **Unicode ไทยยาว ๆ** อาจโดน rate limit ถ้าส่งติด ๆ กัน — skill นี้ไม่ retry, ต้อง space ออกเอง
5. **Quote (`>`)** ไม่รองรับ — ใช้ `_italic_` หรือ code block แทน

## Example: ข้อความ rich formatted

```
*สรุปงาน 16 เม.ย.* 🌸

_Done:_
• Review scene 04
• Sync กับทีม art

_Next:_
• Submit Jira <https://company.atlassian.net/browse/ART-123|ART-123>
• Deploy build 245

cc <users/all> — _estimate: เสร็จก่อน 18:00_
```
