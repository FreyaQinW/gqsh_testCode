# -*- coding: utf-8 -*-
"""OMS 数据看板 API 接口测试"""
import pytest

from utils.api_helper import current_month_datetime_range, first_oms_list_item, post_and_assert_oms, query_oms_list

data_start_time, data_end_time = current_month_datetime_range()


@pytest.mark.oms
def test_dataDashboard_overview(global_config):
    """数据看板 - 查询概览统计数据"""
    post_and_assert_oms(
        global_config,
        '/api/oms-admin/api.order/statistic/day',
        {
            "type":None,
            "pieDateBegin":data_start_time,
            "pieDateEnd":data_end_time,
            "dateType":1,
            "lineDateBegin":data_start_time,
            "lineDateEnd":data_end_time
        },
        '数据看板概览统计',
    )


@pytest.mark.oms
def test_dataDashboard_list(global_config):
    """数据看板 - 查询数据看板列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/dataDashboard/page',
        {
            'startTime': data_start_time,
            'endTime': data_end_time,
            'page': 1,
            'limit': 10,
        },
        '数据看板列表',
        skip_if_empty=True,
    )
    first = first_oms_list_item(json_data, '数据看板列表')
    data_dashboard_no = first.get('dataDashboardNo')
    global_config['dataDashboardNo'] = data_dashboard_no
    print(f'数据看板 dataDashboardNo: {data_dashboard_no}')


@pytest.mark.oms
def test_dataDashboardDetail(global_config):
    """数据看板 - 数据看板列表详情"""
    data_dashboard_no = global_config.get('dataDashboardNo', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/dataDashboard/page',
        {
            'dataDashboardNo': data_dashboard_no,
            'page': 1,
            'limit': 10,
        },
        '数据看板详情',
        skip_if_empty=True,
    )
    print(f'数据看板详情接口查询结果: {json_data}')
