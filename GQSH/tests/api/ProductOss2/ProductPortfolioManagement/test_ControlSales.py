# -*- coding: utf-8 -*-
"""产品组合管理 - 商品控销管理 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success


@pytest.mark.oms
def test_queryControlSalesPage(global_config, product_ctx):
    """商品控销管理 - 分页查询控销列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/controlSales/queryControlSalesPage',
        {
            "pageNo": 1,
            "pageSize": 10,
            "auditStatus":0
        }
    )
    json_data = parse_json(response, '商品控销管理列表')
    assert_success(json_data, '商品控销管理列表')
    print(f'商品控销管理列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    if isinstance(data, list):
        items = data
    print(f'商品控销管理列表 数据条数: {len(items)}')

    # 提取商品控销管理相关字段作为公共参数
    if items:
        product_ctx['controlSalesNo'] = items[0].get('controlSalesNo')
        product_ctx['billType'] = items[0].get('billType')
        product_ctx['salesType'] = items[0].get('salesType')
        print(f'商品控销管理 controlSalesNo: {product_ctx["controlSalesNo"]}')
        print(f'商品控销管理 billType: {product_ctx["billType"]}')
        print(f'商品控销管理 salesType: {product_ctx["salesType"]}')


@pytest.mark.oms
def test_saveProdControlSales(global_config, product_ctx):
    """商品控销管理 - 编辑修改控销单"""
    control_sales_no = product_ctx.get('controlSalesNo')
    bill_type = product_ctx.get('billType')
    sales_type = product_ctx.get('salesType')
    if not control_sales_no or not bill_type or not sales_type:
        pytest.skip('未获取到商品控销管理公共参数，跳过编辑修改控销单测试')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/controlSales/saveProdControlSales',
        {
            "billType": bill_type,
            "shopCodeList": [],
            "controlSalesNo": control_sales_no,
            "prodControlSalesDetailModelList": [
                {"skuCode": "18705563", "beforeSkuStatus": 200, "skuStatus": 200},
                {"skuCode": "37593137", "beforeSkuStatus": 200, "skuStatus": 200},
                {"skuCode": "48046389", "beforeSkuStatus": 200, "skuStatus": 200},
                {"skuCode": "48180096", "beforeSkuStatus": 200, "skuStatus": 200},
                {"skuCode": "53064177", "beforeSkuStatus": 200, "skuStatus": 200},
                {"skuCode": "57138418", "beforeSkuStatus": 200, "skuStatus": 200},
                {"skuCode": "64285973", "beforeSkuStatus": 200, "skuStatus": 200},
                {"skuCode": "67345607", "beforeSkuStatus": 200, "skuStatus": 200},
                {"skuCode": "92060818", "beforeSkuStatus": 200, "skuStatus": 200},
                {"skuCode": "92442307", "beforeSkuStatus": 200, "skuStatus": 200}
            ],
            "effectiveTime": "",
            "effectiveWay": 1,
            "notes": "新增商品",
            "salesType": sales_type
        }
    )
    json_data = parse_json(response, '编辑修改控销单')
    assert_success(json_data, '编辑修改控销单')
    print(f'编辑修改控销单 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
def test_queryPurChaseSkuPageList(global_config, product_ctx):
    """商品控销管理 - 查询采购SKU分页列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/sku/queryPurChaseSkuPageList',
        {
            "pageNo": 1,
            "pageSize": 10,
            "subquery": 0,
            "channel": "mail",
            "skuStatusLis": [100, 200, 400],
            "businessTypeList": []
        }
    )
    json_data = parse_json(response, '采购SKU分页列表')
    assert_success(json_data, '采购SKU分页列表')
    print(f'采购SKU分页列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    if isinstance(data, list):
        items = data
    print(f'采购SKU分页列表 数据条数: {len(items)}')
    if items:
        print(f'采购SKU分页列表 第一条数据: {json.dumps(items[0], ensure_ascii=False, indent=2)}')

    # 提取商品控销管理 skuCode 作为公共参数
    if items:
        product_ctx['controlSalesSkuCode'] = items[0].get('skuCode')
        print(f'商品控销管理 skuCode: {product_ctx["controlSalesSkuCode"]}')

