import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage


class TicketListPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.ticket_tab: Locator = page.locator("#nav_tab_tickets")
        self.rows: Locator = page.locator("#ticket_tbody tr")
        self.priority_filter: Locator = page.get_by_role("combobox", name="優先度で絞り込み")
        self.select_all: Locator = page.get_by_role("checkbox", name="全て選択")
        self.bulk_bar: Locator = page.locator("#bulk_action_bar")
        self.header_user: Locator = page.locator("#header_username")
        self.file_input: Locator = page.locator("#detail_file_input")
        self.file_name: Locator = page.locator("#detail_file_name")
        self.remove_file: Locator = page.get_by_role("button", name="ファイルを削除")
        self.preview_frame = page.frame_locator("#preview_iframe")
        self.manual_button: Locator = page.get_by_role(
            "button", name="外部マニュアルを開く（新しいタブ）"
        )

    def row_by_text(self, text: str) -> Locator:
        return self.rows.filter(has_text=text)

    @allure.step("Expect admin ticket list with 10 rows")
    def expect_admin_ticket_list(self) -> None:
        expect(self.header_user).to_have_text("田中 太郎（管理者）")
        expect(self.ticket_tab).to_have_class("nav-tab nav-tab--active")
        expect(self.rows).to_have_count(10)

    @allure.step("Expect guest header")
    def expect_guest_header(self) -> None:
        expect(self.header_user).to_have_text("鈴木 花子（新規ユーザー）")

    @allure.step("Filter priority 高")
    def filter_priority_high(self) -> None:
        self.priority_filter.select_option("高")

    @allure.step("Expect only high priority tickets")
    def expect_only_high_priority(self, count: int) -> None:
        expect(self.rows).to_have_count(count)
        expect(self.rows.locator(".chip.priority-high")).to_have_count(count)

    @allure.step("Check select-all checkbox")
    def check_select_all(self) -> None:
        self.select_all.check()

    @allure.step("Expect all visible rows checked and bulk bar shown")
    def expect_all_rows_checked_and_bulk_bar(self) -> None:
        expect(self.rows.locator("input.row-checkbox")).to_have_count(10)
        for checkbox in self.rows.locator("input.row-checkbox").all():
            expect(checkbox).to_be_checked()
        expect(self.bulk_bar).to_be_visible()
        expect(self.page.locator("#selected_count")).to_have_text("10件選択中")

    @allure.step("Open detail dialog of row '{text}'")
    def open_detail(self, text: str) -> None:
        self.row_by_text(text).locator("button.btn-detail").click()
        expect(self.page.locator("#detail_overlay")).to_be_visible()

    @allure.step("Upload png file")
    def upload_png(self, name: str, content: bytes) -> None:
        self.file_input.set_input_files(
            {"name": name, "mimeType": "image/png", "buffer": content}
        )

    @allure.step("Expect file preview and delete icon")
    def expect_file_preview(self, name: str) -> None:
        expect(self.file_name).to_contain_text(name)
        expect(self.remove_file).to_be_visible()

    @allure.step("Delete row '{text}' and accept confirm")
    def delete_row_accept(self, text: str) -> None:
        def _accept(dialog) -> None:
            assert dialog.type == "confirm"
            dialog.accept()

        self.page.once("dialog", _accept)
        self.row_by_text(text).locator("button.btn-delete").click()

    @allure.step("Expect row '{text}' removed and delete toast")
    def expect_row_deleted(self, text: str) -> None:
        expect(self.page.get_by_text("チケットを削除しました。")).to_be_visible()
        expect(self.rows.filter(has_text=text)).to_have_count(0)

    @allure.step("Apply status inside preview iframe")
    def apply_status_in_iframe(self, status: str) -> str:
        before = self.page.locator("#ticket_tbody").inner_text()
        self.preview_frame.locator("#frame_status").select_option(label=status)
        self.preview_frame.get_by_role("button", name="適用").click()
        expect(self.preview_frame.locator("body")).to_contain_text(
            f"プレビューを {status} に更新しました（画面外には反映されません）"
        )
        return before

    @allure.step("Expect parent ticket list unchanged")
    def expect_parent_list_unchanged(self, before: str) -> None:
        after = (self.page.locator("#ticket_tbody")).inner_text()
        assert after == before

    @allure.step("Open external manual in a new tab")
    def open_manual_in_new_tab(self):
        with self.page.expect_popup() as popup_info:
            self.manual_button.click()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        return popup
