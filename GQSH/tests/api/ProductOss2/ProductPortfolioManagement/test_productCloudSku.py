# -*- coding: utf-8 -*-
"""产品组合管理 - 云埔商品管理 接口测试
"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success


@pytest.mark.oms
@pytest.mark.order(100)
def test_queryCloudSkuListPage(global_config):
    """云埔商品管理 - 分页查询云SKU列表"""
    purchase_spu_code = global_config.get('purchaseSpuCode') or ''

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/cloud/queryCloudSkuListPage',
        {
            "shortName": "",
            "skuCode": "",
            "skuName": "",
            "spuCode": purchase_spu_code,
            "spuName": "",
            "subquery": 0,
            "labelIds": [],
            "labelGroupId": "",
            "pageNo": 1,
            "pageSize": 30
        }
    )
    json_data = parse_json(response, '云埔商品SKU列表')
    assert_success(json_data, '云埔商品SKU列表')
    print(f'云埔商品SKU列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    if isinstance(data, list):
        items = data
    print(f'云埔商品SKU列表 数据条数: {len(items)}')

    if items:
        sku_list = items[0].get('skuList') or []
        if sku_list:
            sku_code = sku_list[0].get('skuCode')
            if sku_code:
                global_config['cloudSkuCode'] = sku_code
                print(f'【云埔编码】{sku_code}')


@pytest.mark.oms
@pytest.mark.order(101)
def test_addMultipleSkuCode(global_config):
    """设置云埔报货系数"""
    cloud_sku_code = global_config.get('cloudSkuCode')
    if not cloud_sku_code:
        pytest.skip('未获取到 cloudSkuCode，跳过设置云埔报货系数测试')

    request_body = {
        "skuCode": cloud_sku_code,
        "multiple": 2,
        "status": 1,
        "shopCodeList": ["349302", "348566", "349876", "346420", "346851", "316273", "319373"],
        "startTime": "",
        "endTime": ""
    }
    print(f'设置云埔报货系数 请求参数: {json.dumps(request_body, ensure_ascii=False)}')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/cloud/addMultipleSkuCode',
        request_body
    )
    json_data = parse_json(response, '设置云埔报货系数')
    assert_success(json_data, '设置云埔报货系数')
    print(f'设置云埔报货系数 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')






@pytest.mark.oms
@pytest.mark.order(102)
def test_queryPageCouldList(global_config):
    """根据云埔编码查询列表"""
    cloud_sku_code = global_config.get('cloudSkuCode') or ''

    request_body = {
        "saleSetInfoReqModelList": [
            {"saleType": "depot", "saleDataList": []},
            {"saleType": "region", "saleDataList": []},
            {"saleType": "shop", "saleDataList": []},
            {"saleType": "shop_group", "saleDataList": []}
        ],
        "channel": "cloud",
        "categoryId": "",
        "spuName": "",
        "spuCode": "",
        "skuName": "",
        "skuCode": cloud_sku_code,
        "pageSize": 50,
        "pageNo": 1
    }
    print(f'根据云埔编码查询列表 请求参数: {json.dumps(request_body, ensure_ascii=False)}')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/sku/queryPageCouldList',
        request_body
    )
    json_data = parse_json(response, '根据云埔编码查询列表')
    assert_success(json_data, '根据云埔编码查询列表')
    print(f'根据云埔编码查询列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    if isinstance(data, list):
        items = data
    print(f'根据云埔编码查询列表 数据条数: {len(items)}')

    if items:
        spu_id = items[0].get('spuId')
        sku_list_vo = items[0].get('skuListVoList') or []
        sku_id = sku_list_vo[0].get('skuId') if sku_list_vo else None
        if spu_id:
            global_config['cloudSpuId'] = spu_id
            print(f'【云埔 spuId】{spu_id}')
        if sku_id:
            global_config['cloudSkuId'] = sku_id
            print(f'【云埔 skuId】{sku_id}')


@pytest.mark.oms
@pytest.mark.order(103)
def test_saveSpuDescInfo(global_config):
    """更新云埔商品媒资库信息"""
    cloud_spu_id = global_config.get('cloudSpuId')
    purchase_spu_code = global_config.get('purchaseSpuCode')
    cloud_sku_code = global_config.get('cloudSkuCode')
    if not cloud_spu_id or not purchase_spu_code or not cloud_sku_code:
        pytest.skip('未获取到 cloudSpuId/purchaseSpuCode/cloudSkuCode，跳过更新云埔商品媒资库信息测试')

    request_body = {
        "brandId": 1,
        "imageList": [
            {
                "mediaCode": "42e7e010536645ec9243cd289e47aa8a",
                "mediaName": "org.jpg",
                "uploadTime": "2026-08-13 10:36:21",
                "mediaUrl": "https://dev-guoquan-media.oss-cn-beijing.aliyuncs.com/42e7e010536645ec9243cd289e47aa8a.jpg",
                "originUrl": "https://dev-guoquan-media.oss-cn-beijing.aliyuncs.com/42e7e010536645ec9243cd289e47aa8a.jpg",
                "watermarkFlag": "0",
                "watermarkUrl": None,
                "watermarkId": None
            }
        ],
        "spuDetailImageList": [
            {
                "mediaCode": "adf2daec056d409098b9d1380fa94501",
                "mediaName": "org.jpg",
                "uploadTime": "2026-08-13 10:36:27",
                "mediaUrl": "https://dev-guoquan-media.oss-cn-beijing.aliyuncs.com/adf2daec056d409098b9d1380fa94501.jpg",
                "originUrl": "https://dev-guoquan-media.oss-cn-beijing.aliyuncs.com/adf2daec056d409098b9d1380fa94501.jpg",
                "watermarkFlag": None,
                "watermarkUrl": None,
                "watermarkId": None
            }
        ],
        "watermarkList": [
            {
                "mediaCode": "ea6d072e1bb54e05981cc43bc01b0c7b",
                "mediaName": "org.jpg",
                "uploadTime": "2026-08-13 10:36:31",
                "mediaUrl": "https://dev-guoquan-media.oss-cn-beijing.aliyuncs.com/ea6d072e1bb54e05981cc43bc01b0c7b.jpg",
                "originUrl": "https://dev-guoquan-media.oss-cn-beijing.aliyuncs.com/ea6d072e1bb54e05981cc43bc01b0c7b.jpg",
                "watermarkFlag": None,
                "watermarkUrl": None,
                "watermarkId": None
            }
        ],
        "videoList": [
            {"mediaUrl": ""}
        ],
        "videoImageUrl": None,
        "videoIsUrlFlag": 0,
        "spuDesc": "",
        "spuId": cloud_spu_id,
        "purchaseSpuCode": purchase_spu_code,
        "channel": "cloud",
        "channelList": ["cloud"],
        "skuCode": cloud_sku_code,
        "purchaseDesc": "",
        "purchaseExplain": ""
    }
    print(f'更新云埔商品媒资库信息 请求参数: {json.dumps(request_body, ensure_ascii=False)}')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/spu/saveSpuDescInfo',
        request_body
    )
    json_data = parse_json(response, '更新云埔商品媒资库信息')
    assert_success(json_data, '更新云埔商品媒资库信息')
    print(f'更新云埔商品媒资库信息 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(104)
def test_saveSkuSalesSettings(global_config):
    """云埔商品售卖区域设置"""
    cloud_sku_id = global_config.get('cloudSkuId')
    cloud_spu_id = global_config.get('cloudSpuId')
    if not cloud_sku_id or not cloud_spu_id:
        pytest.skip('未获取到 cloudSkuId 或 cloudSpuId，跳过云埔商品售卖区域设置测试')

    request_body = {
        "saleSetInfo": [
            {
                "saleType": "depot",
                "saleDataList": ["GK122"],
                "addList": ["GK122"],
                "delList": []
            },
            {
                "saleType": "region",
                "saleDataList": [],
                "addList": [],
                "delList": []
            },
            {
                "saleType": "shop",
                "saleDataList": [],
                "addList": [],
                "delList": []
            },
            {
                "saleType": "shop_group",
                "saleDataList": [],
                "addList": [],
                "delList": []
            }
        ],
        "status": 200,
        "skuId": cloud_sku_id,
        "spuId": cloud_spu_id
    }
    print(f'云埔商品售卖区域设置 请求参数: {json.dumps(request_body, ensure_ascii=False)}')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/sku/saveSkuSalesSettings',
        request_body
    )
    json_data = parse_json(response, '云埔商品售卖区域设置')
    assert_success(json_data, '云埔商品售卖区域设置')
    print(f'云埔商品售卖区域设置 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')



