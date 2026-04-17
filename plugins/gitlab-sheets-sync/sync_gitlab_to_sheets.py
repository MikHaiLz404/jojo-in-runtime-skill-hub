#!/usr/bin/env python3
"""
GitLab Issues → Google Sheets Sync Plugin

Fetches issues from GitLab and syncs to Google Sheets.
Run: python3 sync_gitlab_to_sheets.py

Requirements:
- GitLab MCP server running (or set GITLAB_URL + GITLAB_TOKEN env vars)
- Google Sheets API enabled + service account with write access
"""

import json
import os
import sys
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# === Configuration ===
GITLAB_URL = os.environ.get('GITLAB_URL', '')
GITLAB_TOKEN = os.environ.get('GITLAB_TOKEN', '')  # Set if GitLab MCP not available
GITLAB_PROJECT = os.environ.get('GITLAB_PROJECT', 'jumbojumps/rp')

SERVICE_ACCOUNT_FILE = 'api/claude-service-account.json'
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', '')
SHEET_NAME = 'GitLab_Issues'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CONFIG_FILE = 'data/sync_config.json'


def fetch_gitlab_issues_via_api():
    """Fetch issues directly from GitLab API (fallback if MCP not available)"""
    if not GITLAB_TOKEN:
        print("GITLAB_TOKEN not set. Using MCP...")
        return None

    url = f"{GITLAB_URL}/api/v4/projects/{GITLAB_PROJECT.replace('/', '%2F')}/issues"
    headers = {'PRIVATE-TOKEN': GITLAB_TOKEN}
    params = {'state': 'opened', 'per_page': 100}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching GitLab issues: {e}")
        return None


def format_issues(issues):
    """Format GitLab issues for Google Sheet"""
    headers = ['IID', 'Title', 'Description', 'State', 'Labels', 'Milestone', 'Assignee', 'Author', 'Due Date', 'URL']
    values = [headers]

    for issue in issues:
        labels = ', '.join(issue.get('labels', []))
        milestone = issue.get('milestone', {}).get('title', '') if issue.get('milestone') else ''
        assignees = issue.get('assignees', [])
        assignee = ', '.join([a.get('name', '') for a in assignees]) if assignees else ''
        if not assignee and issue.get('assignee'):
            assignee = issue.get('assignee', {}).get('name', '')
        author = issue.get('author', {}).get('name', '')
        due_date = issue.get('due_date', '') or ''
        web_url = issue.get('web_url', '')

        description = issue.get('description', '') or ''
        if len(description) > 200:
            description = description[:200] + '...'

        values.append([
            f"#{issue.get('iid', '')}",
            issue.get('title', ''),
            description,
            issue.get('state', ''),
            labels,
            milestone,
            assignee,
            author,
            due_date,
            web_url
        ])

    return values


def get_gitlab_issues_from_mcp():
    """Placeholder for GitLab MCP integration"""
    # This script can be called by Claude Code which has GitLab MCP
    # Just load from pre-fetched data if available
    try:
        with open('data/gitlab_issues.json', 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return data.get('issues', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def create_or_clear_sheet(service):
    """Create sheet if not exists, clear data"""
    spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    existing_sheets = [s['properties']['title'] for s in spreadsheet.get('sheets', [])]

    if SHEET_NAME not in existing_sheets:
        body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': SHEET_NAME,
                        'index': len(existing_sheets)
                    }
                }
            }]
        }
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        print(f"Created sheet: {SHEET_NAME}")
    else:
        print(f"Sheet {SHEET_NAME} already exists")


def load_config():
    """Load saved configuration"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_config(config):
    """Save configuration"""
    os.makedirs('data', exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def interactive_setup():
    """Guide user through first-time setup"""
    print("=" * 60)
    print("🔧 GitLab → Google Sheets Sync Setup")
    print("=" * 60)

    config = load_config()

    # Ask for GitLab URL
    print("\n📌 GitLab Configuration")
    default_gitlab = config.get('GITLAB_URL', 'http://')
    gitlab_url = input(f"   GitLab URL/IP [{default_gitlab}]: ").strip()
    if not gitlab_url:
        gitlab_url = default_gitlab

    # Ask for GitLab Project
    default_project = config.get('GITLAB_PROJECT', 'jumbojumps/rp')
    gitlab_project = input(f"   GitLab Project [{default_project}]: ").strip()
    if not gitlab_project:
        gitlab_project = default_project

    # Ask for Spreadsheet ID
    print("\n📌 Google Spreadsheet Configuration")
    default_spreadsheet = config.get('SPREADSHEET_ID', '')
    if not default_spreadsheet:
        spreadsheet_id = input("   Spreadsheet ID (from URL): ").strip()
    else:
        spreadsheet_id = input(f"   Spreadsheet ID [{default_spreadsheet}]: ").strip()
        if not spreadsheet_id:
            spreadsheet_id = default_spreadsheet

    # Save config
    config = {
        'GITLAB_URL': gitlab_url,
        'GITLAB_PROJECT': gitlab_project,
        'SPREADSHEET_ID': spreadsheet_id,
        'SERVICE_ACCOUNT_FILE': SERVICE_ACCOUNT_FILE
    }
    save_config(config)

    print("\n✅ Configuration saved!")
    print(f"   GitLab: {gitlab_url}")
    print(f"   Project: {gitlab_project}")
    print(f"   Spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

    print("\n" + "=" * 60)
    print("⚠️  NEXT STEPS:")
    print("=" * 60)
    print("""
1. Google Sheets API:
   - Enable: https://console.cloud.google.com/apis/library/sheets.googleapis.com
   - Share spreadsheet with: claude@project-management-492603.iam.gserviceaccount.com

2. Service Account Key:
   - Download from: Google Cloud Console → IAM → Service Accounts → Keys
   - Save as: api/claude-service-account.json

3. GitLab MCP (optional):
   - Run: claude mcp add --transport http GitLab {}/api/v4/mcp
""".format(gitlab_url))
    print("=" * 60)

    return False


def check_setup():
    """Check if setup is complete, guide user if not"""
    global GITLAB_URL, SPREADSHEET_ID

    # Load saved config
    config = load_config()
    GITLAB_URL = config.get('GITLAB_URL', '') or os.environ.get('GITLAB_URL', '')
    SPREADSHEET_ID = config.get('SPREADSHEET_ID', '') or os.environ.get('SPREADSHEET_ID', '')

    # If no config, run interactive setup (only if run with --setup)
    if not GITLAB_URL or not SPREADSHEET_ID:
        if '--setup' in sys.argv or '--interactive' in sys.argv:
            return interactive_setup()
        else:
            print("=" * 60)
            print("⚠️  SETUP REQUIRED")
            print("=" * 60)
            print("\nRun with --setup to configure:")
            print("   python3 sync_gitlab_to_sheets.py --setup")
            print("=" * 60)
            return False

    issues = None
    missing = []

    # Check GitLab connection
    try:
        issues = get_gitlab_issues_from_mcp()
        if issues is None:
            # Try direct API
            issues = fetch_gitlab_issues_via_api()
    except Exception:
        pass

    if issues is None:
        missing.append(f"GitLab ({GITLAB_URL}) - check connection")

    # Check Google Sheets connection
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build('sheets', 'v4', credentials=creds)
        service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    except FileNotFoundError:
        missing.append(f"Service account key (save as {SERVICE_ACCOUNT_FILE})")
    except Exception as e:
        if "not found" in str(e).lower() or "permission" in str(e).lower():
            missing.append(f"Google Sheets access - check spreadsheet ID and sharing")
        else:
            missing.append(f"Google Sheets ({str(e)[:50]})")

    if missing:
        print("=" * 60)
        print("⚠️  SETUP INCOMPLETE")
        print("=" * 60)
        print("\nMissing components:")
        for i, m in enumerate(missing, 1):
            print(f"  {i}. {m}")
        print("\n📖 See docs/GITLAB-SHEETS-SYNC.md for setup instructions")
        print("\n💡 Or run setup again: python3 sync_gitlab_to_sheets.py --setup")
        print("=" * 60)
        return False

    return True


def sync():

    # Check setup first
    if not check_setup():
        sys.exit(1)

    # Try to get issues
    issues = None

    # 1. Try GitLab MCP data (pre-fetched by Claude)
    issues = get_gitlab_issues_from_mcp()

    # 2. Fallback: Direct GitLab API
    if issues is None:
        print("Fetching from GitLab API...")
        issues = fetch_gitlab_issues_via_api()

    if issues is None:
        print("ERROR: Could not fetch GitLab issues. Set GITLAB_TOKEN or use GitLab MCP.")
        sys.exit(1)

    print(f"Found {len(issues)} issues")

    # Load service account
    print("Loading service account...")
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    print("Building Google Sheets service...")
    service = build('sheets', 'v4', credentials=creds)

    # Create/clear sheet
    create_or_clear_sheet(service)

    # Format data
    values = format_issues(issues)
    print(f"Formatted {len(values)} rows (including header)")

    # Clear existing data
    print(f"Clearing {SHEET_NAME}...")
    try:
        service.spreadsheets().values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A1:Z1000'
        ).execute()
    except Exception:
        pass

    # Write to sheet
    range_name = f'{SHEET_NAME}!A1:J{len(values)}'
    body = {'values': values}

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    print(f"Updated cells: {result.get('updatedCells')}")
    print("=" * 50)
    print(f"SUCCESS: {len(issues)} issues synced!")
    print(f"URL: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
    print("=" * 50)


if __name__ == '__main__':
    if '--setup' in sys.argv or '--interactive' in sys.argv:
        interactive_setup()
    else:
        sync()