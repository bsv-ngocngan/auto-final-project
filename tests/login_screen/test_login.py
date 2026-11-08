import allure

from pages.login_page import LoginPage
from pages.ticket_list_page import TicketListPage
from tests.test_data import (
    ADMIN_USER_NAME,
    GUEST_USER_NAME,
    TOTAL_TICKETS,
    WRONG_PASSWORD,
)
from utils.allure_helper import description_md


@allure.feature("Login")
@description_md(
    """
    - **前提条件**: Automation _ Finnal Project.xlsx / sheet Testcases
    - **テスト手順**: ログイン画面（ID GD01_002, GD01_003, GD02.3-004, GD02.3-007, GD02.8-04, GD02.8-09）
    - **期待する結果**: 各テストの description を参照
    """
)
class TestLogin:
    @allure.title("GD01_002 ログイン画面が表示される")
    @description_md(
        """
        - **前提条件**: ブラウザでページを開く
        - **テスト手順**:
            1. ページを開く
        - **期待する結果**: ログイン画面が表示される（ID・パスワード入力欄、ログインボタン）
        """
    )
    def test_gd01_002_login_screen(self, access_to_login: LoginPage) -> None:
        access_to_login.expect_login_form_displayed()

    @allure.title("GD02.3-007 正常系ログイン")
    @description_md(
        """
        - **前提条件**: ログイン画面を表示中
        - **テスト手順**:
            1. IDに admin アカウントのID（.env の ADMIN_ID）を入力する
            2. パスワードに admin アカウントのパスワード（.env の ADMIN_PASSWORD）を入力する
            3. 「ログイン」ボタンを押下する
        - **期待する結果**: チケット一覧画面に遷移し、ヘッダーにログインユーザー名が表示される
        """
    )
    def test_gd02_3_007_login_success(
        self,
        access_to_login: LoginPage,
        admin_account: tuple[str, str],
        ticket_list_page: TicketListPage,
    ) -> None:
        user_id, password = admin_account
        access_to_login.login(user_id, password)
        ticket_list_page.expect_admin_ticket_list(ADMIN_USER_NAME, TOTAL_TICKETS)

    @allure.title("GD02.8-04 異常系ログイン")
    @description_md(
        """
        - **前提条件**: ログイン画面を表示中
        - **テスト手順**:
            1. IDに admin アカウントのID（.env の ADMIN_ID）を入力する
            2. パスワードに「wrongpass」を入力する
            3. 「ログイン」ボタンを押下する
        - **期待する結果**: 「IDまたはパスワードが正しくありません。」というエラーメッセージが表示され、画面遷移しない
        """
    )
    def test_gd02_8_04_login_wrong_password(
        self,
        access_to_login: LoginPage,
        admin_account: tuple[str, str],
    ) -> None:
        user_id, _password = admin_account
        access_to_login.input_id(user_id)
        access_to_login.input_password(WRONG_PASSWORD)
        access_to_login.click_button_login()
        access_to_login.expect_invalid_credential_error()

    @allure.title("GD02.8-09 ログインボタンは未入力のとき非活性")
    @description_md(
        """
        - **前提条件**: ログイン画面を表示中
        - **テスト手順**:
            1. IDとパスワードをどちらも未入力のままにする
        - **期待する結果**: 「ログイン」ボタンが非活性（disabled）のままである
        """
    )
    def test_gd02_8_09_login_disabled_when_empty(self, access_to_login: LoginPage) -> None:
        access_to_login.expect_login_button_disabled()

    @allure.title("GD02.3-004 guestでログインする")
    @description_md(
        """
        - **前提条件**: ログイン画面を表示中
        - **テスト手順**:
            1. IDに guest アカウントのID（.env の GUEST_ID）を入力する
            2. パスワードに guest アカウントのパスワード（.env の GUEST_PASSWORD）を入力する
            3. 「ログイン」ボタンを押下する
        - **期待する結果**: ログインでき、ヘッダーに「鈴木 花子（新規ユーザー）」と表示される
        """
    )
    def test_gd02_3_004_guest_login(self, logged_in_guest: TicketListPage) -> None:
        logged_in_guest.expect_guest_header(GUEST_USER_NAME)

    @allure.title("GD01_003 チケット一覧に10件表示される")
    @description_md(
        """
        - **前提条件**: admin アカウント（.env）でログイン済み
        - **テスト手順**:
            1. 画面表示を確認する
        - **期待する結果**: チケット一覧画面（「チケット一覧」タブがアクティブ）が表示され、10件のチケットが表示される
        """
    )
    def test_gd01_003_ticket_list_after_login(self, logged_in_admin: TicketListPage) -> None:
        logged_in_admin.expect_admin_ticket_list(ADMIN_USER_NAME, TOTAL_TICKETS)
