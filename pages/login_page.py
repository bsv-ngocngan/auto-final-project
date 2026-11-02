import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.section: Locator = page.locator("#login_section")
        self.id_input: Locator = page.get_by_label("ID")
        self.password_input: Locator = page.get_by_label("パスワード")
        self.login_button: Locator = page.get_by_role("button", name="ログイン", exact=True)
        self.heading: Locator = page.get_by_role("heading", name="ログイン")
        self.error_message: Locator = page.get_by_text("IDまたはパスワードが正しくありません。")
        self.main_section: Locator = page.locator("#main_section")

    @allure.step("Open login page")
    def open(self, url: str) -> None:
        self.navigate_to(url)
        expect(self.heading).to_be_visible()

    @allure.step("Input ID")
    def input_id(self, user_id: str) -> None:
        self.id_input.fill(user_id)

    @allure.step("Input password")
    def input_password(self, password: str) -> None:
        self.password_input.fill(password)

    @allure.step("Click login")
    def click_button_login(self) -> None:
        self.login_button.click()

    @allure.step("Login as {user_id}")
    def login(self, user_id: str, password: str) -> None:
        self.input_id(user_id)
        self.input_password(password)
        self.click_button_login()
        expect(self.main_section).to_be_visible()

    @allure.step("Expect login form displayed")
    def expect_login_form_displayed(self) -> None:
        expect(self.heading).to_be_visible()
        expect(self.id_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()

    @allure.step("Expect login button disabled")
    def expect_login_button_disabled(self) -> None:
        expect(self.login_button).to_be_disabled()

    @allure.step("Expect invalid credential error and stay on login")
    def expect_invalid_credential_error(self) -> None:
        expect(self.error_message).to_be_visible()
        expect(self.heading).to_be_visible()
        expect(self.main_section).to_be_hidden()
