# *-*coding:utf-8 *-*
"""Swagger API 测试配置：复用根 conftest 的 oss2_config，仅覆盖网关 URL。"""
import pytest

_SUPPLIER_URL = 'https://test-debug.gqshintra.com'


@pytest.fixture(scope='session')
def global_config(oss2_config):
    """Swagger：test_URL 为 debug 网关；oss2_URL / header 来自 OSS2。"""
    return {
        **oss2_config,
        'test_URL': _SUPPLIER_URL,
        'oss2_URL': oss2_config['test_URL'],
    }
