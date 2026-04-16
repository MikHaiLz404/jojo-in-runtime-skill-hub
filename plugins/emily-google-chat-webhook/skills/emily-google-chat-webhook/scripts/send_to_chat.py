#!/usr/bin/env python3
"""
emily-google-chat-webhook / send_to_chat.py
ส่งข้อความเข้า Google Chat Space ผ่าน Incoming Webhook

Usage examples:
    # ส่ง text ธรรมดา
    send_to_chat.py --space dev --text "Build สำเร็จแล้วค่ะ ✅"

    # ส่งผ่าน URL ตรง
    send_to_chat.py --url "https://chat.googleapis.com/..." --text "hi"

    # ส่ง Card v2
    send_to_chat.py --space daily --card ./examples/daily_summary_card.json

    # reply ใน thread เดิม
    send_to_chat.py --space dev --text "follow-up" --thread-key "deploy-245"

    # ดู payload แต่ไม่ส่ง (dry-run)
    send_to_chat.py --space dev --text "preview" --dry-run

Exit codes:
    0  = ส่งสำเร็จ (หรือ dry-run เสร็จ)
    1  = argument / config ผิด
    2  = payload ไม่ valid
    3  = HTTP error (4xx / 5xx) จาก Google Chat
    4  = network error (DNS / connection / timeout)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

CONFIG_PATH = Path.home() / ".config" / "emily-gchat" / "webhooks.json"
REQUEST_TIMEOUT_S = 15
MAX_TEXT_LEN = 4096  # Google Chat hard limit per message


# ---------- utilities ----------

def _eprint(*args, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)


def _load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {"spaces": {}}
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        _eprint(f"❌ Config file ไม่ valid JSON | Config file is not valid JSON: {e}")
        _eprint(f"   Path: {CONFIG_PATH}")
        sys.exit(1)
    if "spaces" not in data:
        data["spaces"] = {}
    return data


def _resolve_url(space: str | None, url: str | None) -> str:
    if url:
        return url
    if not space:
        _eprint("❌ ต้องระบุ --space หรือ --url อย่างใดอย่างหนึ่ง")
        sys.exit(1)
    config = _load_config()
    preset = config["spaces"].get(space)
    if not preset:
        _eprint(f"❌ Preset '{space}' ไม่พบใน config | Preset not found")
        known = list(config["spaces"].keys())
        if known:
            _eprint(f"   Preset ที่มีอยู่: {', '.join(known)}")
        else:
            _eprint("   ยังไม่มี preset เลย — ลอง: manage_webhooks.py add --name ... --url ...")
        sys.exit(1)
    return preset["url"]


def _build_text_payload(text: str, thread_key: str | None) -> dict[str, Any]:
    if len(text) > MAX_TEXT_LEN:
        _eprint(
            f"❌ ข้อความยาว {len(text)} ตัวอักษร เกิน limit {MAX_TEXT_LEN} | "
            f"Text too long — split into Card sections instead"
        )
        sys.exit(2)
    payload: dict[str, Any] = {"text": text}
    if thread_key:
        payload["thread"] = {"threadKey": thread_key}
    return payload


def _build_card_payload(card_path: Path, thread_key: str | None) -> dict[str, Any]:
    if not card_path.exists():
        _eprint(f"❌ Card JSON file ไม่พบ: {card_path}")
        sys.exit(1)
    try:
        with card_path.open("r", encoding="utf-8") as f:
            card_data = json.load(f)
    except json.JSONDecodeError as e:
        _eprint(f"❌ Card JSON parse ไม่ได้ | Invalid card JSON: {e}")
        _eprint(f"   Tip: ตรวจ syntax ด้วย `python -m json.tool {card_path}`")
        sys.exit(2)

    # รองรับ 2 รูปแบบ: (1) ไฟล์มี "cardsV2" อยู่แล้ว (2) ไฟล์เป็น card เดี่ยว ๆ
    if "cardsV2" in card_data:
        payload = dict(card_data)
    elif "card" in card_data or "header" in card_data or "sections" in card_data:
        # auto-wrap
        card_id = card_data.get("cardId") or card_path.stem
        inner = card_data.get("card") or {
            k: v for k, v in card_data.items() if k in ("header", "sections", "name")
        }
        payload = {"cardsV2": [{"cardId": card_id, "card": inner}]}
    else:
        _eprint(
            "❌ Card JSON ไม่มี 'cardsV2' หรือ 'card'/'sections' | "
            "Missing required keys (see references/card_v2_guide.md)"
        )
        sys.exit(2)

    if thread_key:
        payload["thread"] = {"threadKey": thread_key}
    return payload


def _send(url: str, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_S) as resp:
            status = resp.status
            response_body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        _handle_http_error(e.code, err_body)
        sys.exit(3)
    except urllib.error.URLError as e:
        _eprint(f"❌ Network error | เชื่อมต่อไม่ได้: {e.reason}")
        _eprint("   ลองเช็ค internet / DNS / firewall")
        sys.exit(4)
    except TimeoutError:
        _eprint(f"❌ Timeout หลัง {REQUEST_TIMEOUT_S}s | Request timed out")
        sys.exit(4)

    if status >= 400:
        _handle_http_error(status, response_body)
        sys.exit(3)

    print(f"✅ ส่งสำเร็จ | Sent successfully (HTTP {status})")


def _handle_http_error(status: int, body: str) -> None:
    hints = {
        400: "Payload ผิด format — ตรวจ JSON / Card v2 structure",
        401: "Unauthorized — webhook อาจถูก revoke",
        403: "Forbidden — webhook URL หมดอายุ หรือ space ถูกลบ",
        404: "Not found — URL ผิด หรือ copy ไม่ครบ (ต้องมี ?key=&token=)",
        429: "Rate limit — รอ ~30 วิ แล้วลองใหม่ (skill นี้ไม่ retry อัตโนมัติ)",
    }
    hint = hints.get(status, "ดูรายละเอียดใน response body ด้านล่าง")
    _eprint(f"❌ HTTP {status} — {hint}")
    if body:
        _eprint(f"   Response: {body[:500]}")


# ---------- main ----------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ส่งข้อความเข้า Google Chat ผ่าน Incoming Webhook",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--space", help="ชื่อ preset (เช่น dev, daily-summary)")
    target.add_argument("--url", help="Webhook URL ตรง ๆ")

    msg = parser.add_mutually_exclusive_group(required=True)
    msg.add_argument("--text", help="ข้อความ plain text / rich formatted")
    msg.add_argument("--card", help="Path ไปยังไฟล์ JSON ของ Card v2")
    msg.add_argument("--stdin", action="store_true", help="อ่าน text จาก stdin")

    parser.add_argument("--thread-key", help="Reply key สำหรับ thread เดิม")
    parser.add_argument("--dry-run", action="store_true", help="แสดง payload แต่ไม่ส่งจริง")

    args = parser.parse_args()

    # Build payload
    if args.card:
        payload = _build_card_payload(Path(args.card).expanduser(), args.thread_key)
    elif args.stdin:
        text = sys.stdin.read().rstrip("\n")
        if not text:
            _eprint("❌ stdin ว่างเปล่า")
            sys.exit(1)
        payload = _build_text_payload(text, args.thread_key)
    else:
        payload = _build_text_payload(args.text, args.thread_key)

    # Dry-run = แสดง payload, ไม่ต้อง resolve URL ก็ได้
    if args.dry_run:
        print("🌸 Dry-run — payload ที่จะส่ง:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if args.space:
            try:
                url = _resolve_url(args.space, None)
                # mask URL เพื่อ security
                masked = url[:50] + "...[masked]" if len(url) > 50 else url
                print(f"\n→ target space: {args.space}")
                print(f"→ target URL (masked): {masked}")
            except SystemExit:
                # ยอมให้ dry-run พังถ้า preset ไม่มี
                pass
        else:
            print(f"\n→ target URL (masked): {args.url[:50]}...[masked]")
        return

    url = _resolve_url(args.space, args.url)
    _send(url, payload)


if __name__ == "__main__":
    main()
