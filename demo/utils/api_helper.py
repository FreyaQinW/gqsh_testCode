# *-*coding:utf-8 *-*
"""API 测试公共工具：请求封装、响应断言、日期范围生成"""
import calendar
import json
from datetime import datetime, timedelta

import pytest
import requests


def post_api(global_config, path, body, timeout=10):
    """发送 POST 请求，网络异常时直接 fail"""
    url = global_config['test_URL'] + path
    try:
        return requests.post(
            url=url,
            json=body,
            headers=global_config['header'],
            timeout=timeout,
            verify=True,
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f'网络请求失败: {e}')


def get_api(global_config, path, timeout=10):
    """发送 GET 请求，网络异常时直接 fail"""
    url = global_config['test_URL'] + path
    try:
        return requests.get(
            url=url,
            headers=global_config['header'],
            timeout=timeout,
            verify=True,
        )
    except requests.exceptions.RequestException as e:
        pytest.fail(f'网络请求失败: {e}')


def parse_json(response):
    """解析响应 JSON，失败时直接 fail"""
    try:
        return response.json()
    except json.JSONDecodeError as e:
        pytest.fail(f'JSON解析失败: {e}')


def assert_success(json_data, label, auth_code=401):
    """断言接口返回 success=True"""
    if json_data is None:
        pytest.fail('响应数据为空')
    if json_data.get('code') == auth_code:
        pytest.fail('请重新登录')
    if not json_data.get('success'):
        pytest.fail(f'{label}失败：{json_data.get("msg", "未知错误")}')


def assert_list_not_empty(json_data, label, *, skip_if_empty=False):
    """断言分页列表 totalCount > 0"""
    total_count = json_data.get('data', {}).get('totalCount', 0)
    if total_count == 0:
        if skip_if_empty:
            pytest.skip(f'{label}返回数据为空')
        pytest.fail(f'{label}查询结果为空')
    return total_count


def month_range():
    """近两个月，格式 YYYY-MM"""
    now = datetime.now()
    end_m = now.strftime('%Y-%m')
    y, m = now.year, now.month - 1
    if m < 1:
        y -= 1
        m = 12
    return f'{y}-{m:02d}', end_m


def year_range():
    """当前年度完整范围，格式 YYYY-MM"""
    y = datetime.now().year
    return f'{y}-01', f'{y}-12'


def day_range(days=33):
    """最近 N 天日期范围，格式 YYYY-MM-DD"""
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    return start, end


def three_months_ago_date():
    """三个月前的日期，格式 YYYY-MM-DD"""
    now = datetime.now()
    year = now.year
    month = now.month - 3
    if month < 1:
        year -= 1
        month += 12
    last_day = calendar.monthrange(year, month)[1]
    return datetime(year, month, min(last_day, now.day)).strftime('%Y-%m-%d')


def current_month_datetime_range():
    """当前月起止时间，格式 YYYY-MM-DD HH:MM:SS"""
    now = datetime.now()
    last_day = calendar.monthrange(now.year, now.month)[1]
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(day=last_day, hour=23, minute=59, second=59, microsecond=0)
    return start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S')


def assert_oms_success(json_data, label):
    """OMS 接口断言：token 失效时 code=400"""
    if json_data is None:
        pytest.fail(f'{label}接口返回数据为空，请检查接口是否正常')
    if json_data.get('code') == 400:
        pytest.fail('token过期或无效，请检查登录状态')
    if not json_data.get('success'):
        pytest.fail(f'{label}接口返回数据异常，请检查接口是否正常')


def query_oms_list(global_config, path, body, label):
    """OMS 分页列表：POST → 解析 → 断言 → 空列表 skip"""
    response = post_api(global_config, path, body)
    json_data = parse_json(response)
    print(f'{label}接口返回数据: {json_data}')
    assert_oms_success(json_data, label)
    assert_list_not_empty(json_data, label, skip_if_empty=True)


def purchase_order_search_params(bill_status_list):
    """供应商端采购订单查询参数（近三个月）"""
    current_date = datetime.now().strftime('%Y-%m-%d')
    three_months_ago = three_months_ago_date()
    return {
        'orgId': None,
        'releaseTime': [three_months_ago, current_date],
        'pageNo': 1,
        'pageSize': 10,
        'purchaseEndTime': current_date,
        'purchaseStartTime': three_months_ago,
        'deliveryEndTime': '',
        'deliveryStartTime': '',
        'warehouseCode': None,
        'billStatusList': bill_status_list,
    }


def post_and_assert(global_config, path, body, label):
    """POST → 解析 → 断言 success"""
    response = post_api(global_config, path, body)
    json_data = parse_json(response)
    assert_success(json_data, label)
    return json_data


def post_json(global_config, path, body, timeout=10):
    """POST 并返回解析后的 JSON"""
    return parse_json(post_api(global_config, path, body, timeout=timeout))


def assert_auth_ok(json_data):
    """断言响应非空且未鉴权失败"""
    if json_data is None:
        pytest.fail('响应数据为空')
    if json_data.get('code') == 401:
        pytest.fail('请重新登录')


def assert_failure(json_data, label):
    """断言接口返回 success=False"""
    assert_auth_ok(json_data)
    if json_data.get('success'):
        pytest.fail(f'{label}不应成功')


def extract_jindie_order_no(json_data):
    """从采购订单分页结果提取金蝶订单号"""
    assert_list_not_empty(json_data, '采购订单')
    order_no = json_data.get('data', {}).get('list', [{}])[0].get('jindiePurchaseOrderNo')
    if not order_no:
        pytest.fail('请重新查询采购订单编码')
    return order_no


def format_time_hm(time_value):
    """将时间值格式化为 HH:MM"""
    time_str = str(time_value)
    for time_format in ('%H:%M:%S', '%H:%M'):
        try:
            return datetime.strptime(time_str, time_format).strftime('%H:%M')
        except ValueError:
            continue
    return time_str[:5]
