# -*- coding: utf-8 -*-
"""产品组合管理 - POS缓存刷新列表 接口测试"""
import json
import os

import pytest

from utils.api_helper import parse_json, post_api, assert_success


@pytest.mark.oms
def test_refreshPageList(global_config):
    """POS缓存刷新列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/cache/refresh/pageList',
        {
            "pageSize": 20,
            "pageNo": 1
        }
    )
    json_data = parse_json(response, 'POS缓存刷新列表')
    assert_success(json_data, 'POS缓存刷新列表')
    print(f'POS缓存刷新列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    # 保存响应结果到 JSON 文件
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'screenshots')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'refreshPageList_response.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f'响应结果已保存至: {output_file}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or [] if isinstance(data, dict) else data
    if not items:
        pytest.skip('POS缓存刷新列表无数据，跳过')
    print(f'POS缓存刷新列表 数据条数: {len(items)}')


@pytest.mark.oms
def test_refreshCacheShopSkuSaleStatus(global_config):
    """POS - 循环刷新所有缓存接口"""
    # 读取 refreshPageList 响应文件
    json_path = os.path.join(
        os.path.dirname(__file__), '..', '..', '..', '..', 'screenshots',
        'refreshPageList_response.json'
    )
    with open(json_path, 'r', encoding='utf-8') as f:
        page_data = json.load(f)

    items = page_data.get('data', {}).get('list', [])
    if not items:
        pytest.skip('refreshPageList_response.json 中无 list 数据')

    print(f'共读取到 {len(items)} 条缓存刷新任务')

    for item in items:
        body = {
            "id": item.get('id'),
            "serviceType": item.get('serviceType'),
            "serviceTypeName": item.get('serviceTypeName'),
            "interfaceUniqueCode": item.get('interfaceUniqueCode'),
            "interfaceLocation": item.get('interfaceLocation'),
            "interfaceDescribe": item.get('interfaceDescribe'),
            "param": item.get('param'),
            "pushShow": item.get('pushShow', False),
            "refreshShow": item.get('refreshShow', True)
        }
        label = item.get('interfaceDescribe', '缓存刷新')
        response = post_api(
            global_config,
            '/api/shop-admin/shop-admin/cache/refresh/refresh',
            body
        )
        json_data = parse_json(response, label)
        assert_success(json_data, label)
        print(f'[{label}] id={item.get("id")} 刷新成功')

