# -*- coding: utf-8 -*-
"""quality 400客诉接口测试"""
import pytest

from utils.quality_helper import QUALITY_PREFIX, query_quality_list


@pytest.mark.quality
def test_quality_400ComplainList(global_config):
    """质量 - 查询 400 客诉列表"""
    query_quality_list(
        global_config,
        f'{QUALITY_PREFIX}/complain/400/list',
        {
            'workOrderDate': [],
            'problemTypeList': [],
            'productTypeList': [],
            'pageNo': 1,
            'pageSize': 10,
        },
        '400客诉列表',
        skip_if_empty=True,
    )
