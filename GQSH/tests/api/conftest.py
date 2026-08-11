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
        'documentNo': None, # 采购申请单编号
        'relatedOrder': None,   # 相关订单
        'productSourceCode': None,  # 生产商编码
        'name': None, # 名称
        'nameCode': None,  # 名称编码
        'omsOrderNo':None, # OMS 订单号
        "purchaseOrderNo":None, # 采购单号
        'complainId': None, # 投诉 ID
        'qualityInspectionId': None,    # 质量检验 ID
        'producerReportId': None,   # 生产报告 ID
        'packageProductCode': None, # 包装产品编码
        'accidentId': None, # 质量事故 ID
        'purchase_spu_code': None, # 商品中心编码
        'deptCode': None, # 商品中心仓库编码
        'prodLifeHouseId': None, # 商品产品生命周期仓库 ID
        'lifeCycleTypeValue': None, # 商品产品生命周期类型值
        'purchaseSpuCode': None, # 产品管理采购SPU编码
        'purchaseSpuId': None, # 产品管理采购SPU ID
        'purchaseSpuSpecId': None, # 产品管理采购SPU规格 ID
        'purchasingName': None, # 新建采购SPU名称（串联后续查询）
        'kingDeeSkuCode': None, # 金蝶SKU编码
        'kingDeeDetailInfo': None, # 金蝶明细查询结果（内存传递）
    }


@pytest.fixture(scope='session', autouse=True)
def set_env_vars(global_config):
    for key, value in global_config.items():
        os.environ[key] = str(value)
    yield
    print(f'\n【purchasingName】{global_config.get("purchasingName")}')
    print(f'【kingDeeSkuCode】{global_config.get("kingDeeSkuCode")}')
    print(f'【purchaseSpuId】{global_config.get("purchaseSpuId")}')
    for key in global_config:
        os.environ.pop(key, None)
