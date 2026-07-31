# *-*coding:utf-8 *-*
from playwright.sync_api import Page


class BasePage:
    """基础页面类，封装常用操作"""

    def __init__(self, page: Page):
        self.page = page

    def click(self, selector: str):
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_for(self, selector: str, timeout: int = 10000):
        self.page.locator(selector).wait_for(state='visible', timeout=timeout)

    def screenshot(self, path: str):
        self.page.screenshot(path=path)
