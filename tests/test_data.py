"""Test data shared by the test cases.

Account info is NOT stored here — it is loaded from ``.env`` in ``conftest.py``.
"""
import re

# --- Login ---
WRONG_PASSWORD = "wrongpass"

# --- Header user names ---
ADMIN_USER_NAME = "田中 太郎（管理者）"
GUEST_USER_NAME = "鈴木 花子（新規ユーザー）"

# --- Ticket list ---
TOTAL_TICKETS = 10
SELECTED_COUNT_TEXT = f"{TOTAL_TICKETS}件選択中"
PRIORITY_HIGH = "高"
HIGH_PRIORITY_COUNT = 5
TARGET_TICKET = "ログインできない"

# --- Upload ---
PNG_FILE_NAME = "sample.png"
PNG_1MB = b"\x89PNG\r\n\x1a\n" + b"0" * (1024 * 1024 - 8)

# --- Preview iframe ---
IFRAME_STATUS = "完了"
IFRAME_STATUS_MESSAGE = f"プレビューを {IFRAME_STATUS} に更新しました（画面外には反映されません）"

# --- External manual ---
MANUAL_URL_PATTERN = re.compile(r"^https://playwright\.dev")

# --- Notification ---
NOTIFICATION_NOT_EXIST_KEYWORD = "ngan2-keyword-not-exist-0000"
