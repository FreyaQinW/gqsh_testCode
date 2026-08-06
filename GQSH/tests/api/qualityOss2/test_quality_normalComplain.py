# -*- coding: utf-8 -*-
"""quality 普通客诉接口测试"""
import pytest

from utils.quality_helper import (
    QUALITY_PREFIX,
    assert_detail_id,
    first_item_id,
    post_quality_and_assert,
    query_quality_list,
)


@pytest.mark.quality
@pytest.mark.order(1)
def test_quality_normalComplainList(global_config):
    """普通客诉 - 查询普通客诉列表"""
    _, items = query_quality_list(
        global_config,
        f'{QUALITY_PREFIX}/normal/complain/list',
        {
            'pageNo': 1,
            'pageSize': 10,
            'dutyType': 2,
            'beginBizMonth': '',
            'endBizMonth': '',
            'statusList': [],
        },
        '普通客诉列表',
        skip_if_empty=True,
    )
    complain_id = first_item_id(items, 'id')
    if not complain_id:
        pytest.skip('普通客诉列表首条缺少 id')
    global_config['complainId'] = complain_id
    print(f'【普通客诉 ID】{complain_id}')


@pytest.mark.quality
@pytest.mark.order(2)
def test_quality_normalComplainDetail(global_config):
    """普通客诉 - 查询普通客诉详情"""
    complain_id = global_config.get('complainId')
    if not complain_id:
        _, items = query_quality_list(
            global_config,
            f'{QUALITY_PREFIX}/normal/complain/list',
            {
                'pageNo': 1,
                'pageSize': 10,
                'dutyType': 2,
                'beginBizMonth': '',
                'endBizMonth': '',
                'statusList': [],
            },
            '普通客诉列表',
            skip_if_empty=True,
        )
        complain_id = first_item_id(items, 'id')
        global_config['complainId'] = complain_id
    if not complain_id:
        pytest.skip('未获取到普通客诉 ID，跳过详情测试')

    json_data = post_quality_and_assert(
        global_config,
        f'{QUALITY_PREFIX}/normal/complain/detail',
        {'id': complain_id},
        '普通客诉详情',
    )
    assert_detail_id(json_data, complain_id, label='普通客诉详情')
