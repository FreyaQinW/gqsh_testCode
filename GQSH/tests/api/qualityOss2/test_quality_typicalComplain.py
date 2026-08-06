# -*- coding: utf-8 -*-
"""quality 典型客诉接口测试"""
import pytest

from utils.quality_helper import QUALITY_PREFIX, current_month_iso_range, query_quality_list

biz_start, biz_end = current_month_iso_range()

_DUTY_CASES = [
    (1, '典型客诉供应商责任列表'),
    (2, '典型客诉物流责任列表'),
    (3, '典型客诉锅圈责任列表'),
]


@pytest.mark.quality
@pytest.mark.parametrize('duty_type,label', _DUTY_CASES, ids=['supplier', 'logistics', 'gq'])
def test_quality_typicalComplainList(global_config, duty_type, label):
    """质量 - 按责任类型查询典型客诉列表"""
    query_quality_list(
        global_config,
        f'{QUALITY_PREFIX}/typical/complain/list',
        {
            'dutyType': duty_type,
            'beginBizDate': biz_start,
            'endBizDate': biz_end,
            'statusList': [],
            'pageNo': 1,
            'pageSize': 10,
        },
        label,
        skip_if_empty=True,
    )
