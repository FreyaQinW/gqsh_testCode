# -*- coding: utf-8 -*-
"""产品组合管理 - O2O商品列表 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success


@pytest.mark.oms
def test_pageSpuModelList_O2O(global_config):
    """O2O商品列表 - 分页查询SPU模型列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/spu/pageSpuModelList',
        {
            "categoryIdList": [],
            "businessType": "o2o",
            "releaseEndTime": "",
            "releaseStartTime": "",
            "spuCode": "",
            "spuName": "",
            "source": "",
            "status": None,
            "spuType": "normal",
            "pageNo": 1,
            "pageSize": 50
        }
    )
    json_data = parse_json(response, 'O2O商品列表')
    assert_success(json_data, 'O2O商品列表')
    print(f'O2O商品列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    if isinstance(data, list):
        items = data
    print(f'O2O商品列表 数据条数: {len(items)}')


@pytest.mark.oms
def test_pageSpuModelList_B2C(global_config):
    """B2C商品列表 - 分页查询SPU模型列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/spu/pageSpuModelList',
        {
            "categoryIdList": [],
            "businessType": "b2c",
            "releaseEndTime": "",
            "releaseStartTime": "",
            "spuCode": "",
            "spuName": "",
            "source": "",
            "status": None,
            "spuType": "normal",
            "pageNo": 1,
            "pageSize": 50
        }
    )
    json_data = parse_json(response, 'B2C商品列表')
    assert_success(json_data, 'B2C商品列表')
    print(f'B2C商品列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    if isinstance(data, list):
        items = data
    print(f'B2C商品列表 数据条数: {len(items)}')


@pytest.mark.oms
def test_pageSpuModelList_NextDayDelivery(global_config):
    """次日达商品列表 - 分页查询SPU模型列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/spu/pageSpuModelList',
        {
            "categoryIdList": [],
            "businessType": "next_day_delivery",
            "releaseEndTime": "",
            "releaseStartTime": "",
            "spuCode": "",
            "spuName": "",
            "source": "",
            "status": None,
            "spuType": "normal",
            "pageNo": 1,
            "pageSize": 50
        }
    )
    json_data = parse_json(response, '次日达商品列表')
    assert_success(json_data, '次日达商品列表')
    print(f'次日达商品列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    if isinstance(data, list):
        items = data
    print(f'次日达商品列表 数据条数: {len(items)}')
    
