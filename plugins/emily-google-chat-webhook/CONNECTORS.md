# Connectors

## How tool references work

Plugin files use `~~space-name` as a placeholder for the user's own Google Chat webhook preset names. Each user stores their own webhook URLs locally — nothing is shared.

## Setup required

| What | Placeholder | How to get it |
|------|-------------|---------------|
| Google Chat Webhook URL | `~~webhook-url` | Google Chat Space → Apps & integrations → Add webhooks |
| Space preset name | `~~space-name` | Any name you choose (e.g. `dev`, `alerts`, `daily`) |

## Adding your first webhook

```bash
python3 <skill-scripts-dir>/manage_webhooks.py add \
  --name "~~space-name" \
  --url "~~webhook-url"
```

## No external MCP required

This plugin works entirely with built-in tools (Bash + Python stdlib). No additional MCP servers needed.
