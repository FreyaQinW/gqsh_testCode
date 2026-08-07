# -*- coding: utf-8 -*-
"""quality  400客诉 接口测试"""
import json
from datetime import datetime

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty,current_month_datetime_range


@pytest.mark.oms
def test_quality_typicalComplainList400(global_config):
    """质量 - 查询400客诉列表"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/complain/400/list',
        {
            "workOrderDate":[],
            "problemTypeList":[],
            "productTypeList":[],
            "pageNo":1,
            "pageSize":10
        }
    )
    json_data = parse_json(response, '400客诉列表')
    assert_success(json_data, '400客诉列表')
    print(f'400客诉列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '400客诉列表', skip_if_empty=True)


