# -*- coding: utf-8 -*-
"""quality  产品驳回 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty


@pytest.mark.oms
def test_product_rejectionList(global_config):
    """质量 - 产品驳回列表"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/product/rejection/list',
        {
            "decideResultList": [],
            "pageNo": 1,
            "pageSize": 10
        }
    )
    json_data = parse_json(response, '产品驳回列表')
    assert_success(json_data, '产品驳回列表')
    print(f'产品驳回列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '产品驳回列表', skip_if_empty=True)

    # 提取首条记录的 ID，保存为公共参数
    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    first_item = items[0]
    rejection_id = first_item.get('id')
    global_config['productRejectionId'] = rejection_id
    print(f'产品驳回 ID: {rejection_id}')
