# -*- coding: utf-8 -*-
"""quality  普通客诉 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty


@pytest.mark.oms
def test_quality_normalComplainList(global_config):
    """普通客诉 - 查询普通客诉列表"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/normal/complain/list',
        {
            "pageNo": 1,
            "pageSize": 10,
            "dutyType": 2,
            "beginBizMonth": "",
            "endBizMonth": "",
            "statusList": []
        },
    )
    json_data = parse_json(response, '普通客诉列表 ')
    assert_success(json_data, '普通客诉列表')
    print(f'普通客诉列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '普通客诉列表', skip_if_empty=True)

    # 提取首条记录的 ID，传递给详情测试
    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    first_item = items[0]
    complain_id = first_item.get('id')
    global_config['complainId'] = complain_id
    print(f'普通客诉 ID: {complain_id}')


@pytest.mark.oms
def test_quality_normalComplainDetail(global_config):
    """普通客诉 - 查询普通客诉详情"""
    complain_id = global_config.get('complainId')
    if not complain_id:
        pytest.skip('未获取到普通客诉 ID，跳过详情测试')

    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/normal/complain/detail',
        {"id": complain_id},
    )
    json_data = parse_json(response, '普通客诉详情 ')
    assert_success(json_data, '普通客诉详情')
    print(f'普通客诉详情 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
