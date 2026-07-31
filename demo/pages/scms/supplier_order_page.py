# *-*coding:utf-8 *-*
from pages.base_page import BasePage


class SupplierOrderPage(BasePage):
    """SCMS 供应商端订单页"""

    URL_PATH = '/order/list'

    SEARCH_INPUT = 'input[placeholder*="订单号"]'
    SEARCH_BUTTON = 'button:has-text("查询"), button:has-text("搜索")'
    TABLE_ROWS = 'table tbody tr'

    def navigate(self, base_url: str):
        self.page.goto(base_url + self.URL_PATH)
        self.page.wait_for_load_state('networkidle')

    def search_by_order_no(self, order_no: str):
        self.wait_for(self.SEARCH_INPUT)
        self.fill(self.SEARCH_INPUT, order_no)
        self.click(self.SEARCH_BUTTON)
        self.page.wait_for_load_state('networkidle')

    def get_row_count(self) -> int:
        return self.page.locator(self.TABLE_ROWS).count()
