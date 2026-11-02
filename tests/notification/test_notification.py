import allure

from pages.notification_page import NotificationPage
from pages.ticket_list_page import TicketListPage


@allure.title("GD02.1-01 検索0件から通知作成モーダルを開く")
def test_gd02_1_01_empty_result_opens_create_modal(
    logged_in_admin: TicketListPage,
    notification_page: NotificationPage,
) -> None:
    notification_page.ensure_notification_exists("ngan2-setup-notice", "created by ensure")
