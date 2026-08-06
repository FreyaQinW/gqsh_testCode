# -*- coding: utf-8 -*-
"""产品组合管理 - 小B商品SKU分页列表 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty


@pytest.mark.oms
def test_pageProdSkuXiaoBList(global_config):
    """小B商品SKU - 分页查询小B商品SKU列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/sku/xiaoB/pageProdSkuXiaoBList',
        {
            "categoryIdList": [],
            "jinDeeCode": "",
            "purchaseSpuName": "",
            "saleTypeList": [],
            "skuName": "",
            "status": "",
            "pageSize": 10,
            "pageNo": 1,
            "skuType":"cloud" # "c_sale" 两个值
        },
    )
    json_data = parse_json(response, '小B商品SKU列表')
    assert_success(json_data, '小B商品SKU列表')
    print(f'小B商品SKU列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or [] if isinstance(data, dict) else data
    if not items:
        pytest.skip('小B商品SKU列表无数据，跳过')
    print(f'小B商品SKU列表 数据条数: {len(items)}')
