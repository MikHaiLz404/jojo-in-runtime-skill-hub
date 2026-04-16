---
description: Send a message or summary to a Google Chat space via webhook. Use when the user types /notify-chat, "notify chat", "send to chat", or "post to google chat".
tools:
  - Bash
  - Read
---

# /notify-chat

Send a message to a Google Chat space using a saved webhook preset.

## Steps

1. Find the skill scripts directory. Look for `manage_webhooks.py` and `send_to_chat.py` in the plugin's `skills/emily-google-chat-webhook/scripts/` directory. Use Bash to locate it:
   ```bash
   find ~ -path "*/emily-google-chat-webhook/scripts/manage_webhooks.py" 2>/dev/null | head -1
   ```

2. List available spaces:
   ```bash
   python3 <SCRIPTS_DIR>/manage_webhooks.py list
   ```

3. If no presets exist yet, tell the user:
   > "ยังไม่มี webhook preset ค่ะ — รันคำสั่งนี้เพื่อเพิ่ม:
   > `python3 <path>/manage_webhooks.py add --name <ชื่อ> --url <webhook-url>`"

4. Ask the user which space to send to (if not already specified) and what the message should be.

5. Determine message format:
   - Short announcement → plain `--text`
   - Structured summary with sections → build a Card v2 JSON and use `--card`

6. For Card v2: create a temp JSON file at `/tmp/notify_card.json`, then send:
   ```bash
   python3 <SCRIPTS_DIR>/send_to_chat.py --space <name> --card /tmp/notify_card.json
   ```
   For plain text:
   ```bash
   python3 <SCRIPTS_DIR>/send_to_chat.py --space <name> --text "<message>"
   ```

7. Confirm success or report any errors with a suggested fix.
