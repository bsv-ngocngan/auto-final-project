import re

import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage

PNG_1MB = b"\x89PNG\r\n\x1a\n" + b"0" * (1024 * 1024 - 8)


@allure.title("GD02.4-02 優先度「高」で絞り込む")
def test_gd02_4_02_filter_priority_high(logged_in_admin: TicketListPage) -> None:
    logged_in_admin.filter_priority_high()
    logged_in_admin.expect_only_high_priority(5)


@allure.title("GD02.2-001 全選択チェックボックス")
def test_gd02_2_001_select_all_checkbox(logged_in_admin: TicketListPage) -> None:
    logged_in_admin.check_select_all()
    logged_in_admin.expect_all_rows_checked_and_bulk_bar()


@allure.title("GD02.7-01 PNGをアップロードする")
def test_gd02_7_01_upload_png(logged_in_admin: TicketListPage) -> None:
    logged_in_admin.open_detail("ログインできない")
    logged_in_admin.upload_png("sample.png", PNG_1MB)
    logged_in_admin.expect_file_preview("sample.png")


@allure.title("GD03.1-01 チケット削除を確定する")
def test_gd03_1_01_delete_ticket_confirm(logged_in_admin: TicketListPage) -> None:
    logged_in_admin.delete_row_accept("ログインできない")
    logged_in_admin.expect_row_deleted("ログインできない")


@allure.title("GD03.2-01 iframe内の操作は親画面に影響しない")
def test_gd03_2_01_iframe_apply_status(logged_in_admin: TicketListPage) -> None:
    before = logged_in_admin.apply_status_in_iframe("完了")
    logged_in_admin.expect_parent_list_unchanged(before)


@allure.title("GD03.3-04 外部マニュアルを新しいタブで開く")
def test_gd03_3_04_open_manual_new_tab(logged_in_admin: TicketListPage) -> None:
    popup = logged_in_admin.open_manual_in_new_tab()
    expect(popup).to_have_url(re.compile(r"^https://playwright\.dev"))
