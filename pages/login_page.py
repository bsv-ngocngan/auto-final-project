import allure
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from pages.locators import LoginLocators as L


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.section: Locator = page.locator(L.SECTION)
        self.id_input: Locator = page.get_by_label(L.ID_INPUT_LABEL)
        self.password_input: Locator = page.get_by_label(L.PASSWORD_INPUT_LABEL)
        self.login_button: Locator = page.get_by_role("button", name=L.LOGIN_BUTTON_NAME, exact=True)
        self.heading: Locator = page.get_by_role("heading", name=L.HEADING_NAME)
        self.error_message: Locator = page.get_by_text(L.ERROR_MESSAGE_TEXT)
        self.main_section: Locator = page.locator(L.MAIN_SECTION)
    ### NNTT: nên có file locators.py để lưu các locator, tránh hardcode trong page object để dễ maintain.

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
