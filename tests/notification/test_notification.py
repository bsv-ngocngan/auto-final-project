import allure

from pages.notification_page import NotificationPage
from pages.ticket_list_page import TicketListPage
from tests.test_data import NOTIFICATION_NOT_EXIST_KEYWORD
from utils.allure_helper import description_md

###NNTT: nên có thông tin testcase, class ở đầu.
@allure.feature("Notification")
@description_md(
    """
    - **前提条件**: Automation _ Finnal Project.xlsx / sheet Testcases
    - **テスト手順**: 通知一覧画面（ID GD02.1-01）
    - **期待する結果**: 各テストの description を参照
    """
)
class TestNotification:
    @allure.title("GD02.1-01 検索0件から通知作成モーダルを開く")
    @description_md(
        """
        - **前提条件**: 通知一覧画面を表示中
        - **テスト手順**:
            1. 存在しないキーワードで検索する
            2. 「検索条件に一致する通知が見つかりません」の下にある「＋通知を作成する」ボタンを押下する
        - **期待する結果**: 通知作成モーダルが開く（ツールバーの作成ボタンと同じ動作）
        """
    )
    def test_gd02_1_01_empty_result_opens_create_modal(
        self,
        logged_in_admin: TicketListPage,
        notification_page: NotificationPage,
    ) -> None:
        notification_page.open()
        notification_page.search(NOTIFICATION_NOT_EXIST_KEYWORD)
        notification_page.expect_empty_result()
        notification_page.click_create_from_empty_result()
        notification_page.expect_create_modal_open()
        ###NNTT: chưa có step nào verify kết quả, ngoài ra không nên hardcode dữ liệu trong test, nên tạo test_data.py
