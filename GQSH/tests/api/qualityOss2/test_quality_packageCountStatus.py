# -*- coding: utf-8 -*-
"""quality  包装计数状态 接口测试"""
import json

import pytest

from utils.api_helper import parse_json, post_api, assert_success, assert_list_not_empty


@pytest.mark.oms
def test_quality_packageCountStatusList(global_config):
    """质量 - 包装计数状态列表"""
    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/product/package/list',
        {
            "pageNo": 1,
            "pageSize": 10,
            "statusList": [1]
        }
    )
    json_data = parse_json(response, '包装计数状态列表')
    assert_success(json_data, '包装计数状态列表')
    print(f'包装计数状态列表 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
    assert_list_not_empty(json_data, '包装计数状态列表', skip_if_empty=True)

    # 提取首条记录的 productCode，保存为公共参数
    data = json_data.get('data', {})
    items = data.get('list') or data.get('records') or []
    first_item = items[0]
    product_code = first_item.get('productCode')
    producer_code = first_item.get('producerCode')
    global_config['packageProductCode'] = product_code
    global_config['packageProducerCode'] = producer_code
    print(f'包装计数状态 productCode: {product_code}, producerCode: {producer_code}')


@pytest.mark.oms
def test_quality_packageAdd(global_config):
    """质量 - 包装计数新增"""
    product_code = global_config.get('packageProductCode')
    if not product_code:
        pytest.skip('未获取到 productCode，跳过新增测试')

    response = post_api(
        global_config,
        '/api/gq-quality-scrm/gq-quality-scrm/product/package/add',
        {
            "producerCode": global_config.get('packageProducerCode'),
            "productCode": product_code,
            "fileList": [],
            "syncHuading": True,
            "cartonImg": [
                {
                    "fileName": "测试技能图谱.jpg",
                    "objectName": "20260805/测试技能图谱.jpg",
                    "fileUrl": "//guoquan-product-test.oss-cn-shanghai.aliyuncs.com/20260805/%E6%B5%8B%E8%AF%95%E6%8A%80%E8%83%BD%E5%9B%BE%E8%B0%B1.jpg?Expires=1785906254&OSSAccessKeyId=LTAI5t9i6b8LhKQS9kju4rr5&Signature=0cOzlWQjOAnQ%2FmTQhXUIin%2FZONQ%3D",
                    "fileSize": "",
                    "fileType": ""
                }
            ],
            "platemakingImg": [
                {
                    "fileName": "测试技能图谱.jpg",
                    "objectName": "20260805/测试技能图谱.jpg",
                    "fileUrl": "//guoquan-product-test.oss-cn-shanghai.aliyuncs.com/20260805/%E6%B5%8B%E8%AF%95%E6%8A%80%E8%83%BD%E5%9B%BE%E8%B0%B1.jpg?Expires=1785906249&OSSAccessKeyId=LTAI5t9i6b8LhKQS9kju4rr5&Signature=63vZenc0wVrtJ2NCdFIIaGSn8M0%3D",
                    "fileSize": "",
                    "fileType": ""
                }
            ],
            "platemakingImgVer": "GQ-BZ-2026-08-002-A2",
            "cartonImgVer": "GQ-WX-2026-08-002-A2",
            "cartonImgs": ["20260805/测试技能图谱.jpg"],
            "platemakingImgs": ["20260805/测试技能图谱.jpg"]
        }
    )
    json_data = parse_json(response, '包装计数新增')
    assert_success(json_data, '包装计数新增')
    print(f'包装计数新增 响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')
