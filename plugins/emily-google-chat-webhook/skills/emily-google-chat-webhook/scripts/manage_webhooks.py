#!/usr/bin/env python3
"""
emily-google-chat-webhook / manage_webhooks.py
จัดการ preset ของ Google Chat webhook URL (list / add / remove / test / show)

Config file: ~/.config/emily-gchat/webhooks.json (chmod 600)

Usage:
    manage_webhooks.py list
    manage_webhooks.py add --name dev --url "https://chat.googleapis.com/..." --description "Dev alerts"
    manage_webhooks.py remove --name dev
    manage_webhooks.py show --name dev
    manage_webhooks.py test --name dev
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

CONFIG_DIR = Path.home() / ".config" / "emily-gchat"
CONFIG_PATH = CONFIG_DIR / "webhooks.json"


def _eprint(*args, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)


def _load() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {"spaces": {}}
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        _eprint(f"❌ Config ไม่ valid JSON: {e}")
        sys.exit(1)
    data.setdefault("spaces", {})
    return data


def _save(data: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    # chmod 700 on directory
    os.chmod(CONFIG_DIR, stat.S_IRWXU)
    tmp = CONFIG_PATH.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(CONFIG_PATH)
    # chmod 600 on file (secret inside)
    os.chmod(CONFIG_PATH, stat.S_IRUSR | stat.S_IWUSR)


def _mask_url(url: str) -> str:
    """Show enough to identify, hide the key/token."""
    if "?" in url:
        base, _ = url.split("?", 1)
        return f"{base}?…[hidden]"
    return url[:60] + "…"


# ---------- commands ----------

def cmd_list(args: argparse.Namespace) -> int:
    data = _load()
    spaces = data["spaces"]
    if not spaces:
        print("🌸 ยังไม่มี preset เลย — ลอง: manage_webhooks.py add --name ... --url ...")
        return 0
    print(f"🌸 เก็บไว้ {len(spaces)} preset ที่ {CONFIG_PATH}\n")
    for name, info in spaces.items():
        desc = info.get("description", "")
        print(f"  • {name}")
        if desc:
            print(f"      {desc}")
        print(f"      URL: {_mask_url(info['url'])}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    if not args.url.startswith("https://chat.googleapis.com/"):
        _eprint("⚠️  URL ไม่ได้ขึ้นต้นด้วย https://chat.googleapis.com/ — เป็น Google Chat webhook จริงไหม?")
    data = _load()
    if args.name in data["spaces"] and not args.force:
        _eprint(f"❌ Preset '{args.name}' มีอยู่แล้ว — ใช้ --force เพื่อเขียนทับ")
        return 1
    data["spaces"][args.name] = {
        "url": args.url,
        "description": args.description or "",
    }
    _save(data)
    print(f"✅ เพิ่ม preset '{args.name}' สำเร็จ")
    print(f"   Config: {CONFIG_PATH} (chmod 600)")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    data = _load()
    if args.name not in data["spaces"]:
        _eprint(f"❌ Preset '{args.name}' ไม่พบ")
        return 1
    del data["spaces"][args.name]
    _save(data)
    print(f"✅ ลบ preset '{args.name}' เรียบร้อย")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    data = _load()
    info = data["spaces"].get(args.name)
    if not info:
        _eprint(f"❌ Preset '{args.name}' ไม่พบ")
        return 1
    print(f"🌸 Preset: {args.name}")
    print(f"   Description: {info.get('description', '(none)')}")
    if args.reveal:
        print(f"   URL: {info['url']}")
    else:
        print(f"   URL: {_mask_url(info['url'])}")
        print("   (ใช้ --reveal เพื่อแสดง URL เต็ม)")
    return 0


def cmd_test(args: argparse.Namespace) -> int:
    data = _load()
    info = data["spaces"].get(args.name)
    if not info:
        _eprint(f"❌ Preset '{args.name}' ไม่พบ")
        return 1

    payload = {
        "text": f"🌸 _ping from emily-google-chat-webhook — preset *{args.name}*_"
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        info["url"],
        data=body,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"✅ Webhook '{args.name}' ใช้งานได้ (HTTP {resp.status})")
            return 0
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        _eprint(f"❌ HTTP {e.code} — webhook ใช้ไม่ได้")
        if err_body:
            _eprint(f"   {err_body[:300]}")
        return 3
    except urllib.error.URLError as e:
        _eprint(f"❌ Network error: {e.reason}")
        return 4


# ---------- main ----------

def main() -> int:
    parser = argparse.ArgumentParser(description="จัดการ Google Chat webhook presets")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sp_list = sub.add_parser("list", help="แสดง preset ทั้งหมด")
    sp_list.set_defaults(func=cmd_list)

    sp_add = sub.add_parser("add", help="เพิ่ม preset ใหม่")
    sp_add.add_argument("--name", required=True, help="ชื่อ preset (เช่น dev, daily)")
    sp_add.add_argument("--url", required=True, help="Webhook URL")
    sp_add.add_argument("--description", help="คำอธิบายสั้น ๆ")
    sp_add.add_argument("--force", action="store_true", help="เขียนทับถ้ามีอยู่แล้ว")
    sp_add.set_defaults(func=cmd_add)

    sp_rm = sub.add_parser("remove", help="ลบ preset")
    sp_rm.add_argument("--name", required=True)
    sp_rm.set_defaults(func=cmd_remove)

    sp_show = sub.add_parser("show", help="ดู detail ของ preset")
    sp_show.add_argument("--name", required=True)
    sp_show.add_argument("--reveal", action="store_true", help="แสดง URL เต็ม (ระวัง!)")
    sp_show.set_defaults(func=cmd_show)

    sp_test = sub.add_parser("test", help="ส่ง ping message เพื่อทดสอบ webhook")
    sp_test.add_argument("--name", required=True)
    sp_test.set_defaults(func=cmd_test)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
