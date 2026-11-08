import allure
from playwright.sync_api import expect

from pages.ticket_list_page import TicketListPage
from tests.test_data import (
    HIGH_PRIORITY_COUNT,
    IFRAME_STATUS,
    IFRAME_STATUS_MESSAGE,
    MANUAL_URL_PATTERN,
    PNG_1MB,
    PNG_FILE_NAME,
    PRIORITY_HIGH,
    SELECTED_COUNT_TEXT,
    TARGET_TICKET,
    TOTAL_TICKETS,
)
from utils.allure_helper import description_md


@allure.feature("Ticket list")
@description_md(
    """
    - **前提条件**: Automation _ Finnal Project.xlsx / sheet Testcases
    - **テスト手順**: チケット一覧画面（ID GD02.2-001, GD02.4-02, GD02.7-01, GD03.1-01, GD03.2-01, GD03.3-04）
    - **期待する結果**: 各テストの description を参照
    """
)
class TestTicketList:
    @allure.title("GD02.4-02 優先度「高」で絞り込む")
    @description_md(
        """
        - **前提条件**: チケット一覧画面を表示中
        - **テスト手順**:
            1. 優先度プルダウンで「高」を選択する
        - **期待する結果**: 優先度が「高」のチケットのみ表示される（5件）
        """
    )
    def test_gd02_4_02_filter_priority_high(self, logged_in_admin: TicketListPage) -> None:
        logged_in_admin.filter_priority(PRIORITY_HIGH)
        logged_in_admin.expect_only_high_priority(HIGH_PRIORITY_COUNT)

    @allure.title("GD02.2-001 全選択チェックボックス")
    @description_md(
        """
        - **前提条件**: チケット一覧画面を表示中
        - **テスト手順**:
            1. テーブルヘッダーの全選択チェックボックスを押下する
        - **期待する結果**: 表示中の全行のチェックボックスがチェックされ、一括操作バーが表示される
        """
    )
    def test_gd02_2_001_select_all_checkbox(self, logged_in_admin: TicketListPage) -> None:
        logged_in_admin.check_select_all()
        logged_in_admin.expect_all_rows_checked_and_bulk_bar(TOTAL_TICKETS, SELECTED_COUNT_TEXT)

    @allure.title("GD02.7-01 PNGをアップロードする")
    @description_md(
        """
        - **前提条件**: 詳細ダイアログを表示中
        - **テスト手順**:
            1. ドロップゾーンに.pngファイル（1MB程度）をアップロードする
        - **期待する結果**: ファイル名とサイズがプレビュー表示され、削除アイコンが表示される
        """
    )
    def test_gd02_7_01_upload_png(self, logged_in_admin: TicketListPage) -> None:
        logged_in_admin.open_detail(TARGET_TICKET)
        logged_in_admin.upload_png(PNG_FILE_NAME, PNG_1MB)
        logged_in_admin.expect_file_preview(PNG_FILE_NAME)

    @allure.title("GD03.1-01 チケット削除を確定する")
    @description_md(
        """
        - **前提条件**: チケット一覧画面を表示中
        - **テスト手順**:
            1. 任意の行の「削除」ボタンを押下する
            2. 確認ダイアログ（confirm）で「OK」を押下する
        - **期待する結果**: 該当行が一覧から削除され、トースト通知「チケットを削除しました。」が表示される
        """
    )
    def test_gd03_1_01_delete_ticket_confirm(self, logged_in_admin: TicketListPage) -> None:
        logged_in_admin.delete_row_accept(TARGET_TICKET)
        logged_in_admin.expect_row_deleted(TARGET_TICKET)

    @allure.title("GD03.2-01 iframe内の操作は親画面に影響しない")
    @description_md(
        """
        - **前提条件**: チケット一覧画面を表示中
        - **テスト手順**:
            1. 埋め込みプレビュー内のプルダウンでステータスを選択する
            2. 埋め込みプレビュー内の「適用」ボタンを押下する
        - **期待する結果**: iframe内にのみ結果メッセージが表示され、親ページの一覧には影響しない
        """
    )
    def test_gd03_2_01_iframe_apply_status(self, logged_in_admin: TicketListPage) -> None:
        before = logged_in_admin.apply_status_in_iframe(IFRAME_STATUS, IFRAME_STATUS_MESSAGE)
        logged_in_admin.expect_parent_list_unchanged(before)

    @allure.title("GD03.3-04 外部マニュアルを新しいタブで開く")
    @description_md(
        """
        - **前提条件**: チケット一覧画面を表示中
        - **テスト手順**:
            1. 「外部マニュアルを開く（新しいタブ）」ボタンを押下する
        - **期待する結果**: 新しいタブが開き、外部サイトが表示される
        """
    )
    def test_gd03_3_04_open_manual_new_tab(self, logged_in_admin: TicketListPage) -> None:
        popup = logged_in_admin.open_manual_in_new_tab()
        expect(popup).to_have_url(MANUAL_URL_PATTERN)
