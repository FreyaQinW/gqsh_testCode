# -*- coding: utf-8 -*-
"""质量 SCRM（gq-quality-scrm）接口测试公共工具"""
import json
from datetime import datetime

import pytest

from utils.api_helper import assert_success, current_month_datetime_range, parse_json, post_api

QUALITY_PREFIX = '/api/gq-quality-scrm/gq-quality-scrm'


def to_iso8601_cn(dt_str):
    """YYYY-MM-DD HH:MM:SS → yyyy-MM-dd'T'HH:mm:ss.SSSZ(+0800)"""
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S').strftime(
        '%Y-%m-%dT%H:%M:%S.000+0800'
    )


def current_month_iso_range():
    start, end = current_month_datetime_range()
    return to_iso8601_cn(start), to_iso8601_cn(end)


def quality_list_items(json_data):
    """兼容 data.list / data.records"""
    data = json_data.get('data') or {}
    items = data.get('list')
    if items is None:
        items = data.get('records')
    return items if isinstance(items, list) else []


def quality_total(json_data):
    """兼容 totalCount / total / 列表长度"""
    data = json_data.get('data') or {}
    if data.get('totalCount') not in (None, ''):
        return int(data.get('totalCount') or 0)
    if data.get('total') not in (None, ''):
        return int(data.get('total') or 0)
    return len(quality_list_items(json_data))


def query_quality_list(global_config, path, body, label, *, skip_if_empty=True):
    """质量分页列表：POST → 断言 → 返回 (json_data, items)。"""
    response = post_api(global_config, path, body)
    json_data = parse_json(response, f'{label} ')
    assert_success(json_data, label)
    items = quality_list_items(json_data)
    total = quality_total(json_data)
    print(f'{label}: total={total}, pageSize={len(items)}')
    if total == 0 or not items:
        if skip_if_empty:
            pytest.skip(f'{label}返回数据为空')
        pytest.fail(f'{label}查询结果为空')
    return json_data, items


def post_quality_and_assert(global_config, path, body, label):
    """质量非列表接口：POST → 断言 success，返回 json。"""
    response = post_api(global_config, path, body)
    json_data = parse_json(response, f'{label} ')
    assert_success(json_data, label)
    print(f'{label} 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    return json_data


def first_item_id(items, *candidate_keys):
    """从首条记录提取业务主键。"""
    if not items:
        return None
    first = items[0]
    for key in candidate_keys:
        value = first.get(key)
        if value not in (None, ''):
            return value
    return None


def assert_detail_id(json_data, expected_id, *, id_key='id', label='详情'):
    """断言详情响应中的业务 ID 与请求一致。"""
    data = json_data.get('data')
    if isinstance(data, dict):
        actual = data.get(id_key)
        if actual is None and isinstance(data.get('detail'), dict):
            actual = data['detail'].get(id_key)
    else:
        actual = None
    if actual is not None and str(actual) != str(expected_id):
        pytest.fail(f'{label}ID 不匹配，期望={expected_id}，实际={actual}')
