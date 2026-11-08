import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from pages.locators import TicketListLocators as L


class TicketListPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.ticket_tab: Locator = page.locator(L.TICKET_TAB)
        self.tbody: Locator = page.locator(L.TBODY)
        self.rows: Locator = page.locator(L.ROWS)
        self.priority_filter: Locator = page.get_by_role("combobox", name=L.PRIORITY_FILTER_NAME)
        self.select_all: Locator = page.get_by_role("checkbox", name=L.SELECT_ALL_NAME)
        self.bulk_bar: Locator = page.locator(L.BULK_BAR)
        self.selected_count: Locator = page.locator(L.SELECTED_COUNT)
        self.header_user: Locator = page.locator(L.HEADER_USER)
        self.detail_overlay: Locator = page.locator(L.DETAIL_OVERLAY)
        self.file_input: Locator = page.locator(L.FILE_INPUT)
        self.file_name: Locator = page.locator(L.FILE_NAME)
        self.remove_file: Locator = page.get_by_role("button", name=L.REMOVE_FILE_NAME)
        self.delete_success_toast: Locator = page.get_by_text(L.DELETE_SUCCESS_TEXT)
        self.preview_frame = page.frame_locator(L.PREVIEW_IFRAME)
        self.manual_button: Locator = page.get_by_role("button", name=L.MANUAL_BUTTON_NAME)

    def row_by_text(self, text: str) -> Locator:
        return self.rows.filter(has_text=text)

    @allure.step("Expect admin ticket list: user '{user_name}', {row_count} rows")
    def expect_admin_ticket_list(self, user_name: str, row_count: int) -> None:
        expect(self.header_user).to_have_text(user_name)
        expect(self.ticket_tab).to_have_class(L.TICKET_TAB_ACTIVE_CLASS)
        expect(self.rows).to_have_count(row_count)

    @allure.step("Expect guest header '{user_name}'")
    def expect_guest_header(self, user_name: str) -> None:
        expect(self.header_user).to_have_text(user_name)

    @allure.step("Filter priority '{priority}'")
    def filter_priority(self, priority: str) -> None:
        self.priority_filter.select_option(priority)

    @allure.step("Expect only high priority tickets")
    def expect_only_high_priority(self, count: int) -> None:
        expect(self.rows).to_have_count(count)
        expect(self.rows.locator(L.PRIORITY_HIGH_CHIP)).to_have_count(count)

    @allure.step("Check select-all checkbox")
    def check_select_all(self) -> None:
        self.select_all.check()

    @allure.step("Expect all visible rows checked and bulk bar shown")
    def expect_all_rows_checked_and_bulk_bar(self, row_count: int, selected_text: str) -> None:
        checkboxes = self.rows.locator(L.ROW_CHECKBOX)
        expect(checkboxes).to_have_count(row_count)
        for checkbox in checkboxes.all():
            expect(checkbox).to_be_checked()
        expect(self.bulk_bar).to_be_visible()
        expect(self.selected_count).to_have_text(selected_text)

    @allure.step("Open detail dialog of row '{text}'")
    def open_detail(self, text: str) -> None:
        self.row_by_text(text).locator(L.DETAIL_BUTTON).click()
        expect(self.detail_overlay).to_be_visible()

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
        self.row_by_text(text).locator(L.DELETE_BUTTON).click()

    @allure.step("Expect row '{text}' removed and delete toast")
    def expect_row_deleted(self, text: str) -> None:
        expect(self.delete_success_toast).to_be_visible()
        expect(self.row_by_text(text)).to_have_count(0)

    @allure.step("Apply status '{status}' inside preview iframe")
    def apply_status_in_iframe(self, status: str, expected_message: str) -> str:
        before = self.tbody.inner_text()
        self.preview_frame.locator(L.FRAME_STATUS_SELECT).select_option(label=status)
        self.preview_frame.get_by_role("button", name=L.FRAME_APPLY_BUTTON_NAME).click()
        expect(self.preview_frame.locator("body")).to_contain_text(expected_message)
        return before

    @allure.step("Expect parent ticket list unchanged")
    def expect_parent_list_unchanged(self, before: str) -> None:
        after = self.tbody.inner_text()
        assert after == before, "Parent ticket list changed after iframe action"

    @allure.step("Open external manual in a new tab")
    def open_manual_in_new_tab(self) -> Page:
        with self.page.expect_popup() as popup_info:
            self.manual_button.click()
        popup = popup_info.value
        popup.wait_for_load_state("domcontentloaded")
        return popup
