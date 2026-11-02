import allure

from pages.login_page import LoginPage
from pages.ticket_list_page import TicketListPage


@allure.title("GD01_002 ログイン画面が表示される")
def test_gd01_002_login_screen(access_to_login: LoginPage) -> None:
    access_to_login.expect_login_form_displayed()


@allure.title("GD02.3-007 正常系ログイン")
def test_gd02_3_007_login_success(
    access_to_login: LoginPage,
    admin_account: tuple[str, str], 
    ticket_list_page: TicketListPage,
) -> None:
    user_id, password = admin_account
    access_to_login.login(user_id, password)
    ticket_list_page.expect_admin_ticket_list()


@allure.title("GD02.8-04 異常系ログイン")
def test_gd02_8_04_login_wrong_password(
    access_to_login: LoginPage,
    admin_account: tuple[str, str],
) -> None:
    user_id, _password = admin_account
    access_to_login.input_id(user_id)
    access_to_login.input_password("wrongpass")
    access_to_login.click_button_login()
    access_to_login.expect_invalid_credential_error()


@allure.title("GD02.8-09 ログインボタンは未入力のとき非活性")
def test_gd02_8_09_login_disabled_when_empty(access_to_login: LoginPage) -> None:
    access_to_login.expect_login_button_disabled()


@allure.title("GD02.3-004 guestでログインする")
def test_gd02_3_004_guest_login(logged_in_guest: TicketListPage) -> None:
    logged_in_guest.expect_guest_header()


@allure.title("GD01_003 チケット一覧に10件表示される")
def test_gd01_003_ticket_list_after_login(logged_in_admin: TicketListPage) -> None:
    logged_in_admin.expect_admin_ticket_list()
