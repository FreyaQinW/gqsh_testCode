# -*- coding: utf-8 -*-
"""quality 产品驳回接口测试"""
import pytest

from utils.quality_helper import QUALITY_PREFIX, first_item_id, query_quality_list


@pytest.mark.quality
def test_quality_productRejectionList(global_config):
    """质量 - 产品驳回列表"""
    _, items = query_quality_list(
        global_config,
        f'{QUALITY_PREFIX}/product/rejection/list',
        {
            'decideResultList': [],
            'pageNo': 1,
            'pageSize': 10,
        },
        '产品驳回列表',
        skip_if_empty=True,
    )
    rejection_id = first_item_id(items, 'id')
    if rejection_id:
        global_config['productRejectionId'] = rejection_id
        print(f'【产品驳回 ID】{rejection_id}')
