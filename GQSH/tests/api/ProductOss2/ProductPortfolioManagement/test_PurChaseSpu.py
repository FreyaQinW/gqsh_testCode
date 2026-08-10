# -*- coding: utf-8 -*-
"""产品组合管理 - 产品管理 接口测试"""
import json
import random
import string
import time
from datetime import datetime

import pytest
import requests

from utils.api_helper import parse_json, post_api, assert_success


def _unique_purchasing_name():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"自动产品名称{timestamp}"


def _unique_bar_code():
    return ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=11))


def _extract_list_items(json_data):
    data = json_data.get('data', {})
    if isinstance(data, dict):
        return data.get('list') or data.get('records') or []
    return data if isinstance(data, list) else []


def _store_spu_context(global_config, item):
    """从列表项写入后续用例共用的 SPU 上下文"""
    purchase_spu_code = item.get('code')
    if purchase_spu_code:
        global_config['purchaseSpuCode'] = purchase_spu_code
        print(f'【采购SPU Code】{purchase_spu_code}')

    purchase_spu_id = item.get('purchaseSpuId')
    if purchase_spu_id:
        global_config['purchaseSpuId'] = purchase_spu_id
        print(f'【采购SPU ID】{purchase_spu_id}')

    spec_list = item.get('purchaseSpuSpecList') or []
    if spec_list:
        purchase_spu_spec_id = spec_list[0].get('purchaseSpuSpecId')
        if purchase_spu_spec_id:
            global_config['purchaseSpuSpecId'] = purchase_spu_spec_id
            print(f'【采购SPU Spec ID】{purchase_spu_spec_id}')


def _require_spu_fields(global_config, *keys):
    missing = [k for k in keys if not global_config.get(k)]
    if missing:
        pytest.skip(f'未获取到 {", ".join(missing)}，跳过')


@pytest.mark.oms
@pytest.mark.order(1)
def test_savePurchaseSpuInfo(global_config):
    """产品管理 - 新增采购SPU"""
    purchasing_name = _unique_purchasing_name()
    bar_code = _unique_bar_code()
    global_config['purchasingName'] = purchasing_name

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/spu/savePurchaseSpuInfo',
        {
            "type": "standard",
            "alias": "",
            "auditor": "王钦",
            "category": 4484,
            "productPoolCode": "",
            "desc": "自动化测试数据",
            "isStandard": "0",
            "isSubmit": 1,
            "parentCategory": "1000,2001,4444",
            "purchasingName": purchasing_name,
            "source": "head_purchase",
            "purchaseSpecSupplierList": [
                {
                    "barCode": bar_code,
                    "productsSeries": "",
                    "cargoOwner": "001",
                    "grossWeight": "",
                    "height": "",
                    "length": "",
                    "minimum": "100",
                    "purchasingCycle": "1",
                    "netWeight": "",
                    "originPlace": "自动化测试",
                    "purchasingManagerCode": "1020",
                    "purchasingManagerName": "董海军",
                    "purchasingUnit": "SPZXDWZ0325326",
                    "purchasingUserCode": "1015",
                    "purchasingUsername": "刘亚威",
                    "shelfLife": "1",
                    "shelfLifeUnit": "年",
                    "specUnit": "SPZXDWZ0325326",
                    "specValue": "2",
                    "specId": 1,
                    "number": "200",
                    "storageMode": "冷冻",
                    "supplierCode": "VEN00627",
                    "taxRate": "SL31_SYS",
                    "unitConversionRelationship": "1.00000",
                    "width": "",
                    "storageTemperature": "-18°c"
                }
            ],
            "blackPearlCategory": "",
            "blackPearlParentCategory": "",
            "saveScmPurchaseSceneReqModel": {
                "customerList": [],
                "usageValueList": [],
                "usageTimeList": [],
                "usageContextList": [],
                "usageMethodList": []
            },
            "editorInfoRequest": {
                "consumptionMethods": [""],
                "productFeatures": "",
                "sellingPoints": "",
                "salesScript": ""
            }
        }
    )
    json_data = parse_json(response, '新增采购SPU')
    assert_success(json_data, '新增采购SPU')
    print(f'新增采购SPU 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    data = json_data.get('data')
    if isinstance(data, str) and data:
        global_config['purchaseSpuCode'] = data
    elif isinstance(data, dict):
        code = data.get('code') or data.get('purchaseSpuCode') or data.get('purchasingSpuCode')
        if code:
            global_config['purchaseSpuCode'] = code
        spu_id = data.get('purchaseSpuId') or data.get('id')
        if spu_id:
            global_config['purchaseSpuId'] = spu_id
    print(f'【新建采购SPU】name={purchasing_name}, code={global_config.get("purchaseSpuCode")}')


@pytest.mark.oms
@pytest.mark.order(2)
def test_pagePurChaseSpuList(global_config):
    """产品管理 - 分页查询采购SPU列表 - 定位新建待审核SPU"""
    target_code = global_config.get('purchaseSpuCode') or ''
    target_name = global_config.get('purchasingName') or ''

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/spu/pagePurChaseSpuList',
        {
            "purchaseCategoryIdList": [],
            "purchaseSpuCode": target_code,
            "purchaseSpuName": target_name,
            "purchaseSpuStatus": 20,
            "purchaseSpuType": "",
            "spuSource": "",
            "businessTypeList": [],
            "brand": "",
            "page": 1,
            "limit": 50,
            "startTime": "",
            "endTime": ""
        }
    )
    json_data = parse_json(response, '产品管理SPU列表')
    assert_success(json_data, '产品管理SPU列表')
    print(f'产品管理SPU列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    items = _extract_list_items(json_data)
    if not items:
        pytest.skip('产品管理SPU列表无数据，跳过')
    print(f'产品管理SPU列表 数据条数: {len(items)}')

    matched = None
    for item in items:
        if target_code and item.get('code') == target_code:
            matched = item
            break
        if target_name and item.get('purchasingName') == target_name:
            matched = item
            break

    if matched is None:
        if target_code or target_name:
            pytest.fail(f'未找到新建SPU: code={target_code}, name={target_name}')
        matched = items[0]
        print('未指定新建SPU，回退使用列表首条')

    _store_spu_context(global_config, matched)


@pytest.mark.oms
@pytest.mark.order(3)
def test_updatePurchaseSpuInfo(global_config):
    """产品管理 - 更新采购SPU状态 - 审核"""
    _require_spu_fields(global_config, 'purchaseSpuCode')
    purchase_spu_code = global_config['purchaseSpuCode']

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/spu/updatePurchaseSpuInfo',
        {
            "auditor": "王钦",
            "purchasingSpuCode": purchase_spu_code,
            "remark": "",
            "status": "40"
        }
    )
    json_data = parse_json(response, '更新采购SPU状态')
    assert_success(json_data, '更新采购SPU状态')
    print(f'更新采购SPU状态 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(4)
def test_saveOrDelete(global_config):
    """产品管理 - 根据ID、code 配置业务类型"""
    _require_spu_fields(global_config, 'purchaseSpuId', 'purchaseSpuSpecId')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/scmSkuBusiness/saveOrDelete',
        {
            "businessTypeList": [
                "b2c", "next_day_delivery", "o2o", "digital_price_tag",
                "black_pearl", "tiktok", "f2b", "gq_ticket",
                "xc_o2o", "hk_o2o"
            ],
            "purchaseSpuId": global_config['purchaseSpuId'],
            "purchaseSpuSpecId": global_config['purchaseSpuSpecId']
        }
    )
    json_data = parse_json(response, '配置业务类型')
    assert_success(json_data, '配置业务类型')
    print(f'配置业务类型 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(5)
def test_queueConvertPublish(global_config):
    """产品管理 - 转换 、金蝶、云埔、商品中心"""
    _require_spu_fields(global_config, 'purchaseSpuId', 'purchaseSpuSpecId')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/spu/queueConvertPublish',
        {
            "purchaseSpuId": global_config['purchaseSpuId'],
            "purchaseSpuSpecId": global_config['purchaseSpuSpecId']
        }
    )
    json_data = parse_json(response, '队列转换发布')
    assert_success(json_data, '队列转换发布')
    print(f'队列转换发布 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(6)
def test_queryKingDeeDetailInfo(global_config):
    """产品管理 - 查询金蝶明细信息"""
    _require_spu_fields(global_config, 'purchaseSpuCode')
    purchase_spu_code = global_config['purchaseSpuCode']

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/product/queryKingDeeDetailInfo',
        {
            "purchasingSpuCode": purchase_spu_code
        }
    )
    json_data = parse_json(response, '查询金蝶明细信息')
    assert_success(json_data, '查询金蝶明细信息')
    print(f'查询金蝶明细信息 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    global_config['kingDeeDetailInfo'] = json_data.get('data') or {}


@pytest.mark.oms
@pytest.mark.order(7)
def test_saveKingDeeDetailInfo(global_config):
    """产品管理 - 保存金蝶明细信息"""
    _require_spu_fields(global_config, 'purchaseSpuCode', 'purchaseSpuSpecId')
    purchase_spu_code = global_config['purchaseSpuCode']
    purchase_spu_spec_id = global_config['purchaseSpuSpecId']

    kd = global_config.get('kingDeeDetailInfo')
    if not kd:
        pytest.skip('未获取到金蝶明细信息（kingDeeDetailInfo），跳过保存金蝶明细信息测试')

    king_dee_sku_code = f"{purchase_spu_code}1"
    global_config['kingDeeSkuCode'] = king_dee_sku_code
    sku = (kd.get('skuInfoModelList') or [{}])[0]

    print(f'purchaseSpuCode: {purchase_spu_code}')
    print(f'kingDeeSkuCode: {king_dee_sku_code}')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/product/saveKingDeeDetailInfo',
        {
            "initiatorProvinceCode": kd.get('initiatorProvinceCode') or '',
            "cloudAutoOnlineFlag": kd.get('cloudAutoOnlineFlag') or 0,
            "fullName": kd.get('fullName') or '',
            "brandName": kd.get('brandName') or '',
            "purchasingSpuCode": purchase_spu_code,
            "purchasingName": kd.get('purchasingName') or '',
            "kingDeeCategoryCodeList": kd.get('kingDeeCategoryCodeList') or [1000, 2001, 4444, 4484],
            "isStandard": kd.get('isStandard') or '0',
            "currency": kd.get('currency') or 'PRE001',
            "inventoryCategory": kd.get('inventoryCategory') or 'CHLB01_SYS',
            "purchasingChannel": kd.get('purchasingChannel') or 'head_purchase',
            "useProject": kd.get('useProject') or '',
            "alias": kd.get('alias') or '',
            "kit": kd.get('kit') or '0',
            "creatOrganization": kd.get('creatOrganization') or '001',
            "materialProperties": kd.get('materialProperties') or '',
            "bookkeepingGroup": kd.get('bookkeepingGroup') or '956277',
            "labelId": kd.get('labelId'),
            "skuInfoModelList": [
                {
                    "kingDeeSkuId": sku.get('kingDeeSkuId'),
                    "kingDeeSkuCode": king_dee_sku_code,
                    "purchasingSpuSpecId": purchase_spu_spec_id,
                    "kingDeeSkuStatus": sku.get('kingDeeSkuStatus', False),
                    "purchasingUserCode": sku.get('purchasingUserCode') or '1015',
                    "purchasingUsername": sku.get('purchasingUsername') or '刘亚威',
                    "purchasingManagerCode": sku.get('purchasingManagerCode') or '1020',
                    "purchasingManagerName": sku.get('purchasingManagerName') or '董海军',
                    "supplierCode": sku.get('supplierCode') or 'VEN00627',
                    "supplierName": sku.get('supplierName') or '唐山聚业机械设备制造有限公司',
                    "taxRate": sku.get('taxRate') or 'SL31_SYS',
                    "advanceReceiptDays": sku.get('advanceReceiptDays') or '1',
                    "cargoOwner": sku.get('cargoOwner') or '001',
                    "useOrganization": sku.get('useOrganization') or '001',
                    "purchaseGroupCodes": sku.get('purchaseGroupCodes') or ['1', 'GQ109'],
                    "roleCode": sku.get('roleCode') or '',
                    "specValue": sku.get('specValue') or '2g/串*200串',
                    "barCode": sku.get('barCode') or '',
                    "specUnit": sku.get('specUnit') or 'SPZXDWZ0325326',
                    "specUnitDesc": sku.get('specUnitDesc') or '件',
                    "grossWeight": sku.get('grossWeight') or '',
                    "netWeight": sku.get('netWeight') or '',
                    "length": sku.get('length') or '',
                    "width": sku.get('width') or '',
                    "height": sku.get('height') or '',
                    "purchasingSpecUnit": sku.get('purchasingSpecUnit') or 'SPZXDWZ0325326',
                    "purchasingSpecUnitDesc": sku.get('purchasingSpecUnitDesc') or '件',
                    "unitConversionRelationship": sku.get('unitConversionRelationship') or '1.00000',
                    "minimum": sku.get('minimum') or 100,
                    "purchasingCycle": sku.get('purchasingCycle') or 1,
                    "purchasePricingUnit": sku.get('purchasePricingUnit') or 'SPZXDWZ0325326',
                    "purchasePricingUnitDesc": sku.get('purchasePricingUnitDesc') or '件',
                    "stockUnit": sku.get('stockUnit') or 'SPZXDWZ0325326',
                    "stockUnitDesc": sku.get('stockUnitDesc') or '件',
                    "stockPurchaseUnitConversion": sku.get('stockPurchaseUnitConversion') or '1.00000',
                    "expireTime": sku.get('expireTime') or '1',
                    "productUnitStockConversion": sku.get('productUnitStockConversion') or '',
                    "auxiliaryUnits": sku.get('auxiliaryUnits') or 'SPZXDWZ0325326',
                    "costUnit": sku.get('costUnit') or 'SPZXDWZ0325326',
                    "auxiliaryUnitsDesc": sku.get('auxiliaryUnitsDesc') or '件',
                    "costUnitDesc": sku.get('costUnitDesc') or '件',
                    "storageMode": sku.get('storageMode') or '冷冻',
                    "originPlace": sku.get('originPlace') or '自动化测试',
                    "shelfLife": sku.get('shelfLife') or '1',
                    "shelfLifeUnit": sku.get('shelfLifeUnit') or '年',
                    "saleUnit": sku.get('saleUnit') or 'SPZXDWZ0325326',
                    "salePriceUnit": sku.get('salePriceUnit') or 'SPZXDWZ0325326',
                    "saleUnitDesc": sku.get('saleUnitDesc') or '件',
                    "salePriceUnitDesc": sku.get('salePriceUnitDesc') or '件'
                }
            ],
            "entranceFlag": kd.get('entranceFlag') or 1
        }
    )
    json_data = parse_json(response, '保存金蝶明细信息')
    assert_success(json_data, '保存金蝶明细信息')
    print(f'保存金蝶明细信息 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(8)
def test_pushProductStatusBySpu(global_config):
    """产品管理 - 推送产品状态到金蝶（轮询重试，避免固定 sleep）"""
    _require_spu_fields(global_config, 'purchaseSpuCode')
    purchase_spu_code = global_config['purchaseSpuCode']
    king_dee_sku_code = global_config.get('kingDeeSkuCode')

    request_body = {
        "channel": "kingDee",
        "purchasingSpuCode": purchase_spu_code,
        "purchasingSkuCodes": [king_dee_sku_code] if king_dee_sku_code else []
    }
    print(f'推送产品状态 请求参数: {json.dumps(request_body, ensure_ascii=False)}')

    path = '/api/third-platform/thirdplatform/admin/jindie/pushProductsBySpu'
    last_error = None
    json_data = None
    max_attempts = 6
    for attempt in range(1, max_attempts + 1):
        try:
            response = post_api(
                global_config,
                path,
                request_body,
                timeout=60,
                fail_on_error=False,
            )
            json_data = parse_json(response, '推送产品状态')
            if json_data.get('success'):
                print(f'推送产品状态成功（第{attempt}次）')
                break
            last_error = json_data.get('msg', '未知错误')
            print(f'推送产品状态第{attempt}次未成功: {last_error}')
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            print(f'推送产品状态第{attempt}次网络异常: {last_error}')

        if attempt < max_attempts:
            time.sleep(5)
    else:
        pytest.fail(f'推送产品状态失败（已重试{max_attempts}次）: {last_error}')

    assert_success(json_data, '推送产品状态')
    print(f'推送产品状态 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(9)
def test_queryKingDeeChannelSpuList(global_config):
    """渠道产品管理 - 查询金蝶渠道SPU列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/product/queryKingDeeChannelSpuList',
        {
            "pageNo": 1,
            "pageSize": 30,
            "total": 5414
        },
    )
    json_data = parse_json(response, '金蝶渠道SPU列表')
    assert_success(json_data, '金蝶渠道SPU列表')
    print(f'金蝶渠道SPU列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(10)
def test_getCloudSkuInfo(global_config):
    """产品管理 - 获取云SKU信息"""
    _require_spu_fields(global_config, 'purchaseSpuCode', 'purchaseSpuSpecId')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/cloud/getCloudSkuInfo',
        {
            "type": "edit",
            "change": 1,
            "purchaseSpuCode": global_config['purchaseSpuCode'],
            "purchaseSpuSpecId": global_config['purchaseSpuSpecId'],
            "saleUnitInfoList": [
                {
                    "saleUnit": "SPZXDWZ0325326",
                    "saleUnitValue": "件",
                    "isBasic": 0
                }
            ],
            "flag": 1,
            "hideImage": True,
            "size": 1
        },
    )
    json_data = parse_json(response, '获取云SKU信息')
    assert_success(json_data, '获取云SKU信息')
    print(f'获取云SKU信息 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(11)
def test_saveCloudSkuInfo(global_config):
    """产品管理 - 保存云SKU信息"""
    _require_spu_fields(global_config, 'purchaseSpuCode', 'purchaseSpuId', 'purchaseSpuSpecId')

    product_name = global_config.get('purchasingName') or _unique_purchasing_name()
    barCode = _unique_bar_code()

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/cloud/saveCloudSkuInfo',
        {
            "categoryId": 4484,
            "shortName": product_name,
            "fullName": product_name,
            "pricingManner": "",
            "purchaseSpuCode": global_config['purchaseSpuCode'],
            "purchaseSpuId": global_config['purchaseSpuId'],
            "skuCodeList": [],
            "skuName": product_name,
            "specQualityList": [
                {
                    "barCode": barCode,
                    "solids": None,
                    "purchaseSpuSpecId": global_config['purchaseSpuSpecId'],
                    "shippingPrice": "199",
                    "minPrice": "",
                    "saleUnit": "SPZXDWZ0325326",
                    "skuId": None,
                    "skuCode": None,
                    "supplierCode": "VEN00627",
                    "purchaseSpuSpec": "2g/串",
                    "multiple": 1,
                    "specId": 1,
                    "plannedOffTime": "",
                    "specInfo": {
                        "value": "2",
                        "specName": None,
                        "number": None,
                        "specUnit": None,
                        "spec": None,
                        "specStr": "2g/串",
                        "specId": 1
                    }
                }
            ],
            "cloudAttributeVoList": [
                {
                    "value": "2g/串",
                    "skuCode": None,
                    "saleUnit": "SPZXDWZ0325326",
                    "shippingPrice": 199,
                    "specId": 1
                }
            ],
            "checkRemovePropertyLst": [],
            "entranceFlag": 1
        },
    )
    json_data = parse_json(response, '保存云SKU信息')
    assert_success(json_data, '保存云SKU信息')
    print(f'保存云SKU信息 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(12)
def test_queryPurchaseSkuDetailInfo(global_config):
    """产品管理 - 查询采购SKU明细"""
    _require_spu_fields(global_config, 'purchaseSpuCode', 'purchaseSpuSpecId')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/sku/queryPurchaseSkuDetailInfo',
        {
            "purchaseSpuCode": global_config['purchaseSpuCode'],
            "businessTypeList": ["o2o", "next_day_delivery", "b2c", "f2b", "hk_o2o"],
            "purchaseSpuSpecId": global_config['purchaseSpuSpecId']
        }
    )
    json_data = parse_json(response, '查询采购SKU明细')
    assert_success(json_data, '查询采购SKU明细')
    print(f'查询采购SKU明细 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
@pytest.mark.order(13)
def test_savePurchaseSkuDetailInfo(global_config):
    """产品转换为商品中心"""
    _require_spu_fields(global_config, 'purchaseSpuCode', 'purchaseSpuSpecId')

    purchase_spu_code = global_config['purchaseSpuCode']
    purchasing_name = global_config.get('purchasingName') or ''
    purchase_spu_spec_id = global_config['purchaseSpuSpecId']
    barCode = _unique_bar_code()

    request_body = {
        "purchaseSpuVo": {
            "purchaseSpuId": None,
            "code": purchase_spu_code,
            "productPoolCode": None,
            "supplierProductName": None,
            "purchasingName": purchasing_name,
            "parentCategory": None,
            "firstCategory": "",
            "category": None,
            "categoryIdList": None,
            "categoryUnionName": "火锅类/肉卷类/羊肉卷类/羊肉",
            "blackPearlParentCategory": None,
            "blackPearlCategory": None,
            "blackPearlCategoryUnionName": None,
            "type": "standard",
            "typeDesc": None,
            "isStandard": "0",
            "isStandardDesc": "否",
            "source": "head_purchase",
            "sourceDesc": "锅圈直采",
            "alias": "",
            "desc": None,
            "status": None,
            "statusDesc": None,
            "createTime": None,
            "updateTime": None,
            "creatorName": None,
            "isSelected": None,
            "isShow": None,
            "jindieCode": None,
            "editorInfoRespModel": None,
            "sceneResModel": None,
            "pushKingKee": None,
            "purchasingSkuCodes": None,
            "brand": None,
            "brandDesc": None
        },
        "skuMarketingVo": {
            "userCount": None,
            "faction": None,
            "usageScenario": None,
            "discountRate": None,
            "subsidy": None,
            "plannedSaleEndAt": None,
            "subsidyBeginDate": None,
            "subsidyCloseDate": None,
            "fourPronged": None,
            "salePeriodDay": None,
            "activityCGrossProfit": None
        },
        "spuId": None,
        "spuCode": None,
        "spuName": purchasing_name,
        "shortName": purchasing_name,
        "fullName": purchasing_name,
        "skuSpuName": None,
        "spuSaleType": "standard",
        "speedCombineFlag": None,
        "commonName": purchasing_name,
        "serveType": None,
        "promotionType": None,
        "originate": None,
        "provinceList": None,
        "flag": 0,
        "skuType": None,
        "pricingManner": "common",
        "skuSpecInfoList": [
            {
                "scmPurchasingSpuSpecId": purchase_spu_spec_id,
                "skuId": None,
                "skuCode": None,
                "skuInnerCode": "0102040243",
                "specValue": "2",
                "specId": 1,
                "specUnitName": "g/串",
                "shippingPrice": None,
                "defaultSalePrice": None,
                "multiple": None,
                "plannedOffTime": None,
                "saleUnit": None,
                "saleUnitValue": None,
                "barCodeList": [
                    {
                        "barCode": barCode,
                        "barCodeUpdateTime": ""
                    }
                ],
                "weightValue": "200",
                "weightUnit": "g",
                "skuQualityControlInfo": {
                    "storageWay": "冷冻",
                    "expireTime": 1,
                    "expireTimeUnit": "年",
                    "originPlace": "自动化测试",
                    "supplierCode": "VEN00627",
                    "printReceipt": None,
                    "supplierResVoList": "唐山聚业机械设备制造有限公司"
                },
                "hasPushedChannel": False,
                "businessTypePriceList": [
                    {"businessType": "o2o", "businessName": "O2O", "businessDesc": None, "createTime": None, "updateTime": None, "shippingPrice": "199", "defaultSalePrice": "288", "classAPrice": None, "classBPrice": None, "classDPrice": None, "blackPearlPrice": None, "xiaoBPrice": None, "activityPrice": None},
                    {"businessType": "next_day_delivery", "businessName": "次日达", "businessDesc": None, "createTime": None, "updateTime": None, "shippingPrice": "199", "defaultSalePrice": "288", "classAPrice": None, "classBPrice": None, "classDPrice": None, "blackPearlPrice": None, "xiaoBPrice": None, "activityPrice": None},
                    {"businessType": "b2c", "businessName": "B2C", "businessDesc": None, "createTime": None, "updateTime": None, "shippingPrice": "199", "defaultSalePrice": "288", "classAPrice": None, "classBPrice": None, "classDPrice": None, "blackPearlPrice": None, "xiaoBPrice": None, "activityPrice": None},
                    {"businessType": "f2b", "businessName": "F2B", "businessDesc": None, "createTime": None, "updateTime": None, "shippingPrice": "199", "defaultSalePrice": "288", "classAPrice": None, "classBPrice": None, "classDPrice": None, "blackPearlPrice": None, "xiaoBPrice": None, "activityPrice": None}
                ],
                "alias": None,
                "filterProperty": None,
                "checkChannel": None,
                "f2bPriceList": [
                    {"price": "266", "priceCode": "948999", "priceName": "直销客户价格"},
                    {"price": "288", "priceCode": "814261", "priceName": "经销商价格"}
                ],
                "solids": None
            }
        ],
        "businessTypePriceList": [
            {"businessType": "o2o", "businessName": "O2O", "businessDesc": None, "createTime": None, "updateTime": None, "shippingPrice": None, "defaultSalePrice": None, "classAPrice": None, "classBPrice": None, "classDPrice": None, "blackPearlPrice": None, "xiaoBPrice": None, "activityPrice": None},
            {"businessType": "next_day_delivery", "businessName": "次日达", "businessDesc": None, "createTime": None, "updateTime": None, "shippingPrice": None, "defaultSalePrice": None, "classAPrice": None, "classBPrice": None, "classDPrice": None, "blackPearlPrice": None, "xiaoBPrice": None, "activityPrice": None},
            {"businessType": "b2c", "businessName": "B2C", "businessDesc": None, "createTime": None, "updateTime": None, "shippingPrice": None, "defaultSalePrice": None, "classAPrice": None, "classBPrice": None, "classDPrice": None, "blackPearlPrice": None, "xiaoBPrice": None, "activityPrice": None},
            {"businessType": "f2b", "businessName": "F2B", "businessDesc": None, "createTime": None, "updateTime": None, "shippingPrice": None, "defaultSalePrice": None, "classAPrice": None, "classBPrice": None, "classDPrice": None, "blackPearlPrice": None, "xiaoBPrice": None, "activityPrice": None}
        ],
        "skuThirdCodeList": [],
        "purchaseSpuModelList": [
            {
                "purchaseSpuCode": None,
                "purchaseSpuId": None,
                "code": purchase_spu_code,
                "productPoolCode": None,
                "supplierProductName": None,
                "purchaseSpuInnerCode": None,
                "purchasingName": purchasing_name,
                "firstCategory": "",
                "parentCategory": None,
                "category": None,
                "categoryIdList": None,
                "categoryUnionName": "火锅类/肉卷类/羊肉卷类/羊肉",
                "blackPearlParentCategory": None,
                "blackPearlCategory": None,
                "blackPearlCategoryUnionName": None,
                "type": "standard",
                "typeDesc": None,
                "isStandard": "0",
                "isStandardDesc": "否",
                "source": "head_purchase",
                "sourceDesc": "锅圈直采",
                "alias": "",
                "desc": None,
                "status": None,
                "statusDesc": None,
                "createTime": None,
                "updateTime": None,
                "creatorId": None,
                "creatorName": None,
                "cloudConvertOperatorId": None,
                "cloudConvertOperatorName": None,
                "isSelected": 0,
                "isShow": 0,
                "purchasingSpuSpecId": None,
                "jindieCode": None,
                "editorInfoRespModel": None,
                "sceneResModel": None,
                "pushKingKee": None,
                "purchasingSkuCodes": None,
                "brand": None,
                "brandDesc": None
            }
        ],
        "isCouponPck": None,
        "virtualType": None,
        "mainImageList": None,
        "isLunchBox": None,
        "alias": None,
        "solids": None,
        "checkChannelLst": ["mail", "meituan", "ele", "jd"],
        "checkRemovePropertyLst": [],
        "entranceFlag": 1
    }
    print(f'产品转换为商品中心 请求参数: {json.dumps(request_body, ensure_ascii=False)}')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/sku/savePurchaseSkuDetailInfo',
        request_body
    )
    json_data = parse_json(response, '产品转换为商品中心')
    assert_success(json_data, '产品转换为商品中心')
    print(f'产品转换为商品中心 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')



