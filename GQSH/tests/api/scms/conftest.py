# *-*coding:utf-8 *-*
import os
import pytest
from utils.csv_reader import load_csv_data
from utils.auto_login import refresh_scms_token

_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')


@pytest.fixture(scope="session")
def global_config():
    """SCMS 供应商端 API 全局配置（自动登录刷新 token）"""
    refresh_scms_token()
    Author = load_csv_data(os.path.join(_DATA_DIR, 'AuthorSupplier.csv'))
    token = Author.split('scmsToken=')[1]
    base_url = os.environ.get('SCMS_BASE_URL', 'https://test-scms.zzgqsh.com').rstrip('/')
    host = base_url.split('://', 1)[-1]
    Cookie = 'guoquan_monitor_uuid=1768285139701; gq_token=' + Author
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': host,
        'Origin': base_url,
        'Referer': base_url,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'Token': token,
        'Sign': 'decb9ffab03916881bcd412827be6a45',
        'Authorization': Author,
        'Cookie': Cookie,
    }
    return {
        'test_URL': base_url,
        'header': header,
        # 优先从环境变量读取（与 oss2 联合运行时由对应模块写入）
        'JINDIE_PURCHASE_ORDER_NO': os.environ.get('JINDIE_PURCHASE_ORDER_NO') or None,
        'inserted_supplier_code': os.environ.get('INSERTED_SUPPLIER_CODE') or None,
        'inserted_supplier_name': os.environ.get('INSERTED_SUPPLIER_NAME') or None,
        'inserted_supplier_inner_code': os.environ.get('INSERTED_SUPPLIER_INNER_CODE') or None,
        'inserted_producer_code': os.environ.get('INSERTED_PRODUCER_CODE') or None,
        'inserted_producer_name': os.environ.get('INSERTED_PRODUCER_NAME') or None,
        'materialCode': None,
        'materialName': None,
        'materialSpec': None,
        'batchNo': None,
        'inventoryBatchCode': None,
        'inventoryNum': None,
        'appointDate': None,
        'startTime': None,
        'endTime': None,
        'capacity': None,
        'capacityRemained': None,
        'purchaseOrderDetailCode': None,
    }


@pytest.fixture(scope="session", autouse=True)
def set_env_vars(global_config):
    for key, value in global_config.items():
        os.environ[key] = str(value)
    yield
    for key in global_config.keys():
        os.environ.pop(key, None)
