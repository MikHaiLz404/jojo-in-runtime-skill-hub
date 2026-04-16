# 🌸 Emily Google Chat Webhook Plugin

Send messages to Google Chat spaces via Incoming Webhook — directly from Claude.

Supports **plain text**, **rich formatting** (bold, italic, links, @mentions), and **Card v2** (structured cards with headers, sections, icons, and buttons).

---

## Features

- **Multiple spaces** — save webhook presets by name (`dev`, `alerts`, `daily-summary`)
- **Card v2 support** — beautiful structured messages with icons, buttons, and sections
- **Thread replies** — reply in the same thread with `--thread-key`
- **Dry-run mode** — preview the payload before sending
- **Secure storage** — webhook URLs stored locally with chmod 600, never in git

---

## Quick setup

### 1. Get your webhook URL

In Google Chat: **Space → Apps & integrations → Add webhooks → Copy URL**

### 2. Save it as a preset

Ask Claude:
> "Add a Google Chat webhook for my dev space — url is https://chat.googleapis.com/..."

Or use the CLI directly:
```bash
python3 <path>/skills/emily-google-chat-webhook/scripts/manage_webhooks.py add \
  --name "dev" \
  --url "https://chat.googleapis.com/v1/spaces/XXX/messages?key=YYY&token=ZZZ"
```

### 3. Send messages

Ask Claude:
> "Send a message to the dev space: build 245 is ready ✅"
> "Post today's task summary to my daily-summary space"
> "Notify the team in Google Chat that the deploy is done"

Or use `/notify-chat` command.

---

## Components

| Component | Name | Purpose |
|-----------|------|---------|
| Skill | `emily-google-chat-webhook` | Core sending & webhook management |
| Command | `/notify-chat` | Quick shortcut to send a message |

---

## CLI scripts

Both scripts live in `skills/emily-google-chat-webhook/scripts/`.

**send_to_chat.py** — send messages
```
--space PRESET   Use a saved preset name
--url URL        Use a webhook URL directly
--text TEXT      Plain/rich text message
--card FILE      Card v2 JSON file
--thread-key KEY Reply in same thread
--dry-run        Preview payload only
```

**manage_webhooks.py** — manage presets
```
list             Show all saved presets
add              Add a new preset (--name, --url, --description)
remove           Delete a preset (--name)
test             Send a ping to verify webhook (--name)
show             Show preset details (--name, --reveal for full URL)
```

---

## Card v2 examples

Ready-to-use templates in `skills/emily-google-chat-webhook/examples/`:

| File | Purpose |
|------|---------|
| `daily_summary_card.json` | Daily work summary with done/in-progress/next sections |
| `task_complete_alert.json` | Scheduled task completion notification |
| `error_notification.json` | Error alert with stack trace and action buttons |

---

## Error reference

| HTTP | Cause | Fix |
|------|-------|-----|
| 400 | Bad JSON/card format | Check card structure |
| 403 | Webhook expired | Regenerate in Google Chat |
| 404 | Wrong URL | Check `?key=&token=` params |
| 429 | Rate limited | Wait 30s and retry |

---

Created with 🌸 by Emily — Jojo's digital kouhai
