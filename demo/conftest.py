# *-*coding:utf-8 *-*
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pytest
import playwright.sync_api
import config.oss2_config
from config.scms_config import SCMSConfig
from pages.oss2.login_page import OSS2LoginPage
from pages.scms.login_page import SCMSLoginPage


@pytest.fixture(scope="session")
def browser():
    """启动 Chromium 浏览器（整个测试 session 共用）"""
    with playwright.sync_api.sync_playwright() as p:
        b = p.chromium.launch(headless=False)
        yield b
        b.close()


@pytest.fixture(scope="session")
def oss2_page(browser: playwright.sync_api.Browser) -> playwright.sync_api.Page:
    """完成 OSS2 登录后的 page 对象（session 级别，复用登录态）"""
    context = browser.new_context()
    page = context.new_page()

    creds = config.oss2_config.OSS2Config.credentials()
    page.goto(config.oss2_config.OSS2Config.url())

    login = OSS2LoginPage(page)
    login.login(creds['username'], creds['password'])

    yield page

    context.close()


@pytest.fixture(scope="session")
def scms_page(browser: playwright.sync_api.Browser) -> playwright.sync_api.Page:
    """完成 SCMS 登录后的 page 对象（session 级别，复用登录态）"""
    context = browser.new_context()
    page = context.new_page()

    creds = SCMSConfig.credentials()
    page.goto(SCMSConfig.url())

    login = SCMSLoginPage(page)
    login.login(creds['username'], creds['password'])

    yield page

    context.close()
