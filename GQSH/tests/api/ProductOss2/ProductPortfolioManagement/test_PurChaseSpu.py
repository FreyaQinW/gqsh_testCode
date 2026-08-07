# -*- coding: utf-8 -*-
"""产品组合管理 - 产品管理 接口测试"""
import json
import os
import random
import string
import time
from datetime import datetime

import pytest

from utils.api_helper import parse_json, post_api, assert_success


@pytest.mark.oms
def test_savePurchaseSpuInfo(global_config):
    """产品管理 - 新增采购SPU"""
    # 使用时间戳确保名称唯一
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    purchasing_name = f"自动产品名称{timestamp}"

    # 生成唯一 barCode：7位数字 + 随机字母
    bar_code = ''.join(random.choices(string.digits, k=7)) + ''.join(random.choices(string.ascii_uppercase, k=3))

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



@pytest.mark.oms
def test_pagePurChaseSpuList(global_config):
    """产品管理 - 分页查询采购SPU列表 - 待审核状态"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/spu/pagePurChaseSpuList',
        {
            "purchaseCategoryIdList": [],
            "purchaseSpuCode": "",
            "purchaseSpuName": "",
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

    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or [] if isinstance(data, dict) else data
    if not items:
        pytest.skip('产品管理SPU列表无数据，跳过')
    print(f'产品管理SPU列表 数据条数: {len(items)}')

    # 提取首条记录保存为 JSON 文件
    first_item = items[0]
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'screenshots')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'pagePurChaseSpuList_first_item_response.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(first_item, f, ensure_ascii=False, indent=2)
    print(f'首条记录已保存至: {output_file}')

    # 提取首条记录的 code 和 id，保存为公共参数
    purchase_spu_code = first_item.get('code')
    if purchase_spu_code:
        global_config['purchaseSpuCode'] = purchase_spu_code
        print(f'【采购SPU Code】{purchase_spu_code}')

    purchase_spu_id = first_item.get('purchaseSpuId')
    if purchase_spu_id:
        global_config['purchaseSpuId'] = purchase_spu_id
        print(f'【采购SPU ID】{purchase_spu_id}')

    # 提取嵌套的 purchaseSpuSpecId
    spec_list = first_item.get('purchaseSpuSpecList') or []
    if spec_list:
        purchase_spu_spec_id = spec_list[0].get('purchaseSpuSpecId')
        if purchase_spu_spec_id:
            global_config['purchaseSpuSpecId'] = purchase_spu_spec_id
            print(f'【采购SPU Spec ID】{purchase_spu_spec_id}')
    


@pytest.mark.oms
def test_updatePurchaseSpuInfo(global_config):
    """产品管理 - 更新采购SPU状态 - 审核"""
    purchase_spu_code = global_config.get('purchaseSpuCode')
    if not purchase_spu_code:
        pytest.skip('未获取到采购SPU Code，跳过更新测试')

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
def test_saveOrDelete(global_config):
    """产品管理 - 根据ID、code 配置业务类型"""
    purchase_spu_id = global_config.get('purchaseSpuId')
    purchase_spu_spec_id = global_config.get('purchaseSpuSpecId')
    if not purchase_spu_id or not purchase_spu_spec_id:
        pytest.skip('未获取到 purchaseSpuId 或 purchaseSpuSpecId，跳过配置业务类型测试')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/scmSkuBusiness/saveOrDelete',
        {
            "businessTypeList": [
                "b2c", "next_day_delivery", "o2o", "digital_price_tag",
                "black_pearl", "tiktok", "f2b", "gq_ticket",
                "xc_o2o", "hk_o2o"
            ],
            "purchaseSpuId": purchase_spu_id,
            "purchaseSpuSpecId": purchase_spu_spec_id
        }
    )
    json_data = parse_json(response, '配置业务类型')
    assert_success(json_data, '配置业务类型')
    print(f'配置业务类型 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')



@pytest.mark.oms
def test_queueConvertPublish(global_config):
    """产品管理 - 转换 、金蝶、云埔、商品中心"""
    purchase_spu_id = global_config.get('purchaseSpuId')
    purchase_spu_spec_id = global_config.get('purchaseSpuSpecId')
    if not purchase_spu_id or not purchase_spu_spec_id:
        pytest.skip('未获取到 purchaseSpuId 或 purchaseSpuSpecId，跳过队列转换发布测试')

    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin/purchase/spu/queueConvertPublish',
        {
            "purchaseSpuId": purchase_spu_id,
            "purchaseSpuSpecId": purchase_spu_spec_id
        }
    )
    json_data = parse_json(response, '队列转换发布')
    assert_success(json_data, '队列转换发布')
    print(f'队列转换发布 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')




@pytest.mark.oms
def test_queryKingDeeDetailInfo(global_config):
    """产品管理 - 查询金蝶明细信息"""
    purchase_spu_code = global_config.get('purchaseSpuCode')
    if not purchase_spu_code:
        pytest.skip('未获取到采购SPU Code，跳过查询金蝶明细信息测试')

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

    # 保存响应结果到 JSON 文件
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'screenshots')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'queryKingDeeDetailInfo_response.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f'响应结果已保存至: {output_file}')



@pytest.mark.oms
def test_saveKingDeeDetailInfo(global_config):
    """产品管理 - 保存金蝶明细信息"""
    purchase_spu_code = global_config.get('purchaseSpuCode')
    purchase_spu_spec_id = global_config.get('purchaseSpuSpecId')
    if not purchase_spu_code or not purchase_spu_spec_id:
        pytest.skip('未获取到 purchaseSpuCode 或 purchaseSpuSpecId，跳过保存金蝶明细信息测试')

    # kingDeeSkuCode = purchaseSpuCode + "1"
    king_dee_sku_code = f"{purchase_spu_code}1"
    global_config['kingDeeSkuCode'] = king_dee_sku_code

    # 从 queryKingDeeDetailInfo_response.json 读取字段值
    json_file = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'screenshots', 'queryKingDeeDetailInfo_response.json')
    with open(json_file, 'r', encoding='utf-8') as f:
        kingdee_data = json.load(f)
    kd = kingdee_data.get('data', {})
    sku = kd.get('skuInfoModelList', [{}])[0]

    print(f'kingDeeSkuCode: {purchase_spu_code}')
    print (f'kingDeeSkuCode: {king_dee_sku_code}')

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
def test_pushProductStatusBySpu(global_config):
    """产品管理 - 推送产品状态到金蝶"""
    purchase_spu_code = global_config.get('purchaseSpuCode')
    kingDeeSkuCode = global_config.get('kingDeeSkuCode')
    if not purchase_spu_code:
        pytest.skip('未获取到采购SPU Code，跳过推送产品状态测试')

    # 等待30秒，确保金蝶明细保存完成
    print('等待30秒后执行推送产品状态...')
    time.sleep(30)

    request_body = {
        "channel":"kingDee",
        "purchasingSpuCode":purchase_spu_code,
        "purchasingSkuCodes":[kingDeeSkuCode]
        }
    print(f'推送产品状态 请求参数: {json.dumps(request_body, ensure_ascii=False)}')

    response = post_api(
        global_config,
        '/api/third-platform/thirdplatform/admin/jindie/pushProductsBySpu',
        request_body
    )
    json_data = parse_json(response, '推送产品状态')
    assert_success(json_data, '推送产品状态')
    print(f'推送产品状态 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
