# -*- coding: utf-8 -*-
"""OMS 数据导入 API 接口测试"""
# import pytest
#
# from utils.api_helper import current_month_datetime_range, query_oss2_list
#
# data_start_time, data_end_time = current_month_datetime_range()
#
#
# @pytest.mark.oms
# def test_dataImport_importTaskList(global_config):
#     """数据导入 - 查询导入任务列表"""
#     query_oss2_list(
#         global_config,
#         '/api/oms-admin/api/dataImport/task/page',
#         {
#             'startTime': data_start_time,
#             'endTime': data_end_time,
#             'taskName': '',
#             'importType': '',
#             'status': '',
#             'page': 1,
#             'limit': 10,
#         },
#         '数据导入任务列表',
#         skip_if_empty=True,
#     )
#
#
# @pytest.mark.oms
# def test_dataImport_importTemplateList(global_config):
#     """数据导入 - 查询导入模板列表"""
#     query_oss2_list(
#         global_config,
#         '/api/oms-admin/api/dataImport/template/page',
#         {
#             'templateName': '',
#             'templateType': '',
#             'page': 1,
#             'limit': 10,
#         },
#         '数据导入模板列表',
#         skip_if_empty=True,
#     )
#
#
# @pytest.mark.oms
# def test_dataImport_importRecordList(global_config):
#     """数据导入 - 查询导入记录列表"""
#     query_oss2_list(
#         global_config,
#         '/api/oms-admin/api/dataImport/record/page',
#         {
#             'startTime': data_start_time,
#             'endTime': data_end_time,
#             'importType': '',
#             'operator': '',
#             'status': '',
#             'page': 1,
#             'limit': 10,
#         },
#         '数据导入记录列表',
#         skip_if_empty=True,
#     )

import pytest
from utils.api_helper import first_oss2_list_item, query_oss2_list


@pytest.mark.oms
def test_dataImport_list(global_config):
    """数据导入 - 查询数据导入列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/dataImport/page',
        {
            'page': 1,
            'limit': 10,
        },
        '数据导入列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, '数据导入列表')
    data_import_no = first.get('dataImportNo')
    global_config['dataImportNo'] = data_import_no
    print(f'数据导入 dataImportNo: {data_import_no}')


@pytest.mark.oms
def test_dataImportDetail(global_config):
    """数据导入 - 数据导入列表详情"""
    data_import_no = global_config.get('dataImportNo', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/dataImport/page',
        {
            'dataImportNo': data_import_no,
            'page': 1,
            'limit': 10,
        },
        '数据导入详情',
        skip_if_empty=True,
    )
    print(f'数据导入详情接口查询结果: {json_data}')
