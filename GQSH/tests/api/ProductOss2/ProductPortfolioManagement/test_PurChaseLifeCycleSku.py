# -*- coding: utf-8 -*-
"""产品组合管理 - C端商品生命周期 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success


@pytest.mark.oms
def test_queryPurChaseLifeCycleSkuPageList(global_config):
    """C端商品生命周期 - 分页列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/sku/queryPurChaseLifeCycleSkuPageList',
        {
            "pageSize": 20,
            "pageNo": 2,
            "businessTypeList": []
        }
    )
    json_data = parse_json(response, 'C端商品生命周期列表')
    assert_success(json_data, 'C端商品生命周期列表')
    print(f'C端商品生命周期列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or [] if isinstance(data, dict) else data
    if not items:
        pytest.skip('C端商品生命周期列表无数据，跳过')
    print(f'C端商品生命周期列表 数据条数: {len(items)}')
