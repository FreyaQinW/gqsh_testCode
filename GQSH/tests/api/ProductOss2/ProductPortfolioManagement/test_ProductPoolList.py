# -*- coding: utf-8 -*-
"""预产品池 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success


@pytest.mark.oms
def test_pageProductPoolList(global_config):
    """预产品池 - 分页查询产品池列表"""
    response = post_api(
        global_config,
        '/api/shop-admin/shop-admin//pool/pageProductPoolList',
        {
            "productName": "",
            "productPoolCode": "",
            "manageArea": "",
            "labelFlag": "",
            "launchFlag": "",
            "userClientScene": [],
            "timeScene": [],
            "scenePackage": [],
            "applicationScene": [],
            "scenePeopleNumber": [],
            "applicationConvenience": [],
            "pageNo": 1,
            "pageSize": 50
        },
    )
    json_data = parse_json(response, '产品池列表')
    assert_success(json_data, '产品池列表')
    print(f'产品池列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')



