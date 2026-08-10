# -*- coding: utf-8 -*-
"""产品组合管理 - 商品售卖区域设置 接口测试
可设置O2O、云埔、B2C、次日达、F2B的商品设置
"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success


@pytest.mark.oms
@pytest.mark.order(1)
def test_queryPageThumbnailSkuWithSpuModelStatusList(global_config):
    """O2O商品售卖管理 - 分页查询缩略图SKU列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/sku/queryPageThumbnailSkuWithSpuModelStatusList',
        {
            "channel": "product",
            "businessType": "o2o",
            "spuName": "",
            "pageSize": 50,
            "pageNo": 1
        }
    )
    json_data = parse_json(response, 'O2O商品售卖管理列表')
    assert_success(json_data, 'O2O商品售卖管理列表')
    print(f'O2O商品售卖管理列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    if isinstance(data, list):
        items = data
    print(f'O2O商品售卖管理列表 数据条数: {len(items)}')
