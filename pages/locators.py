"""Central place for every selector / accessible name used by the page objects.

Page objects only build Playwright ``Locator`` objects from these constants,
so when the UI changes we only need to update this file.
"""


class LoginLocators:
    SECTION = "#login_section"
    MAIN_SECTION = "#main_section"
    ID_INPUT_LABEL = "ID"
    PASSWORD_INPUT_LABEL = "パスワード"
    LOGIN_BUTTON_NAME = "ログイン"
    HEADING_NAME = "ログイン"
    ERROR_MESSAGE_TEXT = "IDまたはパスワードが正しくありません。"


class TicketListLocators:
    TICKET_TAB = "#nav_tab_tickets"
    TICKET_TAB_ACTIVE_CLASS = "nav-tab nav-tab--active"
    TBODY = "#ticket_tbody"
    ROWS = "#ticket_tbody tr"
    PRIORITY_FILTER_NAME = "優先度で絞り込み"
    PRIORITY_HIGH_CHIP = ".chip.priority-high"
    SELECT_ALL_NAME = "全て選択"
    ROW_CHECKBOX = "input.row-checkbox"
    BULK_BAR = "#bulk_action_bar"
    SELECTED_COUNT = "#selected_count"
    HEADER_USER = "#header_username"
    DETAIL_BUTTON = "button.btn-detail"
    DELETE_BUTTON = "button.btn-delete"
    DETAIL_OVERLAY = "#detail_overlay"
    FILE_INPUT = "#detail_file_input"
    FILE_NAME = "#detail_file_name"
    REMOVE_FILE_NAME = "ファイルを削除"
    DELETE_SUCCESS_TEXT = "チケットを削除しました。"
    PREVIEW_IFRAME = "#preview_iframe"
    FRAME_STATUS_SELECT = "#frame_status"
    FRAME_APPLY_BUTTON_NAME = "適用"
    MANUAL_BUTTON_NAME = "外部マニュアルを開く（新しいタブ）"


class NotificationLocators:
    TAB = "#nav_tab_notifications"
    PANEL = "#panel_notifications"
    TBODY = "#notification_tbody"
    SEARCH_INPUT_NAME = "タイトルまたは内容で検索"
    SEARCH_BUTTON_NAME = "検索"
    EMPTY_RESULT_TEXT = "検索条件に一致する通知が見つかりません"
    EMPTY_CREATE_BUTTON_NAME = "＋通知を作成する"
    MODAL = "#notification_modal"
    MODAL_TITLE = "#notification_modal_title"
    MODAL_TITLE_CREATE_TEXT = "通知を作成"
    TITLE_INPUT_NAME = "タイトル*"
    BODY_INPUT_NAME = "内容*"
    SUBMIT_BUTTON = "#notif_modal_submit"
    CREATE_SUCCESS_TEXT = "通知を作成しました。"
