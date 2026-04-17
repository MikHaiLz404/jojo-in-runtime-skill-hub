# GitLab → Google Sheets Sync Plugin

Syncs GitLab issues from a project to a Google Spreadsheet automatically.

## Quick Start

```bash
# 1. Navigate to plugin directory
cd plugins/gitlab-sheets-sync

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run setup (first time only)
make setup

# 4. Sync issues to spreadsheet
make sync
```

## Setup Requirements

1. **GitLab MCP or API Token** - For fetching issues
2. **Google Sheets API** - For writing to spreadsheet
3. **Service Account** - JSON key for Google authentication

See [GITLAB-SHEETS-SYNC.md](./GITLAB-SHEETS-SYNC.md) for detailed setup instructions.

## Files

```
gitlab-sheets-sync/
├── sync_gitlab_to_sheets.py   # Main plugin script
├── Makefile                   # CLI shortcuts
├── requirements.txt           # Dependencies
├── GITLAB-SHEETS-SYNC.md      # Setup documentation
├── api/                       # Service account key (add manually)
└── data/                      # Config and cache (created on first run)
```
