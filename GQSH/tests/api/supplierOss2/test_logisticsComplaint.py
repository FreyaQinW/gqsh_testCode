# *-*coding:utf-8 *-*
"""
XT账务管理 -- 物流客诉
页面字段：赔付单号 / 供应商 / 客户名称 / 制单日期 / 确认日期
表格列：制单日期、赔付单号、客户名称、商品编码、商品名称、规格、批次、
         处理方式、供应商、生产商、客户赔付金额、其他赔付金额、制单员
"""
import json
import pytest
import requests
from datetime import datetime, timedelta

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range

BASE = '/api/supplier-admin/supplier-admin/interior'





# ──────────────────────────────────────────────
#  推送状态数量汇总
# ──────────────────────────────────────────────

@pytest.mark.run(order=1)
def test_complaint_queryStatusCount(global_config):
    """物流客诉--查询推送状态数量汇总"""
    body = {"pageNo": 1, "pageSize": 10}
    try:
        jd = parse_json(post_api(global_config, BASE + '/complaint/queryLogisticsComplaintCount', body))
        assert_success(jd, '物流客诉-推送状态数量')
        data = jd.get('data') or []
        print(f'\n物流客诉推送状态汇总:')
        for item in data:
            print(f'  {item.get("orderStatusName")}：{item.get("total")} 条')
        # 校验返回状态枚举（待推送=0，推送成功=1）
        status_codes = [i.get('orderStatus') for i in data]
        assert 0 in status_codes or 1 in status_codes, '未返回预期推送状态枚举'
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ──────────────────────────────────────────────
#  查询列表
# ──────────────────────────────────────────────

@pytest.mark.run(order=2)
def test_complaint_queryAllPage(global_config):
    """物流客诉--查询全量列表（不带日期过滤）"""
    body = {"pageNo": 1, "pageSize": 10}
    try:
        jd = parse_json(post_api(global_config, BASE + '/complaint/queryPage', body))
        assert_success(jd, '物流客诉-全量列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n物流客诉总数: {total}')
        if records:
            r = records[0]
            print(f'  赔付单号：    {r.get("code")}')
            print(f'  客户名称：    {r.get("customerName")}')
            print(f'  商品编码：    {r.get("materialCode")}')
            print(f'  商品名称：    {r.get("materialName")}')
            print(f'  规格：        {r.get("materialSpec")}')
            print(f'  批次：        {r.get("batchNo")}')
            print(f'  处理方式：    {r.get("processMode")}')
            print(f'  供应商：      {r.get("supplierName")}')
            print(f'  生产商：      {r.get("producerName")}')
            print(f'  客户赔付金额：{r.get("complaintAmount")}')
            print(f'  其他赔付金额：{r.get("otherAmount")}')
            print(f'  制单员：      {r.get("createUser")}')
            print(f'  制单日期：    {r.get("createTime")}')
            print(f'  确认日期：    {r.get("complaintTime")}')
            print(f'  赔付状态：    {r.get("complaintStatus")}')
            print(f'  推送状态：    {r.get("pushStatusName")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=3)
def test_complaint_queryByCreateDate(global_config):
    """物流客诉--按制单日期范围查询"""
    start_d, end_d = day_range(365)
    body = {
        "pageNo": 1, "pageSize": 10,
        "createStartDate": start_d,
        "createEndDate": end_d
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/complaint/queryPage', body))
        assert_success(jd, '物流客诉-制单日期筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n物流客诉(近365天制单)总数: {total}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=4)
def test_complaint_queryByComplaintDate(global_config):
    """物流客诉--按确认日期范围查询"""
    start_d, end_d = day_range(365)
    body = {
        "pageNo": 1, "pageSize": 10,
        "complaintTimeStart": start_d,
        "complaintTimeEnd": end_d
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/complaint/queryPage', body))
        assert_success(jd, '物流客诉-确认日期筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n物流客诉(近365天确认)总数: {total}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=5)
def test_complaint_queryByCode(global_config):
    """物流客诉--按赔付单号精确查询"""
    # 先查一条记录取赔付单号
    r0 = post_api(global_config, BASE + '/complaint/queryPage', {"pageNo": 1, "pageSize": 1})
    records = (r0.json().get('data') or {}).get('list') or []
    if not records:
        pytest.skip('暂无物流客诉数据，跳过赔付单号精确查询')

    code = records[0].get('code')
    body = {"pageNo": 1, "pageSize": 10, "code": code}
    try:
        jd = parse_json(post_api(global_config, BASE + '/complaint/queryPage', body))
        assert_success(jd, '物流客诉-赔付单号精确查询')
        total = (jd.get('data') or {}).get('totalCount', 0)
        result_list = (jd.get('data') or {}).get('list') or []
        print(f'\n赔付单号[{code}]查询结果: {total} 条')
        if result_list:
            assert result_list[0].get('code') == code, '返回记录赔付单号不匹配'
            print(f'  核验通过：赔付单号 = {result_list[0].get("code")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=6)
def test_complaint_queryBySupplier(global_config):
    """物流客诉--按供应商筛选"""
    # 先查一条记录取供应商编码
    r0 = post_api(global_config, BASE + '/complaint/queryPage', {"pageNo": 1, "pageSize": 1})
    records = (r0.json().get('data') or {}).get('list') or []
    if not records:
        pytest.skip('暂无物流客诉数据，跳过供应商筛选')

    supplier_code = records[0].get('supplierCode')
    body = {"pageNo": 1, "pageSize": 10, "supplierCode": supplier_code}
    try:
        jd = parse_json(post_api(global_config, BASE + '/complaint/queryPage', body))
        assert_success(jd, '物流客诉-供应商筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n供应商[{supplier_code}]客诉总数: {total}')
        assert total >= 1, f'按供应商筛选应至少有1条记录'
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=7)
def test_complaint_queryByPushStatus_pending(global_config):
    """物流客诉--按推送状态筛选（待推送）"""
    body = {"pageNo": 1, "pageSize": 10, "orderStatus": 0}
    try:
        jd = parse_json(post_api(global_config, BASE + '/complaint/queryPage', body))
        assert_success(jd, '物流客诉-待推送筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n物流客诉(待推送)总数: {total}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=8)
def test_complaint_queryByPushStatus_success(global_config):
    """物流客诉--按推送状态筛选（推送成功）"""
    body = {"pageNo": 1, "pageSize": 10, "orderStatus": 1}
    try:
        jd = parse_json(post_api(global_config, BASE + '/complaint/queryPage', body))
        assert_success(jd, '物流客诉-推送成功筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n物流客诉(推送成功)总数: {total}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=9)
def test_complaint_pagination(global_config):
    """物流客诉--分页查询（第2页）"""
    body = {"pageNo": 2, "pageSize": 5}
    try:
        jd = parse_json(post_api(global_config, BASE + '/complaint/queryPage', body))
        assert_success(jd, '物流客诉-分页查询')
        data = jd.get('data') or {}
        total = data.get('totalCount', 0)
        curr_page = data.get('currPage', 1)
        page_size = data.get('pageSize', 5)
        print(f'\n物流客诉分页: 第{curr_page}页，每页{page_size}条，共{total}条')
        assert curr_page == 2
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
