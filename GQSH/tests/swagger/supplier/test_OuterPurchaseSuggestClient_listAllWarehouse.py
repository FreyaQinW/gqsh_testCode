# *-*coding:utf-8 *-*
"""智能补货采购建议 - 全量获取仓库编码、仓库名称"""
import json

import pytest
import requests

from utils.api_helper import parse_json

SWAGGER_PATH = '/supplier-center/h/com.guoquan.supplier.center.api.outer.purchasesuggest.OuterPurchaseSuggestClient'


@pytest.mark.run(order=1)
def test_listAllWarehouse(global_config):
    """智能补货采购建议 - 全量获取仓库编码、仓库名称"""
    body = {}
    try:
        url = global_config['test_URL'] + SWAGGER_PATH + '/listAllWarehouse'
        print(f'请求URL: {url}')
        response = requests.post(
            url=url,
            json=body,
            timeout=30,
            verify=True,
        )
        jd = parse_json(response, '全量获取仓库编码仓库名称')
        print(f'响应参数: {json.dumps(jd, ensure_ascii=False, indent=2)}')
    except requests.exceptions.RequestException as e:
        pytest.fail(f'网络请求失败: {e}')
