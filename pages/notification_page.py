import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage


class NotificationPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.tab: Locator = page.locator("#nav_tab_notifications")
        self.panel: Locator = page.locator("#panel_notifications")
        self.search_input: Locator = page.get_by_role("textbox", name="タイトルまたは内容で検索")
        self.search_button: Locator = self.panel.get_by_role("button", name="検索")
        self.empty_create_button: Locator = page.get_by_role("button", name="＋通知を作成する")
        self.modal: Locator = page.locator("#notification_modal")
        self.title_input: Locator = page.get_by_role("textbox", name="タイトル*")
        self.body_input: Locator = page.get_by_role("textbox", name="内容*")
        self.submit_button: Locator = page.locator("#notif_modal_submit")

    @allure.step("Open notification tab")
    def open(self) -> None:
        self.tab.click()
        expect(self.panel).to_be_visible()

    @allure.step("Search notification '{keyword}'")
    def search(self, keyword: str) -> None:
        self.search_input.fill(keyword)
        self.search_button.click()

    @allure.step("Click create button under empty search result")
    def click_create_from_empty_result(self) -> None:
        expect(self.panel.get_by_text("検索条件に一致する通知が見つかりません")).to_be_visible()
        self.empty_create_button.click()

    @allure.step("Expect notification create modal open")
    def expect_create_modal_open(self) -> None:
        expect(self.modal).to_be_visible()
        expect(self.page.locator("#notification_modal_title")).to_have_text("通知を作成")

    @allure.step("Ensure notification exists: {title}")
    def ensure_notification_exists(self, title: str, body: str) -> None:
        self.open()
        self.search(title)
        if self.page.locator("#notification_tbody").get_by_text(title, exact=True).count() > 0:
            return
        self.click_create_from_empty_result()
        self.expect_create_modal_open()
        self.title_input.fill(title)
        self.body_input.fill(body)
        self.submit_button.click()
        expect(self.page.get_by_text("通知を作成しました。")).to_be_visible()
        expect(self.page.locator("#notification_tbody").get_by_text(title, exact=True)).to_be_visible()
