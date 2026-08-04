# -*- coding: utf-8 -*-
"""quality  典型客诉 接口测试"""
import json
from datetime import datetime

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty,current_month_datetime_range

sale_start_time, sale_end_time = current_month_datetime_range()
# 服务端要求 ISO 8601 格式: yyyy-MM-dd'T'HH:mm:ss.SSSZ
_iso_fmt = '%Y-%m-%dT%H:%M:%S.000+0800'
biz_start = datetime.strptime(sale_start_time, '%Y-%m-%d %H:%M:%S').strftime(_iso_fmt)
biz_end   = datetime.strptime(sale_end_time,   '%Y-%m-%d %H:%M:%S').strftime(_iso_fmt)


@pytest.mark.oms
def test_quality_typicalComplainList(global_config):
    """质量 - 查询典型客诉供应商责任列表"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/typical/complain/list',
        {
            "dutyType": 1,
            "beginBizDate": biz_start,
            "endBizDate": biz_end,
            "statusList": [],
            "pageNo": 1,
            "pageSize": 10
        }
    )
    json_data = parse_json(response, '典型客诉供应商责任列表')
    assert_success(json_data, '典型客诉供应商责任列表')
    print(f'典型客诉供应商责任列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '典型客诉供应商责任列表', skip_if_empty=True)


@pytest.mark.oms
def test_quality_typicalComplainList1(global_config):
    """质量 - 查询典型客诉物流责任列表"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/typical/complain/list',
        {
            "dutyType": 2,
            "beginBizDate": biz_start,
            "endBizDate": biz_end,
            "statusList": [],
            "pageNo": 1,
            "pageSize": 10
        }
    )
    json_data = parse_json(response, '典型客诉物流责任列表')
    assert_success(json_data, '典型客诉物流责任列表')
    print(f'典型客诉物流责任列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '典型客诉物流责任列表', skip_if_empty=True)



@pytest.mark.oms
def test_quality_typicalComplainList2(global_config):
    """质量 - 查询典型客诉锅圈责任列表"""
    response = post_api(    
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/typical/complain/list',
        {
            "dutyType": 3,
            "beginBizDate": biz_start,
            "endBizDate": biz_end,
            "statusList": [],
            "pageNo": 1,
            "pageSize": 10
        }
    )
    json_data = parse_json(response, '典型客诉锅圈责任列表')
    assert_success(json_data, '典型客诉锅圈责任列表')
    print(f'典型客诉锅圈责任列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '典型客诉锅圈责任列表', skip_if_empty=True)
