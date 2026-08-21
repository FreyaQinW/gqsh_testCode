# *-*coding:utf-8 *-*
"""OSS2 / OMS / Product / quality / swagger 共享 API 客户端配置。

仅提供 test_URL + header（及跨系统桥接键）。
业务上下文请放到各模块 conftest（如 ProductOss2 的 product_ctx）。
其他模块仍可向本 dict 动态写入，以兼容存量用例。
"""
import os

import pytest

from utils.auto_login import refresh_oss2_token
from utils.csv_reader import load_csv_data

_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# 跨系统联合跑时需要落到环境变量的键（supplier → scms 等）
_ENV_BRIDGE_KEYS = (
    'JINDIE_PURCHASE_ORDER_NO',
    'INSERTED_SUPPLIER_CODE',
    'INSERTED_SUPPLIER_NAME',
    'INSERTED_SUPPLIER_INNER_CODE',
    'INSERTED_PRODUCER_CODE',
    'INSERTED_PRODUCER_NAME',
)


@pytest.fixture(scope='session')
def oss2_config():
    """OSS2 登录与 header，供 api / swagger 等复用。"""
    refresh_oss2_token()
    author = load_csv_data(os.path.join(_DATA_DIR, 'Author.csv'))
    base_url = os.environ.get('OSS2_BASE_URL', 'https://test-oss2.zzgqsh.com').rstrip('/')
    host = base_url.split('://', 1)[-1]
    cookie = f'guoquan_monitor_uuid=1768285139701; gq_token={author}'
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': host,
        'Origin': base_url,
        'Referer': base_url,
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        ),
        'X-TOKEN': '',
        'Authorization': author,
        'Cookie': cookie,
    }
    return {
        'test_URL': base_url,
        'header': header,
    }


@pytest.fixture(scope='session')
def global_config(oss2_config):
    """OSS2 API 客户端：登录刷新 token，返回 URL + header。"""
    return oss2_config


@pytest.fixture(scope='session', autouse=True)
def set_env_vars(global_config):
    """仅同步跨系统桥接键，避免把 header 等整包写入 environ。"""
    yield
    for key in _ENV_BRIDGE_KEYS:
        value = global_config.get(key)
        if value not in (None, '', 'None'):
            os.environ[key] = str(value)
