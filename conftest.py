import os

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.notification_page import NotificationPage
from pages.ticket_list_page import TicketListPage

load_dotenv()

def _env(name: str, default: str) -> str:
    return os.getenv(name, "").strip() or default


BASE_URL = _env("BASE_URL", "https://bsv-nhungnguyen.github.io/bai_tap_17082026.html")
ADMIN_ID = _env("ADMIN_ID", "admin")
ADMIN_PASSWORD = _env("ADMIN_PASSWORD", "admin123")
GUEST_ID = _env("GUEST_ID", "guest")
GUEST_PASSWORD = _env("GUEST_PASSWORD", "guest123")


def pytest_configure(config) -> None:
    headed = os.getenv("HEADED", "false").strip().lower() == "true"
    if os.getenv("CI", "").strip().lower() in {"1", "true"}:
        headed = False
    try:
        config.option.headed = headed
    except AttributeError:
        pass


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return
    page = item.funcargs.get("page")
    if page is None:
        return
    allure.attach(
        page.screenshot(full_page=True),
        name="failure-screenshot",
        attachment_type=allure.attachment_type.PNG,
    )


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def admin_account() -> tuple[str, str]:
    return ADMIN_ID, ADMIN_PASSWORD


@pytest.fixture
def guest_account() -> tuple[str, str]:
    return GUEST_ID, GUEST_PASSWORD


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def ticket_list_page(page: Page) -> TicketListPage:
    return TicketListPage(page)


@pytest.fixture
def notification_page(page: Page) -> NotificationPage:
    return NotificationPage(page)


@pytest.fixture
def access_to_login(login_page: LoginPage, base_url: str) -> LoginPage:
    login_page.open(base_url)
    return login_page


@pytest.fixture
def logged_in_admin(
    access_to_login: LoginPage,
    admin_account: tuple[str, str],
    ticket_list_page: TicketListPage,
) -> TicketListPage:
    user_id, password = admin_account
    access_to_login.login(user_id, password)
    return ticket_list_page


@pytest.fixture
def logged_in_guest(
    access_to_login: LoginPage,
    guest_account: tuple[str, str],
    ticket_list_page: TicketListPage,
) -> TicketListPage:
    user_id, password = guest_account
    access_to_login.login(user_id, password)
    return ticket_list_page
