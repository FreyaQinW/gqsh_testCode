# -*- coding: utf-8 -*-
"""quality 厂家后补报告接口测试"""
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
def test_quality_producerReportList(global_config):
    """质量 - 待审核的厂家后补报告列表"""
    _, items = query_quality_list(
        global_config,
        f'{QUALITY_PREFIX}/producer/report/list',
        {
            'pageNo': 1,
            'pageSize': 10,
            'statusList': [2],
        },
        '厂家后补报告列表',
        skip_if_empty=True,
    )
    report_id = first_item_id(items, 'id')
    if not report_id:
        pytest.skip('厂家后补报告列表首条缺少 id')
    global_config['producerReportId'] = report_id
    print(f'【厂家后补报告 ID】{report_id}')


@pytest.mark.quality
@pytest.mark.order(2)
def test_quality_producerReportDetail(global_config):
    """质量 - 厂家后补报告详情"""
    report_id = global_config.get('producerReportId')
    if not report_id:
        pytest.skip('未获取到厂家后补报告 ID，跳过详情测试')

    json_data = post_quality_and_assert(
        global_config,
        f'{QUALITY_PREFIX}/producer/report/detail',
        {'id': report_id},
        '厂家后补报告详情',
    )
    assert_detail_id(json_data, report_id, label='厂家后补报告详情')


@pytest.mark.quality
@pytest.mark.order(3)
def test_quality_producerReportAudit(global_config):
    """质量 - 厂家后补报告审核（会变更单据状态，请在测试环境执行）"""
    report_id = global_config.get('producerReportId')
    if not report_id:
        pytest.skip('未获取到厂家后补报告 ID，跳过审核测试')

    post_quality_and_assert(
        global_config,
        f'{QUALITY_PREFIX}/producer/report/audit',
        {'id': report_id, 'isPassed': True},
        '厂家后补报告审核',
    )
