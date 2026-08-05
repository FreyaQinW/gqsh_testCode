# -*- coding: utf-8 -*-
"""quality  产品标准管理 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty


@pytest.mark.oms
def test_quality_productStandardsList(global_config):
    """质量 - 产品标准管理列表"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/product/standards/list',
        {
            "pageNo": 1,
            "pageSize": 10,
            "statusList": [1]
        }
    )
    json_data = parse_json(response, '产品标准列表')
    assert_success(json_data, '产品标准列表')
    print(f'产品标准列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '产品标准列表', skip_if_empty=True)

    # 提取首条记录的 ID，保存为公共参数
    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    first_item = items[0]
    standard_id = first_item.get('id')
    global_config['productStandardId'] = standard_id
    print(f'产品标准 ID: {standard_id}')


@pytest.mark.oms
def test_quality_productStandardsEdit(global_config):
    """质量 - 产品标准编辑"""
    standard_id = global_config.get('productStandardId')
    if not standard_id:
        pytest.skip('未获取到产品标准 ID，跳过编辑测试')

    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/product/standards/edit',
        {
            "id": standard_id,
            "standardsList": [
                {
                    "type": 1,
                    "name": "产品标准",
                    "syncHuading": True,
                    "files": [
                        {
                            "name": "统一社会信用代码.jpeg",
                            "key": "20260722/统一社会信用代码.jpeg",
                            "url": "https://guoquan-product-test.oss-cn-shanghai.aliyuncs.com/20260722/%E7%BB%9F%E4%B8%80%E7%A4%BE%E4%BC%9A%E4%BF%A1%E7%94%A8%E4%BB%A3%E7%A0%81.jpeg?Expires=1785845385&OSSAccessKeyId=LTAI5t9i6b8LhKQS9kju4rr5&Signature=yEfxbAjSyhI5JjNvzyYTVUYoI7c%3D"
                        }
                    ]
                },
                {
                    "type": 2,
                    "name": "工艺标准",
                    "syncHuading": True,
                    "files": []
                },
                {
                    "type": 3,
                    "name": "原料标准",
                    "syncHuading": True,
                    "files": [
                        {
                            "name": "IMG_1991.jpg",
                            "key": "20260722/IMG_1991.jpg",
                            "url": "https://guoquan-product-test.oss-cn-shanghai.aliyuncs.com/20260722/IMG_1991.jpg?Expires=1785845385&OSSAccessKeyId=LTAI5t9i6b8LhKQS9kju4rr5&Signature=7rv9yfzL2zomVTOx8Do0YlvSBNg%3D"
                        }
                    ]
                }
            ]
        }
    )
    json_data = parse_json(response, '产品标准编辑')
    assert_success(json_data, '产品标准编辑')
    print(f'产品标准编辑 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
