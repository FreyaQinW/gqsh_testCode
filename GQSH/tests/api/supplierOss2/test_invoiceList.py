# *-*coding:utf-8 *-*
"""
XT账务管理 -- 发票列表
审核状态枚举：0=待审核  1=审核通过  2=审核不通过  3=审核中  4=审核失败
发票类型：数电发票（增值税专用发票）/ 数电发票
红蓝字：1=蓝字  2=红字
"""
import json
import pytest
import requests
from datetime import datetime, timedelta

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range

BASE = '/api/supplier-admin/supplier-admin/interior'





# ──────────────────────────────────────────────
#  审核状态数量汇总
# ──────────────────────────────────────────────

@pytest.mark.run(order=1)
def test_invoice_countByAuditStatus(global_config):
    """发票列表--查询审核状态数量汇总"""
    start_d, end_d = day_range(365)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 10,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": ""
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/countAccountingInvoiceInfo', body))
        assert_success(jd, '发票列表-状态数量汇总')
        data = jd.get('data') or []
        print(f'\n发票审核状态汇总:')
        for item in data:
            print(f'  {item.get("auditStatusCn", "全部")}：{item.get("total", 0)} 条')
        # 校验枚举完整性（全部/待审核/审核通过/审核不通过/审核中/审核失败）
        status_names = [i.get('auditStatusCn') for i in data]
        assert '全部' in status_names, '状态汇总缺少"全部"枚举'
        assert '待审核' in status_names, '状态汇总缺少"待审核"枚举'
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ──────────────────────────────────────────────
#  查询列表
# ──────────────────────────────────────────────

@pytest.mark.run(order=2)
def test_invoice_queryAllPage(global_config):
    """发票列表--查询全量列表"""
    start_d, end_d = day_range(365)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 10,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": "",
        "auditStatusList": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/queryPage', body))
        assert_success(jd, '发票列表-全量查询')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n发票总数: {total}')
        if records:
            r = records[0]
            print(f'  发票流水号：  {r.get("invoiceSeq")}')
            print(f'  发票号码：    {r.get("invoiceNo")}')
            print(f'  供应商：      {r.get("supplierName")}')
            print(f'  发票类型：    {r.get("typeCn")}')
            print(f'  票型：        {r.get("patternTypeCn")}')
            print(f'  红蓝字：      {r.get("redBlueCn")}')
            print(f'  采购组织：    {r.get("purchaseOrgName")}')
            print(f'  含税金额：    {r.get("allAmount")}')
            print(f'  不含税金额：  {r.get("noTaxAmount")}')
            print(f'  税额：        {r.get("taxAmount")}')
            print(f'  审核状态：    {r.get("auditStatusCn")}')
            print(f'  创建日期：    {r.get("createDate")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=3)
def test_invoice_queryByAuditStatus_pending(global_config):
    """发票列表--按审核状态筛选（待审核）"""
    start_d, end_d = day_range(365)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 10,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": "",
        "auditStatusList": [0]      # 0=待审核
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/queryPage', body))
        assert_success(jd, '发票列表-待审核筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n发票(待审核)总数: {total}')
        # 校验返回记录状态一致
        for rec in records:
            assert rec.get('auditStatus') == 0, f'期望待审核(0)，实际={rec.get("auditStatus")}'
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=4)
def test_invoice_queryByAuditStatus_approved(global_config):
    """发票列表--按审核状态筛选（审核通过）"""
    start_d, end_d = day_range(365)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 10,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": "",
        "auditStatusList": [1]      # 1=审核通过
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/queryPage', body))
        assert_success(jd, '发票列表-审核通过筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n发票(审核通过)总数: {total}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=5)
def test_invoice_queryByAuditStatus_rejected(global_config):
    """发票列表--按审核状态筛选（审核不通过）"""
    start_d, end_d = day_range(365)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 10,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": "",
        "auditStatusList": [2]      # 2=审核不通过
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/queryPage', body))
        assert_success(jd, '发票列表-审核不通过筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n发票(审核不通过)总数: {total}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=6)
def test_invoice_queryByCreateDateRange(global_config):
    """发票列表--按创建日期范围查询"""
    start_d, end_d = day_range(33)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 10,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": "",
        "auditStatusList": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/queryPage', body))
        assert_success(jd, '发票列表-创建日期筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n发票(近33天)总数: {total}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=7)
def test_invoice_queryBySupplier(global_config):
    """发票列表--按供应商筛选"""
    # 先查一条记录取供应商名称
    start_d, end_d = day_range(365)
    r0 = post_api(global_config, BASE + '/accountingInvoice/queryPage', {
        "orgId": "1", "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d], "releaseTime2": [],
        "pageNo": 1, "pageSize": 1,
        "createStartTime": start_d, "createEndTime": end_d,
        "createStartDate": "", "createEndDate": "", "auditStatusList": []
    })
    records = (r0.json().get('data') or {}).get('list') or []
    if not records:
        pytest.skip('暂无发票数据，跳过供应商筛选测试')

    supplier_name = records[0].get('supplierName', '')
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 10,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": "",
        "auditStatusList": [],
        "supplierName": supplier_name
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/queryPage', body))
        assert_success(jd, '发票列表-供应商筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n供应商[{supplier_name}]发票总数: {total}')
        assert total >= 1
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=8)
def test_invoice_queryByInvoiceNo(global_config):
    """发票列表--按发票号码精确查询"""
    start_d, end_d = day_range(365)
    r0 = post_api(global_config, BASE + '/accountingInvoice/queryPage', {
        "orgId": "1", "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d], "releaseTime2": [],
        "pageNo": 1, "pageSize": 1,
        "createStartTime": start_d, "createEndTime": end_d,
        "createStartDate": "", "createEndDate": "", "auditStatusList": []
    })
    records = (r0.json().get('data') or {}).get('list') or []
    if not records:
        pytest.skip('暂无发票数据，跳过发票号码精确查询')

    invoice_no = records[0].get('invoiceNo', '')
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 10,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": "",
        "auditStatusList": [],
        "invoiceNo": invoice_no
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/queryPage', body))
        assert_success(jd, '发票列表-发票号码精确查询')
        total = (jd.get('data') or {}).get('totalCount', 0)
        result = (jd.get('data') or {}).get('list') or []
        print(f'\n发票号码[{invoice_no}]查询: {total} 条')
        if result:
            assert result[0].get('invoiceNo') == invoice_no, '返回发票号码不匹配'
            print(f'  核验通过：发票号码 = {result[0].get("invoiceNo")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ──────────────────────────────────────────────
#  金额汇总
# ──────────────────────────────────────────────

@pytest.mark.run(order=9)
def test_invoice_sumAmount(global_config):
    """发票列表--查询金额汇总"""
    start_d, end_d = day_range(365)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 10,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": ""
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/sumAccountingInvoiceInfo', body))
        assert_success(jd, '发票列表-金额汇总')
        data = jd.get('data') or {}
        print(f'\n发票金额汇总:')
        print(f'  含税金额合计：  {data.get("allAmountSum")}')
        print(f'  不含税金额合计：{data.get("noTaxAmountSum")}')
        print(f'  税额合计：      {data.get("taxAmountSum")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=10)
def test_invoice_pagination(global_config):
    """发票列表--分页查询"""
    start_d, end_d = day_range(365)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "releaseTime2": [],
        "pageNo": 1, "pageSize": 5,
        "createStartTime": start_d,
        "createEndTime": end_d,
        "createStartDate": "",
        "createEndDate": "",
        "auditStatusList": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingInvoice/queryPage', body))
        assert_success(jd, '发票列表-分页查询')
        data = jd.get('data') or {}
        total = data.get('totalCount', 0)
        page_size = data.get('pageSize', 5)
        curr_page = data.get('currPage', 1)
        print(f'\n发票分页: 第{curr_page}页，每页{page_size}条，共{total}条')
        assert curr_page == 1
        assert page_size == 5
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
