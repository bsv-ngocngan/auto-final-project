import os
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.notification_page import NotificationPage
from pages.ticket_list_page import TicketListPage

load_dotenv()

DEFAULT_BASE_URL = "https://bsv-nhungnguyen.github.io/bai_tap_17082026.html"


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, "").strip() or default


def _require_env(name: str) -> str:
    """Read a required value from .env / environment. Fail clearly when missing."""
    value = _env(name)
    if not value:
        pytest.fail(
            f"Missing environment variable '{name}'. "
            "Copy .env.example to .env and fill in the account info.",
            pytrace=False,
        )
    return value


BASE_URL = _env("BASE_URL", DEFAULT_BASE_URL)
###NNTT: không nên hardcode account info trong code, nên để trong file .env và load vào.
###NNTT: ví dụ:ADMIN_ID = os.getenv("ADMIN_ID")


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

    if report.when == "call":
        item.rep_call = report
        _attach_screenshot(item, report)
    elif report.when == "teardown":
        _attach_video_if_failed(item)


def _attach_screenshot(item, report) -> None:
    """Attach a screenshot to Allure for every test (passed and failed)."""
    page = item.funcargs.get("page")
    if page is None:
        return
    status = "passed" if report.passed else "failed"
    try:
        allure.attach(
            page.screenshot(full_page=True),
            name=f"screenshot-{status}",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:  # page may already be closed / crashed
        allure.attach(str(exc), name="screenshot-error", attachment_type=allure.attachment_type.TEXT)


def _attach_video_if_failed(item) -> None:
    """Attach the recorded video to Allure when the test failed.

    pytest-playwright (``--video=retain-on-failure`` in pytest.ini) saves the
    video into ``output_path`` while tearing down the browser context, so the
    file is only available at the teardown report.
    """
    rep_call = getattr(item, "rep_call", None)
    if rep_call is None or not rep_call.failed:
        return
    output_path = (item.funcargs or {}).get("output_path")
    if not output_path:
        return
    for video in sorted(Path(output_path).glob("video*.webm")):
        allure.attach.file(
            str(video),
            name=f"failure-{video.stem}",
            attachment_type=allure.attachment_type.WEBM,
        )

###NNTT: hàm chụp hình nên hoạt động cả khi passed, không chỉ khi fail. Nếu được nên tạo thêm điều kiện quay video khi testcase failed.

@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def admin_account() -> tuple[str, str]:
    return _require_env("ADMIN_ID"), _require_env("ADMIN_PASSWORD")


@pytest.fixture
def guest_account() -> tuple[str, str]:
    return _require_env("GUEST_ID"), _require_env("GUEST_PASSWORD")


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
