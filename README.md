# auto-final-project
# ngan2

Bài tập cuối khóa — Playwright Python, 13 case trên trang Bài tập 17.08.2026.

URL: https://bsv-nhungnguyen.github.io/bai_tap_17082026.html

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
```

## Run

```bash
pytest
HEADED=true pytest -k test_gd01_002_login_screen
```

## 13 cases

| ID | Test |
|---|---|
| GD01_002 | `test_gd01_002_login_screen` |
| GD02.3-007 | `test_gd02_3_007_login_success` |
| GD02.8-04 | `test_gd02_8_04_login_wrong_password` |
| GD02.8-09 | `test_gd02_8_09_login_disabled_when_empty` |
| GD01_003 | `test_gd01_003_ticket_list_after_login` |
| GD02.3-004 | `test_gd02_3_004_guest_login` |
| GD02.4-02 | `test_gd02_4_02_filter_priority_high` |
| GD02.2-001 | `test_gd02_2_001_select_all_checkbox` |
| GD02.7-01 | `test_gd02_7_01_upload_png` |
| GD03.1-01 | `test_gd03_1_01_delete_ticket_confirm` |
| GD03.2-01 | `test_gd03_2_01_iframe_apply_status` |
| GD03.3-04 | `test_gd03_3_04_open_manual_new_tab` |
| GD02.1-01 | `test_gd02_1_01_empty_result_opens_create_modal` |
