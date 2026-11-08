# ngan2

## Locator order
1. get_by_role(name)
2. get_by_label / get_by_placeholder
3. #id
4. class BEM (`.btn-detail`, `.row-checkbox`)

## Traps used by these tests
- Select-all checkbox has opacity 0. Call `check()` on the input (`全て選択`), not the icon.
- File input `#detail_file_input` is `display:none`. Use `set_input_files`.
- `詳細` / `削除` repeat on every row. Scope with the row locator, and use `.btn-delete` / `.btn-detail`.
- Notification empty-result create button is `＋通知を作成する` (`#btn_new_notification_empty`), not the toolbar button.
- `ensure_notification_exists` searches, opens that button only when missing, then creates.

## Accounts
- Account info (admin / guest) được load từ `.env` (`ADMIN_ID`, `ADMIN_PASSWORD`, `GUEST_ID`, `GUEST_PASSWORD`).
- Xem `.env.example` để biết các key cần khai báo. Không ghi ID / password vào file này.

###NNTT: không để account info ở đây. 

