# -*- coding: utf-8 -*-
"""quality 质量事故接口测试"""
import pytest

from utils.quality_helper import (
    QUALITY_PREFIX,
    current_month_iso_range,
    first_item_id,
    post_quality_and_assert,
    query_quality_list,
)

_, month_end_iso = current_month_iso_range()


@pytest.mark.quality
@pytest.mark.order(1)
def test_quality_accidentListPendingPushdown(global_config):
    """质量 - 质量事故列表（待下推 status=1）"""
    _, items = query_quality_list(
        global_config,
        f'{QUALITY_PREFIX}/quality/accident/list',
        {
            'pageNo': 1,
            'pageSize': 10,
            'statusList': [1],
        },
        '质量事故列表(待下推)',
        skip_if_empty=True,
    )
    accident_id = first_item_id(items, 'id')
    if not accident_id:
        pytest.skip('质量事故列表首条缺少 id')
    global_config['accidentPushdownId'] = accident_id
    print(f'【质量事故待下推 ID】{accident_id}')


@pytest.mark.quality
@pytest.mark.order(2)
def test_quality_accidentPushdown(global_config):
    """质量 - 质量事故下推（会变更单据状态，请在测试环境执行）"""
    accident_id = global_config.get('accidentPushdownId')
    if not accident_id:
        pytest.skip('未获取到质量事故 ID，跳过下推测试')

    post_quality_and_assert(
        global_config,
        f'{QUALITY_PREFIX}/quality/accident/pushdown',
        {
            'id': accident_id,
            'setupUploadTime': month_end_iso,
        },
        '质量事故下推',
    )


@pytest.mark.quality
@pytest.mark.order(3)
def test_quality_accidentListPendingReview(global_config):
    """质量 - 质量事故列表（待审核 status=3）"""
    _, items = query_quality_list(
        global_config,
        f'{QUALITY_PREFIX}/quality/accident/list',
        {
            'pageNo': 1,
            'pageSize': 10,
            'statusList': [3],
        },
        '质量事故列表(待审核)',
        skip_if_empty=True,
    )
    accident_id = first_item_id(items, 'id')
    if not accident_id:
        pytest.skip('质量事故待审核列表首条缺少 id')
    global_config['accidentAuditId'] = accident_id
    print(f'【质量事故待审核 ID】{accident_id}')


@pytest.mark.quality
@pytest.mark.order(4)
def test_quality_accidentAudit(global_config):
    """质量 - 质量事故审核（会变更单据状态，请在测试环境执行）"""
    accident_id = global_config.get('accidentAuditId')
    if not accident_id:
        pytest.skip('未获取到质量事故 ID，跳过审核测试')

    post_quality_and_assert(
        global_config,
        f'{QUALITY_PREFIX}/quality/accident/audit',
        {'id': accident_id, 'isPassed': True},
        '质量事故审核',
    )
