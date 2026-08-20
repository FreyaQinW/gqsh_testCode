# *-*coding:utf-8 *-*
"""OMS 区域实时库存 API 接口测试"""
import json

import pytest
import requests

from utils.api_helper import assert_oss2_success, parse_json, post_api

BASE = '/api/oms-admin/stock'


@pytest.mark.run(order=1)
def test_regionalInventory_list(global_config):
    """区域实时库存 - 查询区域库存列表"""
    body = {
        'platformSkuCode': '',
        'platformSkuName': '',
        'warehouseNo': 'CK831',
        'orgNo': '000001',
        'page': 1,
        'limit': 10,
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/page', body))
        assert_oss2_success(jd, '区域实时库存列表')
        data = jd.get('data') or {}
        total = data.get('totalCount', 0)
        print(f'区域实时库存列表总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
