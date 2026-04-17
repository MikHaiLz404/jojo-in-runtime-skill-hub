# GitLab → Google Sheets Sync Plugin

Sync GitLab issues to a Google Spreadsheet automatically.

---

## First-Time Setup

### 1. GitLab MCP Connection

**Option A: Claude Code with MCP (Recommended)**
```bash
claude mcp add --transport http GitLab http://YOUR_GITLAB_IP:PORT/api/v4/mcp
```

Example for your setup:
```bash
claude mcp add --transport http GitLab http://43.164.3.14/api/v4/mcp
```

**Option B: Direct API (No MCP)**
Set `GITLAB_TOKEN` environment variable:
```bash
export GITLAB_TOKEN=your_gitlab_personal_access_token
```

---

### 2. Google Sheets Connection

#### Option A: Claude Code with Google Drive (Recommended)

If you use **Claude Code** with Google Drive connected, just share the spreadsheet with your Google account. The service account will have access through Drive sharing.

1. Share spreadsheet with your Google email
2. That's it! ✓

#### Option B: Standalone Claude Code (Service Account)

If you use **Claude Code standalone** without Google Drive connector:

1. **Enable Google Sheets API**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Select project `project-management-492603`
   - APIs & Services → Library → Enable "Google Sheets API"

2. **Share Spreadsheet with Service Account**
   - Open your spreadsheet
   - Share → Add email: `claude@project-management-492603.iam.gserviceaccount.com`
   - Give "Editor" access

3. **Service Account Key**
   - Download JSON key from Google Cloud Console → IAM → Service Accounts → Keys
   - Save as `api/claude-service-account.json` in project

---

### 3. Update Configuration

Edit `sync_gitlab_to_sheets.py` or set environment variables:

```bash
# Required for direct API (no MCP)
export GITLAB_TOKEN=your_token_here

# Optional (defaults shown)
export GITLAB_URL=http://43.164.3.14
```

Update spreadsheet ID in script if using different spreadsheet:
```python
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE'
```

---

## Usage

```bash
# Via Make
make gitlab-sync

# Direct
python3 sync_gitlab_to_sheets.py
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Permission denied" on spreadsheet | Share spreadsheet with `claude@project-management-492603.iam.gserviceaccount.com` |
| "Caller does not have permission" | Enable Google Sheets API in Google Cloud Console |
| GitLab MCP not found | Run: `claude mcp add --transport http GitLab http://43.164.3.14/api/v4/mcp` |
| No issues found | Check GitLab project path (`jumbojumps/rp`) is correct |

---

## Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  GitLab     │────▶│  GitLab MCP     │────▶│  sync_gitlab_   │
│  Issues     │     │  (or Direct API)│     │  to_sheets.py   │
└─────────────┘     └─────────────────┘     └────────┬─────────┘
                                                     │
                                                     ▼
                                            ┌──────────────────┐
                                            │  Google Sheets   │
                                            │  (Service Account│
                                            │   or OAuth)      │
                                            └──────────────────┘
```

**Connection Methods:**

| Method | Pros | Cons |
|--------|------|------|
| **MCP + Google Drive** | No credentials needed | Requires Claude Code with both MCPs |
| **MCP + Service Account** | Full automation | Requires setup |
| **Direct API + Service Account** | Works standalone | Need GITLAB_TOKEN |
