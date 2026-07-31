# *-*coding:utf-8 *-*
import json
import pytest
import requests
from datetime import datetime, timedelta

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range


BASE = '/api/supplier-admin/supplier-admin/interior/materialContrast'




# ──────────────────────────────────────────────
#  XT基础资料 -- 物料对照表
# ──────────────────────────────────────────────

"物料对照表--查询列表"
@pytest.mark.run(order=1)
def test_materialContrastQueryPage(global_config):
    body = {
        "pageNo": 1,
        "pageSize": 10,
        "jindieMaterialCode": None,    # 物料编码（购方）
        "jindieMaterialName": None,    # 物料名称（购方）
        "invoiceMaterialName": None,   # 物料名称（销方）
        "auditStatus": None,           # 审核状态
        "channelCode": None,           # 供应商
        "updateStartTime": None,       # 更新日期开始
        "updateEndTime": None          # 更新日期结束
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '物料对照表-查询列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n物料对照表总数: {total}')
        if records:
            r = records[0]
            print(f'供应商：          {r.get("channelName")}')
            print(f'物料编码（购方）： {r.get("jindieMaterialCode")}')
            print(f'物料名称（购方）： {r.get("jindieMaterialName")}')
            print(f'规格（购方）：     {r.get("jindieMaterialSpec")}')
            print(f'计价单位（购方）： {r.get("jindieMaterialUnit")}')
            print(f'物料编码（销方）： {r.get("invoiceMaterialCode")}')
            print(f'物料名称（销方）： {r.get("invoiceMaterialName")}')
            print(f'规格（销方）：     {r.get("invoiceMaterialSpec")}')
            print(f'计价单位（销方）： {r.get("invoiceMaterialUnit")}')
            print(f'更新时间：         {r.get("updateTime")}')
            print(f'审核状态：         {r.get("auditStatusDesc")}')
            global_config['materialContrastId'] = r.get('jindieHeadId')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"物料对照表--按审核状态查询（待审核）"
@pytest.mark.run(order=2)
def test_materialContrastQueryByAuditStatus(global_config):
    body = {
        "pageNo": 1,
        "pageSize": 10,
        "jindieMaterialCode": None,
        "jindieMaterialName": None,
        "invoiceMaterialName": None,
        "auditStatus": 0,              # 0=待审核
        "channelCode": None,
        "updateStartTime": None,
        "updateEndTime": None
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '物料对照表-待审核列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n待审核物料对照表总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"物料对照表--按更新日期范围查询（近60天）"
@pytest.mark.run(order=3)
def test_materialContrastQueryByDateRange(global_config):
    end_d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start_d = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d %H:%M:%S')
    body = {
        "pageNo": 1,
        "pageSize": 10,
        "jindieMaterialCode": None,
        "jindieMaterialName": None,
        "invoiceMaterialName": None,
        "auditStatus": None,
        "channelCode": None,
        "updateStartTime": start_d,
        "updateEndTime": end_d
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '物料对照表-按日期查询')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n近60天物料对照表总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
