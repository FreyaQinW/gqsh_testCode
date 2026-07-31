# *-*coding:utf-8 *-*
from playwright.sync_api import Page
from pages.base_page import BasePage


class OrderListPage(BasePage):
    """OSS2 采购订单列表页"""

    URL_PATH = '/purchase/order'

    # 选择器（根据实际页面调整）
    SEARCH_INPUT = 'input[placeholder*="订单号"]'
    SEARCH_BUTTON = 'button:has-text("查询"), button:has-text("搜索")'
    TABLE_ROWS = 'table tbody tr'
    EMPTY_TIP = '.el-empty, .ant-empty, :has-text("暂无数据")'

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

    def has_results(self) -> bool:
        return self.get_row_count() > 0
