# -*- coding: utf-8 -*-
"""产品组合管理 - 产品归集 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success


@pytest.mark.oms
def test_queryProdSummary(global_config):
    """产品归集 - 查询产品归集列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/sku/queryProdSummary',
        {
            "pageSize": 20,
            "pageNo": 1
        }
    )
    json_data = parse_json(response, '产品归集列表')
    assert_success(json_data, '产品归集列表')
    print(f'产品归集列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or [] if isinstance(data, dict) else data
    if not items:
        pytest.skip('产品归集列表无数据，跳过')
    print(f'产品归集列表 数据条数: {len(items)}')
