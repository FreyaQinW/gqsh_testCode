# -*- coding: utf-8 -*-
"""OMS 辅助功能 API 接口测试"""
import pytest

from utils.api_helper import current_month_datetime_range, first_oss2_list_item, query_oss2_list

data_start_time, data_end_time = current_month_datetime_range()


@pytest.mark.oms
def test_auxiliaryFunctions_operationLog(global_config):
    """辅助功能 - 查询操作日志列表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/api/auxiliary/operationLog/page',
        {
            'startTime': data_start_time,
            'endTime': data_end_time,
            'operator': '',
            'module': '',
            'action': '',
            'page': 1,
            'limit': 10,
        },
        '操作日志列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_auxiliaryFunctions_exportTaskList(global_config):
    """辅助功能 - 查询导出任务列表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/api/auxiliary/exportTask/page',
        {
            'startTime': data_start_time,
            'endTime': data_end_time,
            'taskName': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '导出任务列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_auxiliaryFunctions_messageList(global_config):
    """辅助功能 - 查询系统消息列表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/api/auxiliary/message/page',
        {
            'startTime': data_start_time,
            'endTime': data_end_time,
            'messageType': '',
            'isRead': '',
            'page': 1,
            'limit': 10,
        },
        '系统消息列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_auxiliaryFunctions_list(global_config):
    """辅助功能 - 查询辅助功能列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/auxiliaryFunctions/page',
        {
            'page': 1,
            'limit': 10,
        },
        '辅助功能列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, '辅助功能列表')
    auxiliary_functions_no = first.get('auxiliaryFunctionsNo')
    global_config['auxiliaryFunctionsNo'] = auxiliary_functions_no
    print(f'辅助功能 auxiliaryFunctionsNo: {auxiliary_functions_no}')


@pytest.mark.oms
def test_auxiliaryFunctionsDetail(global_config):
    """辅助功能 - 辅助功能列表详情"""
    auxiliary_functions_no = global_config.get('auxiliaryFunctionsNo', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/auxiliaryFunctions/page',
        {
            'auxiliaryFunctionsNo': auxiliary_functions_no,
            'page': 1,
            'limit': 10,
        },
        '辅助功能详情',
        skip_if_empty=True,
    )
    print(f'辅助功能详情接口查询结果: {json_data}')
