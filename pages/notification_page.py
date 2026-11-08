import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from pages.locators import NotificationLocators as L


class NotificationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.tab: Locator = page.locator(L.TAB)
        self.panel: Locator = page.locator(L.PANEL)
        self.tbody: Locator = page.locator(L.TBODY)
        self.search_input: Locator = page.get_by_role("textbox", name=L.SEARCH_INPUT_NAME)
        self.search_button: Locator = self.panel.get_by_role("button", name=L.SEARCH_BUTTON_NAME)
        self.empty_result: Locator = self.panel.get_by_text(L.EMPTY_RESULT_TEXT)
        self.empty_create_button: Locator = page.get_by_role("button", name=L.EMPTY_CREATE_BUTTON_NAME)
        self.modal: Locator = page.locator(L.MODAL)
        self.modal_title: Locator = page.locator(L.MODAL_TITLE)
        self.title_input: Locator = page.get_by_role("textbox", name=L.TITLE_INPUT_NAME)
        self.body_input: Locator = page.get_by_role("textbox", name=L.BODY_INPUT_NAME)
        self.submit_button: Locator = page.locator(L.SUBMIT_BUTTON)
        self.create_success_toast: Locator = page.get_by_text(L.CREATE_SUCCESS_TEXT)

    def row_by_title(self, title: str) -> Locator:
        return self.tbody.get_by_text(title, exact=True)

    @allure.step("Open notification tab")
    def open(self) -> None:
        self.tab.click()
        expect(self.panel).to_be_visible()

    @allure.step("Search notification '{keyword}'")
    def search(self, keyword: str) -> None:
        self.search_input.fill(keyword)
        self.search_button.click()

    @allure.step("Expect empty search result")
    def expect_empty_result(self) -> None:
        expect(self.empty_result).to_be_visible()
        expect(self.empty_create_button).to_be_visible()

    @allure.step("Click create button under empty search result")
    def click_create_from_empty_result(self) -> None:
        expect(self.empty_result).to_be_visible()
        self.empty_create_button.click()

    @allure.step("Expect notification create modal open")
    def expect_create_modal_open(self) -> None:
        expect(self.modal).to_be_visible()
        expect(self.modal_title).to_have_text(L.MODAL_TITLE_CREATE_TEXT)
        expect(self.title_input).to_be_visible()
        expect(self.body_input).to_be_visible()
        expect(self.submit_button).to_be_visible()

    @allure.step("Expect notification '{title}' in list")
    def expect_notification_in_list(self, title: str) -> None:
        expect(self.row_by_title(title)).to_be_visible()

    @allure.step("Ensure notification exists: {title}")
    def ensure_notification_exists(self, title: str, body: str) -> None:
        self.open()
        self.search(title)
        if self.row_by_title(title).count() > 0:
            return
        self.click_create_from_empty_result()
        self.expect_create_modal_open()
        self.title_input.fill(title)
        self.body_input.fill(body)
        self.submit_button.click()
        expect(self.create_success_toast).to_be_visible()
        self.expect_notification_in_list(title)
