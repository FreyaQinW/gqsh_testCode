# -*- coding: utf-8 -*-
"""quality 包装计数状态接口测试"""
import os

import pytest

from utils.quality_helper import (
    QUALITY_PREFIX,
    post_quality_and_assert,
    query_quality_list,
)


@pytest.mark.quality
@pytest.mark.order(1)
def test_quality_packageCountStatusList(global_config):
    """质量 - 包装计数状态列表"""
    _, items = query_quality_list(
        global_config,
        f'{QUALITY_PREFIX}/product/package/list',
        {
            'pageNo': 1,
            'pageSize': 10,
            'statusList': [1],
        },
        '包装计数状态列表',
        skip_if_empty=True,
    )
    first = items[0]
    product_code = first.get('productCode')
    producer_code = first.get('producerCode')
    if not product_code:
        pytest.skip('包装计数列表首条缺少 productCode')
    global_config['packageProductCode'] = product_code
    global_config['packageProducerCode'] = producer_code
    print(f'【包装计数】productCode={product_code}, producerCode={producer_code}')


@pytest.mark.quality
@pytest.mark.order(2)
def test_quality_packageAdd(global_config):
    """质量 - 包装计数新增（需环境变量提供无凭证的对象名，默认 skip）"""
    product_code = global_config.get('packageProductCode')
    producer_code = global_config.get('packageProducerCode')
    if not product_code:
        pytest.skip('未获取到 productCode，跳过新增测试')

    # 避免仓库内硬编码 OSS AccessKey/Signature；由 CI/本地环境注入对象名
    carton_object = os.getenv('QUALITY_PACKAGE_CARTON_OBJECT', '').strip()
    plate_object = os.getenv('QUALITY_PACKAGE_PLATE_OBJECT', '').strip()
    if not carton_object or not plate_object:
        pytest.skip(
            '未配置 QUALITY_PACKAGE_CARTON_OBJECT / QUALITY_PACKAGE_PLATE_OBJECT，'
            '跳过包装计数新增（勿在代码中提交带 AccessKey 的签名 URL）'
        )

    post_quality_and_assert(
        global_config,
        f'{QUALITY_PREFIX}/product/package/add',
        {
            'producerCode': producer_code,
            'productCode': product_code,
            'fileList': [],
            'syncHuading': True,
            'cartonImg': [
                {
                    'fileName': carton_object.split('/')[-1],
                    'objectName': carton_object,
                    'fileUrl': '',
                    'fileSize': '',
                    'fileType': '',
                }
            ],
            'platemakingImg': [
                {
                    'fileName': plate_object.split('/')[-1],
                    'objectName': plate_object,
                    'fileUrl': '',
                    'fileSize': '',
                    'fileType': '',
                }
            ],
            'platemakingImgVer': os.getenv('QUALITY_PACKAGE_PLATE_VER', 'GQ-BZ-AUTO-TEST'),
            'cartonImgVer': os.getenv('QUALITY_PACKAGE_CARTON_VER', 'GQ-WX-AUTO-TEST'),
            'cartonImgs': [carton_object],
            'platemakingImgs': [plate_object],
        },
        '包装计数新增',
    )
