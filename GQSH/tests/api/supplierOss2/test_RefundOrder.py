# *-*coding:utf-8 *-*
import json
import pytest
import requests

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range


BASE = '/api/supplier-admin/supplier-admin/interior'




# ──────────────────────────────────────────────
#  采购退料单
# ──────────────────────────────────────────────

"采购退料单--同步金蝶退料单"
@pytest.mark.run(order=1)
def test_syncJindieRefundOrder(global_config):
    body = {"jindieJobEnum": "PUR_MRB"}
    try:
        jd = parse_json(post_api(global_config, BASE + '/jindieJob/execute', body))
        assert_success(jd, '同步金蝶退料单')
        print(f'\n同步金蝶退料单结果: {jd.get("data")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购退料单--查询退料单列表"
@pytest.mark.run(order=2)
def test_refundOrderQueryPage(global_config):
    body = {
        "channelObj": {"supplierId": ""},
        "releaseTime": None,
        "pageNo": 1,
        "pageSize": 10,
        "adminPermissions": True,
        "refundEndDate": "",
        "refundStartDate": "",
        "channelCode": None,
        "jindieWarehouseId": None,
        "refundOrderNo": None,
        "materialName": None,
        "sourceOrderNo": None
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/refundOrder/queryPage', body))
        assert_success(jd, '查询退料单列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n退料单列表总数: {total}')
        if records:
            r = records[0]
            print(f'退料单号：  {r.get("jindieOrderNo")}')
            print(f'退料仓库：  {r.get("jindieWarehouseName")}')
            print(f'供应商：    {r.get("jindieSupplierName")}')
            print(f'物料名称：  {r.get("materialName")}')
            print(f'规格型号：  {r.get("materialSpec")}')
            print(f'采购单位：  {r.get("purchaseUnitName")}')
            print(f'退料日期：  {r.get("refundDate")}')
            print(f'退料数量：  {r.get("refundNum")}')
            print(f'退料金额：  {r.get("amount")}')
            print(f'源单编号：  {r.get("sourceBillNo")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
