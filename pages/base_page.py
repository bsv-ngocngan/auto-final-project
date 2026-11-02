import time
from collections.abc import Callable

import allure
from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Navigate to URL: {url}")
    def navigate_to(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    @allure.step("Expect visible")
    def expect_visible(self, locator: Locator) -> None:
        expect(locator).to_be_visible()

    @allure.step("Expect hidden")
    def expect_hidden(self, locator: Locator) -> None:
        expect(locator).to_be_hidden()

    def wait_until(
        self,
        condition: Callable[[], bool],
        *,
        timeout_ms: int = 10000,
        poll_interval_ms: int = 200,
        message: str = "Condition was not met before timeout",
    ) -> None:
        deadline = time.monotonic() + timeout_ms / 1000
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                if condition():
                    return
            except Exception as exc:
                last_error = exc
            self.page.wait_for_timeout(poll_interval_ms)
        detail = f" ({last_error})" if last_error else ""
        raise AssertionError(f"{message}{detail}")
