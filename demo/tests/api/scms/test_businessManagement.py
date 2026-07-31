# *-*coding:utf-8 *-*
from datetime import datetime, timedelta
import requests
import pytest
import json

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range




BASE = '/api/supplier-admin/supplier-admin/supplier'
COMMON = '/api/supplier-admin/supplier-admin/common'




# ──────────────────────────────────────────────
#  准交率
# ──────────────────────────────────────────────

"业务管理--准交率--查询仓库列表"
@pytest.mark.run(order=1)
def test_warehouseSelectList(global_config):
    resp = post_api(global_config, BASE + '/warehouse/selectList', {})
    try:
        jd = resp.json()
        assert_success(jd, '准交率-仓库列表')
        print('仓库列表数量:', len(jd.get('data') or []))
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


"业务管理--准交率--查询列表"
@pytest.mark.run(order=2)
def test_orderCrossingStatQueryPage(global_config):
    param = {
        "updateTime": [],
        "pageNo": 1,
        "pageSize": 10,
        "rqArrivalEndDate": "",
        "rqArrivalStartDate": ""
    }
    resp = post_api(global_config, BASE + '/orderCrossingStat/queryPage', param)
    try:
        jd = resp.json()
        assert_success(jd, '准交率列表')
        total = jd.get('data', {}).get('totalCount', 0)
        print(f'准交率列表总数: {total}')
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


# ──────────────────────────────────────────────
#  延期申请
# ──────────────────────────────────────────────

"业务管理--延期申请--查询条件枚举"
@pytest.mark.run(order=3)
def test_delayApplyConditions(global_config):
    param = {"typeList": ["purchase_delay_audit_status", "material_channel_enum"]}
    resp = post_api(global_config, COMMON + '/conditionsQuery/queryConditionListByType', param)
    try:
        jd = resp.json()
        assert_success(jd, '延期申请-条件枚举')
        print('延期申请枚举项:', list((jd.get('data') or {}).keys()))
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


"业务管理--延期申请--查询列表"
@pytest.mark.run(order=4)
def test_purchaseDelayApplyQueryPage(global_config):
    param = {
        "releaseTime1": [],
        "releaseTime2": [],
        "releaseTime3": [],
        "pageNo": 1,
        "pageSize": 10,
        "createStartTime": "",
        "createEndTime": "",
        "deliveryStartTime": "",
        "deliveryEndTime": "",
        "delayStartTime": "",
        "delayEndTime": ""
    }
    resp = post_api(global_config, BASE + '/purchaseDelayApply/queryPage', param)
    try:
        jd = resp.json()
        assert_success(jd, '延期申请列表')
        total = jd.get('data', {}).get('totalCount', 0)
        print(f'延期申请列表总数: {total}')
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


# ──────────────────────────────────────────────
#  排产计划
# ──────────────────────────────────────────────

"业务管理--排产计划--查询状态枚举"
@pytest.mark.run(order=5)
def test_productionPlanConditions(global_config):
    param = {"typeList": ["supplier_production_plan_status"]}
    resp = post_api(global_config, COMMON + '/conditionsQuery/queryConditionListByType', param)
    try:
        jd = resp.json()
        assert_success(jd, '排产计划-状态枚举')
        print('排产计划枚举项:', list((jd.get('data') or {}).keys()))
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


"业务管理--排产计划--查询列表"
@pytest.mark.run(order=6)
def test_productionPlanQueryPage(global_config):
    start_m, end_m = month_range()
    param = {
        "releaseTime": [start_m, end_m],
        "pageNo": 1,
        "pageSize": 10,
        "statEndDate": end_m,
        "statStartDate": start_m
    }
    resp = post_api(global_config, BASE + '/productionPlan/queryPage', param)
    try:
        jd = resp.json()
        assert_success(jd, '排产计划列表')
        total = jd.get('data', {}).get('totalCount', 0)
        print(f'排产计划列表总数: {total}')
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


# ──────────────────────────────────────────────
#  入库列表
# ──────────────────────────────────────────────

"业务管理--入库列表--查询渠道枚举"
@pytest.mark.run(order=7)
def test_warehousingConditions(global_config):
    param = {"typeList": ["material_channel_enum"]}
    resp = post_api(global_config, COMMON + '/conditionsQuery/queryConditionListByType', param)
    try:
        jd = resp.json()
        assert_success(jd, '入库列表-渠道枚举')
        print('入库渠道枚举项:', list((jd.get('data') or {}).keys()))
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


"业务管理--入库列表--查询列表"
@pytest.mark.run(order=8)
def test_warehousingOrderQueryPage(global_config):
    start_d, end_d = day_range(60)
    param = {
        "channelObj": {"supplierId": ""},
        "producerObj": {"producerCode": ""},
        "releaseTime": [start_d, end_d],
        "pageNo": 1,
        "pageSize": 10,
        "adminPermissions": True,
        "warehousingEndDate": end_d,
        "warehousingStartDate": start_d,
        "supplierCode": None,
        "warehouseCode": None,
        "producerCode": None
    }
    resp = post_api(global_config, BASE + '/warehousingOrder/queryPage', param)
    try:
        jd = resp.json()
        assert_success(jd, '入库列表')
        total = jd.get('data', {}).get('totalCount', 0)
        print(f'入库列表总数: {total}')
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


# ──────────────────────────────────────────────
#  采购退料
# ──────────────────────────────────────────────

"业务管理--采购退料--查询列表"
@pytest.mark.run(order=9)
def test_receiveOrderQueryPage(global_config):
    start_d, end_d = day_range(60)
    param = {
        "channelObj": {"supplierId": ""},
        "releaseTime": [start_d, end_d],
        "pageNo": 1,
        "pageSize": 10,
        "refundEndDate": end_d,
        "refundStartDate": start_d,
        "jindieWarehouseId": None
    }
    resp = post_api(global_config, BASE + '/receiveOrder/queryPage', param)
    try:
        jd = resp.json()
        assert_success(jd, '采购退料列表')
        total = jd.get('data', {}).get('totalCount', 0)
        print(f'采购退料列表总数: {total}')
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


# ──────────────────────────────────────────────
#  赔付列表
# ──────────────────────────────────────────────

"业务管理--赔付列表--查询条件枚举"
@pytest.mark.run(order=10)
def test_claimConditions(global_config):
    param = {"typeList": ["yes_no_int_status", "claim_duty"]}
    resp = post_api(global_config, COMMON + '/conditionsQuery/queryConditionListByType', param)
    try:
        jd = resp.json()
        assert_success(jd, '赔付列表-条件枚举')
        print('赔付枚举项:', list((jd.get('data') or {}).keys()))
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")


"业务管理--赔付列表--查询列表"
@pytest.mark.run(order=11)
def test_claimQuerySupplierClaimList(global_config):
    param = {
        "releaseTime": [],
        "supplierDuty": None,
        "pageNo": 1,
        "pageSize": 10,
        "edate": "",
        "sdate": "",
        "etime": "",
        "stime": ""
    }
    resp = post_api(global_config, BASE + '/claim/querySupplierClaimList', param)
    try:
        jd = resp.json()
        assert_success(jd, '赔付列表')
        total = jd.get('data', {}).get('totalCount', 0)
        print(f'赔付列表总数: {total}')
    except json.JSONDecodeError as e:
        pytest.fail(f"JSON 解析失败：{e}")
    except requests.exceptions.RequestException as e:
        pytest.fail(f"网络请求失败：{e}")
