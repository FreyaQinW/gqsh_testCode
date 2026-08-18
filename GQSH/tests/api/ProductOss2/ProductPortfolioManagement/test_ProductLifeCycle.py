# -*- coding: utf-8 -*-
"""产品组合管理 - 产品生命周期 接口测试"""
import json
from datetime import datetime

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty


@pytest.mark.oms
def test_queryLifeCycleList(global_config, product_ctx):
    """产品生命周期 - 查询产品生命周期列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/lifecycle/queryLifeCycleList',
        {
            "categoryIdList": [],
            "pageNo": 1,
            "pageSize": 10,
            "tabCode": "sh_gq"
        },
    )
    json_data = parse_json(response, '产品生命周期列表')
    assert_success(json_data, '产品生命周期列表')
    print(f'产品生命周期列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '产品生命周期列表', skip_if_empty=True)

    # 提取首条记录的 purchaseSpuCode，传递给后续测试
    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    if items:
        purchase_spu_code = items[0].get('purchaseSpuCode')
        product_ctx['purchaseSpuCode'] = purchase_spu_code
        print(f'产品生命周期 purchaseSpuCode: {purchase_spu_code}')


@pytest.mark.oms
def test_queryLifeCycleDetailsList(global_config, product_ctx):
    """产品生命周期 - 查询产品生命周期明细列表"""
    purchase_spu_code = product_ctx.get('purchaseSpuCode')
    if not purchase_spu_code:
        pytest.skip('未获取到 purchaseSpuCode，跳过明细列表测试')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/lifecycle/queryLifeCycleDetailsList',
        {
            "purchaseSpuCode": purchase_spu_code
        },
    )
    json_data = parse_json(response, '产品生命周期明细列表')
    assert_success(json_data, '产品生命周期明细列表')
    print(f'产品生命周期明细列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    # 提取首条记录的 deptCode，传递给后续测试
    data = json_data.get('data', [])
    items = data if isinstance(data, list) else (data.get('list') or data.get('records') or [])
    if not items:
        pytest.skip('产品生命周期明细列表无数据，跳过')
    dept_code = items[0].get('deptCode')
    product_ctx['deptCode'] = dept_code
    print(f'产品生命周期明细 deptCode: {dept_code}')


@pytest.mark.oms
def test_queryLifeCycleDetailsList1(global_config, product_ctx):
    """产品生命周期 - 查询产品生命周期明细列表（含deptCode）"""
    purchase_spu_code = product_ctx.get('purchaseSpuCode')
    dept_code = product_ctx.get('deptCode')
    if not purchase_spu_code or not dept_code:
        pytest.skip('未获取到 purchaseSpuCode 或 deptCode，跳过明细列表测试')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/lifecycle/queryLifeCycleDetailsList',
        {
            "purchaseSpuCode": purchase_spu_code,
            "deptCode": dept_code
        },
    )
    json_data = parse_json(response, '产品生命周期明细列表1')
    assert_success(json_data, '产品生命周期明细列表1')
    print(f'产品生命周期明细列表1 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    # 提取首条记录的 prodLifeHouseId，传递给后续测试
    data = json_data.get('data', [])
    items = data if isinstance(data, list) else (data.get('list') or data.get('records') or [])
    if not items:
        pytest.skip('产品生命周期明细列表1无数据，跳过')
    prod_life_house_id = items[0].get('prodLifeHouseId')
    product_ctx['prodLifeHouseId'] = prod_life_house_id
    print(f'产品生命周期明细 prodLifeHouseId: {prod_life_house_id}')


@pytest.mark.oms
def test_queryLifeCycleTypeList(global_config, product_ctx):
    """产品生命周期 - 查询生命周期类型列表"""
    prod_life_house_id = product_ctx.get('prodLifeHouseId')
    if not prod_life_house_id:
        pytest.skip('未获取到 prodLifeHouseId，跳过类型列表测试')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/lifecycle/queryLifeCycleTypeList',
        {
            "prodLifeHouseId": prod_life_house_id
        },
    )
    json_data = parse_json(response, '生命周期类型列表')
    assert_success(json_data, '生命周期类型列表')
    print(f'生命周期类型列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    # 提取首条记录的 value，传递给后续测试
    data = json_data.get('data', [])
    items = data if isinstance(data, list) else (data.get('list') or data.get('records') or [])
    if not items:
        pytest.skip('生命周期类型列表无数据，跳过')
    life_cycle_type_value = items[0].get('value')
    product_ctx['lifeCycleTypeValue'] = life_cycle_type_value
    print(f'生命周期类型 value: {life_cycle_type_value}')


@pytest.mark.oms
def test_updateScmLifeCycle(global_config, product_ctx):
    """产品生命周期 - 更新产品生命周期状态"""
    prod_life_house_id = product_ctx.get('prodLifeHouseId')
    life_cycle_type_value = product_ctx.get('lifeCycleTypeValue')
    jinDeeCode = product_ctx.get('purchaseSpuCode')
    if not prod_life_house_id or not life_cycle_type_value:
        pytest.skip('未获取到 prodLifeHouseId 或 lifeCycleTypeValue，跳过更新测试')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/lifecycle/updateScmLifeCycle',
        {
            "id": prod_life_house_id,
            "prodLifeCycleType": life_cycle_type_value,
            "stock": None,
            "remark": "审厂未通过",
            "repertoryNumber": None,
            "availableDay": None,
            "jinDeeCode": jinDeeCode
        },
    )
    json_data = parse_json(response, '更新产品生命周期')
    # 接口可能返回“当前已经是短期禁下单无需修改”，均为有效业务响应
    success = json_data.get('success', False)
    msg = json_data.get('msg', '')
    assert success or '无需修改' in msg or '已经' in msg, f'更新产品生命周期失败：{msg}'
    print(f'更新产品生命周期 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
def test_queryLifeCycleByJinDieCodeList(global_config, product_ctx):
    """产品生命周期 - 根据金蝶编码查询生命周期列表"""
    purchase_spu_code = product_ctx.get('purchaseSpuCode')
    if not purchase_spu_code:
        pytest.skip('未获取到 purchaseSpuCode，跳过金蝶编码查询测试')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/lifecycle/queryLifeCycleByJinDieCodeList',
        {
            "jindieCode": f"{purchase_spu_code}1"
        },
    )
    json_data = parse_json(response, '金蝶编码生命周期列表')
    assert_success(json_data, '金蝶编码生命周期列表')
    print(f'金蝶编码生命周期列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', [])
    items = data if isinstance(data, list) else (data.get('list') or data.get('records') or [])
    if not items:
        pytest.skip('金蝶编码生命周期列表无数据，跳过')
    print(f'金蝶编码生命周期列表 数据条数: {len(items)}')
