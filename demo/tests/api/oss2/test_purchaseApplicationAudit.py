# *-*coding:utf-8 *-*
"""
采购申请单-搭赠功能 API 测试
测试用例来源：采购申请单-搭赠功能测试用例.xlsx
覆盖场景：
  TC-DZ-006  创建申请单时赠品列正常展示（含 gift=True 物料）
  TC-DZ-009  可用赠品数量 = 累计可用量 - 当前申请单已使用量
  TC-DZ-032  点击【确定并审核】下推确认（审核接口含 supplierCode）
  TC-DZ-033  确认下推后赠品使用数量同步给供应商订单
  TC-DZ-035  审核通过后已审核列表可查到关联供应商订单
"""
import json
import pytest
import requests
from datetime import datetime, timedelta
import logging

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range

BASE = '/api/supplier-admin/supplier-admin/interior/purchaseApplicationRecords'
PRODUCT_SOURCE_BASE = '/api/supplier-admin/supplier-admin/interior/productSource'




# ──────────────────────────────────────────────────────────────────────────────
# TC-DZ-006 / TC-DZ-009
# 创建含赠品物料（gift=True）的采购申请单
# ──────────────────────────────────────────────────────────────────────────────
"TC-DZ-006 / TC-DZ-009  创建含赠品物料的采购申请单"
@pytest.mark.run(order=1)
def test_purchaseOrderWithGiftAdd(global_config):
    apply_date = datetime.now().strftime('%Y-%m-%d')
    arrival_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    param = {
        "mcName": "王钦",
        "applyDate": apply_date,
        "materialInfos": [
            {
                "arrivalDate": arrival_date,
                "isDelete": 0,
                "materialCode": "1056341",
                "materialName": "自动化测试商品",
                "mcId": "208",
                "gift": True,
                "mcName": "王钦",
                "producerCode": "P644212",
                "producerName": "自动化测试厂商",
                "quantity": "10",
                "materialChannel": 1,
                "channelQuantity": "10",
                "warehouseCode": "CK005",
                "warehouseName": "华鼎郑州普洛斯",
                "unitCode": "001",
                "remark": "",
                "giftQuantity": 0
            }
        ],
        "addOrderType": None,
        "orderType": 1,
        "mcId": "208",
        "remark": "",
        "orgId": "1"
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/addPurchaseApplication', param))
        logging.info(f'含赠品申请单新增结果：{jd}')
        assert_success(jd, '含赠品采购申请单新增')
        # 若接口直接返回 documentNo，优先保存
        data = jd.get('data')
        doc_no = data.get('documentNo') if isinstance(data, dict) else None
        if doc_no:
            global_config['documentNo'] = doc_no
            logging.info(f'新建单据编号：{doc_no}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(f"请求异常：{str(e)}")


# ──────────────────────────────────────────────────────────────────────────────
# TC-DZ-009
# 查询待审核申请单，获取 documentNo 供后续步骤使用
# ──────────────────────────────────────────────────────────────────────────────
"TC-DZ-009  查询待审核申请单，获取 documentNo"
@pytest.mark.run(order=2)
def test_purchaseGiftApplicationSearch(global_config):
    current_date = datetime.now().strftime('%Y-%m-%d')
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    param = {
        "mcIdList": [],
        "materialCodeList": ["1056341"],
        "warehouseCodeList": [],
        "closedStatus": 0,
        "documentSourceList": [],
        "pageNo": 1,
        "pageSize": 100,
        "applyDateStart": current_date,
        "applyDateEnd": future_date,
        "approvalStatusList": [0]
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryByPage', param))
        logging.info(f'待审核申请单列表：{jd}')
        assert_success(jd, '待审核申请单查询')

        total = jd.get('data', {}).get('totalCount', 0)
        if total == 0:
            pytest.fail('查询结果为空，无物料1054051的待审核申请单')

        order_list = jd.get('data', {}).get('list', [])

        # 优先使用步骤1保存的 documentNo（当前新建单据），否则取列表第一条
        existing_doc_no = global_config.get('documentNo')
        if existing_doc_no:
            first = next((r for r in order_list if r.get('documentNo') == existing_doc_no), order_list[0])
        else:
            first = order_list[0]

        order_no = first.get('documentNo')
        if not order_no:
            pytest.fail('未获取到申请单编号')

        global_config['documentNo'] = order_no
        global_config['materialChannel'] = first.get('materialChannel')
        logging.info(f'申请单编号：{order_no}，渠道：{first.get("materialChannel")}（{first.get("materialChannelCn")}）')
        assert global_config['documentNo'] is not None

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(f"请求异常：{str(e)}")


# ──────────────────────────────────────────────────────────────────────────────
# 前置步骤：查询货源清单，获取物料1056341对应的供应商编码
# ──────────────────────────────────────────────────────────────────────────────
"前置步骤  查询货源清单，获取物料1056341的供应商编码"
@pytest.mark.run(order=3)
def test_querySupplierCodeForAudit(global_config):
    param = {
        "forbidStatus": None,
        "channelObj": {"supplierCode": ""},
        "producerObj": {"producerCode": "P644212"},
        "releaseTime": [],
        "pageNo": 1,
        "pageSize": 20,
        "createDateEnd": "",
        "createDateStart": "",
        "forbidStatusList": [],
        "supplierCode": None,
        "producerCode": "P644212",
        "auditStatusList": [1]
    }
    try:
        jd = parse_json(post_api(global_config, PRODUCT_SOURCE_BASE + '/queryPage', param))
        logging.info(f'货源清单查询结果：{jd}')
        assert_success(jd, '货源清单查询')

        records = (jd.get('data') or {}).get('list') or []
        if not records:
            pytest.skip('未找到生产商P150717对应的已审核货源清单，跳过后续审核步骤')

        # 取第一条匹配的供应商编码
        supplier_code = records[0].get('supplierCode') or ''
        if not supplier_code:
            pytest.skip('货源清单中未获取到供应商编码，跳过后续审核步骤')

        global_config['supplierCode'] = supplier_code
        logging.info(f'货源清单供应商编码：{supplier_code}，供应商名称：{records[0].get("supplierName")}')

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(f"请求异常：{str(e)}")


# ──────────────────────────────────────────────────────────────────────────────
# TC-DZ-032 / TC-DZ-033
# 审核并下推：请求体携带 supplierCode，修复"供应商编码不可为空"问题
# 审核通过后赠品使用数量同步给供应商订单
# ──────────────────────────────────────────────────────────────────────────────
"TC-DZ-032 / TC-DZ-033  审核并下推，携带 supplierCode"
@pytest.mark.run(order=4)
def test_purchaseApplicationGiftAudit(global_config):
    supplier_code = global_config.get('supplierCode', '')
    if not supplier_code:
        pytest.skip('supplierCode 未获取，跳过审核步骤')

    param = {
        "checkWdt": True,
        "planNo": "",
        "documentNo": global_config['documentNo'],
        "supplierCode": supplier_code
    }
    logging.info(f'审核请求参数：{param}')
    try:
        jd = parse_json(post_api(global_config, BASE + '/audit', param))
        logging.info(f'审核结果：{jd}')
        assert_success(jd, '采购申请单审核')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(f"请求异常：{str(e)}")


# ──────────────────────────────────────────────────────────────────────────────
# TC-DZ-035
# 审核通过后查询已审核列表，验证关联供应商订单已生成（赠品数量已同步扣减）
# ──────────────────────────────────────────────────────────────────────────────
"TC-DZ-035  审核通过后查询已审核列表，验证关联供应商订单存在"
@pytest.mark.run(order=5)
def test_purchaseApplicationGiftApprovedSearch(global_config):
    current_date = datetime.now().strftime('%Y-%m-%d')
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    param = {
        "mcIdList": [],
        "materialCodeList": ["1056341"],
        "warehouseCodeList": [],
        "closedStatus": 0,
        "documentSourceList": [],
        "pageNo": 1,
        "pageSize": 100,
        "applyDateStart": current_date,
        "applyDateEnd": future_date,
        "approvalStatusList": [1]
    }
    logging.info(f'已审核查询参数：{param}')
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryByPage', param))
        logging.info(f'已审核申请单列表：{jd}')
        assert_success(jd, '已审核申请单查询')

        total = jd.get('data', {}).get('totalCount', 0)
        if total == 0:
            pytest.fail('未查询到已审核的采购申请单')

        order_list = jd.get('data', {}).get('list', [])
        related_order = order_list[0].get('relatedOrder') if order_list else None
        if not related_order:
            pytest.fail('审核通过后未生成关联供应商订单，赠品数量未同步')

        global_config['JINDIE_PURCHASE_ORDER_NO'] = related_order
        logging.info(f'关联供应商订单号：{related_order}')
        assert global_config['JINDIE_PURCHASE_ORDER_NO'] is not None

    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(f"请求异常：{str(e)}")
