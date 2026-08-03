# *-*coding:utf-8 *-*
from playwright.sync_api import Page
from pages.base_page import BasePage


class OSS2LoginPage(BasePage):
    """OSS2 运营后台登录页"""

    USERNAME_INPUT = 'input[placeholder="请输入用户名"]'
    PASSWORD_INPUT = 'input[placeholder="请输入密码"]'
    LOGIN_BUTTON = 'button:has-text("确 定")'

    def login(self, username: str, password: str):
        self.wait_for(self.USERNAME_INPUT)
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        # 等待跳回 OSS2 域名
        self.page.wait_for_url('**/test-oss2.zzgqsh.com/**', timeout=15000)
