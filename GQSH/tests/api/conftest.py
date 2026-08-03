# *-*coding:utf-8 *-*
"""OSS2 / OMS OSS2 模块共享 API 测试配置"""
import os

import pytest

from utils.auto_login import refresh_oss2_token
from utils.csv_reader import load_csv_data

_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')


@pytest.fixture(scope='session')
def global_config():
    """OSS2 运营后台 API 全局配置（自动登录刷新 token）"""
    refresh_oss2_token()
    author = load_csv_data(os.path.join(_DATA_DIR, 'Author.csv'))
    cookie = f'guoquan_monitor_uuid=1768285139701; gq_token={author}'
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': 'test-oss2.zzgqsh.com',
        'Origin': 'https://test-oss2.zzgqsh.com',
        'Referer': 'https://test-oss2.zzgqsh.com',
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        ),
        'X-TOKEN': '',
        'Authorization': author,
        'Cookie': cookie,
    }
    return {
        'test_URL': 'https://test-oss2.zzgqsh.com',
        'header': header,
        'JINDIE_PURCHASE_ORDER_NO': None,
        'documentNo': None,
        'relatedOrder': None,
        'productSourceCode': None,
        'name': None,
        'nameCode': None,
        'omsOrderNo':None,
        "purchaseOrderNo":None
    }


@pytest.fixture(scope='session', autouse=True)
def set_env_vars(global_config):
    for key, value in global_config.items():
        os.environ[key] = str(value)
    yield
    for key in global_config:
        os.environ.pop(key, None)
