# *-*coding:utf-8 *-*
"""ProductOss2 业务上下文：采购 SPU / 云埔 / 控销 / 生命周期等串联参数。"""
import pytest


@pytest.fixture(scope='session')
def product_ctx():
    """产品中心链路共享上下文（session 级，供 flow 脚本跨文件传递）。"""
    return {}
