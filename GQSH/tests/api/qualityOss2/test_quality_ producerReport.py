# -*- coding: utf-8 -*-
"""quality  厂家后补报告 接口测试"""
import json
from datetime import datetime

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty,current_month_datetime_range


@pytest.mark.oms
def test_quality_producerReportList(global_config):
    """质量 - 待审核的厂家后补报告"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/producer/report/list',
        {
            "pageNo":1,
            "pageSize":10,
            "statusList":[2]
        }
    )
    json_data = parse_json(response, '厂家后补报告列表')
    assert_success(json_data, '厂家后补报告列表')
    print(f'厂家后补报告列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '厂家后补报告列表', skip_if_empty=True)

    # 提取首条记录的 ID，传递给详情测试
    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    first_item = items[0]
    report_id = first_item.get('id')
    global_config['producerReportId'] = report_id
    print(f'厂家后补报告 ID: {report_id}')


@pytest.mark.oms
def test_quality_producerReportDetail(global_config):
    """质量 - 厂家后补报告详情"""
    report_id = global_config.get('producerReportId')
    if not report_id:
        pytest.skip('未获取到厂家后补报告 ID，跳过详情测试')

    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/producer/report/detail',
        {"id": report_id}
    )
    json_data = parse_json(response, '厂家后补报告详情')
    assert_success(json_data, '厂家后补报告详情')
    print(f'厂家后补报告详情 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')


@pytest.mark.oms
def test_quality_producerReportAudit(global_config):
    """质量 - 厂家后补报告审核"""
    report_id = global_config.get('producerReportId')
    if not report_id:
        pytest.skip('未获取到厂家后补报告 ID，跳过审核测试')

    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/producer/report/audit',
        {"id": report_id, "isPassed": True}
    )
    json_data = parse_json(response, '厂家后补报告审核')
    assert_success(json_data, '厂家后补报告审核')
    print(f'厂家后补报告审核 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
