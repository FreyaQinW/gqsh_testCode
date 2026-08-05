# -*- coding: utf-8 -*-
"""quality  质量事故 接口测试"""
import json
from datetime import datetime

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty, current_month_datetime_range

data_start_time, data_end_time = current_month_datetime_range()
# 服务端要求 ISO 8601 格式: yyyy-MM-dd'T'HH:mm:ss.SSSZ
_iso_fmt = '%Y-%m-%dT%H:%M:%S.000+0800'
pushdown_upload_time = datetime.strptime(data_end_time, '%Y-%m-%d %H:%M:%S').strftime(_iso_fmt)


@pytest.mark.oms
def test_accidentList(global_config):
    """质量 - 质量事故列表，待下推状态"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/quality/accident/list',
        {
            "pageNo": 1,
            "pageSize": 10,
            "statusList": [1]
        }
    )
    json_data = parse_json(response, '质量事故列表')
    assert_success(json_data, '质量事故列表')
    print(f'质量事故列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '质量事故列表', skip_if_empty=True)

    # 提取首条记录的 ID，保存为公共参数
    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    first_item = items[0]
    accident_id = first_item.get('id')
    global_config['accidentId'] = accident_id
    print(f'质量事故 ID: {accident_id}')


@pytest.mark.oms
def test_quality_accidentListPushdown(global_config):
    """质量 - 质量事故下推"""
    accident_id = global_config.get('accidentId')
    if not accident_id:
        pytest.skip('未获取到质量事故 ID，跳过下推测试')

    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/quality/accident/pushdown',
        {
            "id": accident_id,
            "setupUploadTime": pushdown_upload_time
        }
    )
    json_data = parse_json(response, '质量事故下推')
    assert_success(json_data, '质量事故下推')
    print(f'质量事故下推 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')



@pytest.mark.oms
def test_accidentPendingReview(global_config):
    """质量 - 质量事故列表，待审核状态"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/quality/accident/list',
        {
            "pageNo": 1,
            "pageSize": 10,
            "statusList": [3]
        }
    )
    json_data = parse_json(response, '质量事故列表')
    assert_success(json_data, '质量事故列表')
    print(f'质量事故列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '质量事故列表', skip_if_empty=True)

    # 提取首条记录的 ID，保存为公共参数
    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    first_item = items[0]
    accident_id = first_item.get('id')
    global_config['accidentId'] = accident_id
    print(f'质量事故 ID: {accident_id}')


@pytest.mark.oms
def test_accidentPendingReviewAudit(global_config):
    """质量 - 质量事故审核"""
    accident_id = global_config.get('accidentId')
    if not accident_id:
        pytest.skip('未获取到质量事故 ID，跳过审核测试')

    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/quality/accident/audit',
        {"id": accident_id, "isPassed": True}
    )
    json_data = parse_json(response, '质量事故审核')
    assert_success(json_data, '质量事故审核')
    print(f'质量事故审核 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')