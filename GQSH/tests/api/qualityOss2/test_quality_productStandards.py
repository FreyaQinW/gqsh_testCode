# -*- coding: utf-8 -*-
"""quality 产品标准管理接口测试"""
import pytest

from utils.quality_helper import (
    QUALITY_PREFIX,
    first_item_id,
    post_quality_and_assert,
    query_quality_list,
)


@pytest.mark.quality
@pytest.mark.order(1)
def test_quality_productStandardsList(global_config):
    """质量 - 产品标准管理列表"""
    _, items = query_quality_list(
        global_config,
        f'{QUALITY_PREFIX}/product/standards/list',
        {
            'pageNo': 1,
            'pageSize': 10,
            'statusList': [1],
        },
        '产品标准列表',
        skip_if_empty=True,
    )
    standard_id = first_item_id(items, 'id')
    if not standard_id:
        pytest.skip('产品标准列表首条缺少 id')
    global_config['productStandardId'] = standard_id
    print(f'【产品标准 ID】{standard_id}')


@pytest.mark.quality
@pytest.mark.order(2)
def test_quality_productStandardsEdit(global_config):
    """质量 - 产品标准编辑（不上传签名文件，避免硬编码 OSS 凭证）"""
    standard_id = global_config.get('productStandardId')
    if not standard_id:
        _, items = query_quality_list(
            global_config,
            f'{QUALITY_PREFIX}/product/standards/list',
            {'pageNo': 1, 'pageSize': 10, 'statusList': [1]},
            '产品标准列表',
            skip_if_empty=True,
        )
        standard_id = first_item_id(items, 'id')
        global_config['productStandardId'] = standard_id
    if not standard_id:
        pytest.skip('未获取到产品标准 ID，跳过编辑测试')

    post_quality_and_assert(
        global_config,
        f'{QUALITY_PREFIX}/product/standards/edit',
        {
            'id': standard_id,
            'standardsList': [
                {'type': 1, 'name': '产品标准', 'syncHuading': False, 'files': []},
                {'type': 2, 'name': '工艺标准', 'syncHuading': False, 'files': []},
                {'type': 3, 'name': '原料标准', 'syncHuading': False, 'files': []},
            ],
        },
        '产品标准编辑',
    )
