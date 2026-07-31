# *-*coding:utf-8 *-*
import json
import os
import pytest
import requests

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range

# ──────────────────────────────────────────────
#  入库单管理
# ──────────────────────────────────────────────

BASE = '/api/supplier-admin/supplier-admin/interior'




# ──────────────────────────────────────────────
#  入库单管理
# ──────────────────────────────────────────────

"入库单管理--同步金蝶入库单"
@pytest.mark.run(order=1)
def test_syncJindieInboundOrder(global_config):
    body = {"jindieJobEnum": "STK_INSTOCK"}
    try:
        jd = parse_json(post_api(global_config, BASE + '/jindieJob/execute', body, timeout=30))
        assert_success(jd, '同步金蝶入库单')
        print(f'\n同步金蝶入库单结果: {jd.get("data")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"入库单管理--查询入库单列表"
@pytest.mark.run(order=2)
def test_warehousingOrderQueryPage(global_config):
    body = {
        "channelObj": {"supplierId": ""},
        "producerObj": {"producerCode": ""},
        "releaseTime": None,
        "materialChannelList": [],
        "pageNo": 1,
        "pageSize": 10,
        "adminPermissions": True,
        "warehousingEndDate": "",
        "warehousingStartDate": "",
        "supplierCode": None,
        "warehouseCode": None,
        "producerCode": None
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/warehousingOrder/queryPage', body, timeout=30))
        assert_success(jd, '查询入库单列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n入库单列表总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"入库单管理--根据采购订单号查询入库单"
@pytest.mark.run(order=3)
def test_warehousingOrderQueryByOrderNo(global_config):
    order_no = global_config.get('JINDIE_PURCHASE_ORDER_NO') or os.environ.get('JINDIE_PURCHASE_ORDER_NO')
    if not order_no:
        pytest.skip('未找到采购订单号，请与 test_orderSearch.py 联合运行')
    body = {
        "channelObj": {"supplierId": ""},
        "producerObj": {"producerCode": ""},
        "releaseTime": None,
        "materialChannelList": [],
        "pageNo": 1,
        "pageSize": 10,
        "adminPermissions": True,
        "warehousingEndDate": "",
        "warehousingStartDate": "",
        "supplierCode": None,
        "warehouseCode": None,
        "producerCode": None,
        "jindiePurchaseOrderNo": order_no
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/warehousingOrder/queryPage', body, timeout=30))
        assert_success(jd, '按采购订单号查询入库单')
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n采购订单编码：{order_no}')
        print(f'入库单数量：  {len(records)}')
        if records:
            r = records[0]
            print(f'入库单号：    {r.get("warehousingOrderNo") or r.get("orderNo")}')
            print(f'入库状态：    {r.get("statusName") or r.get("status")}')
            print(f'入库数量：    {r.get("totalNum") or r.get("warehousingNum")}')
            global_config['warehousingOrderNo'] = r.get('warehousingOrderNo') or r.get('orderNo')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
