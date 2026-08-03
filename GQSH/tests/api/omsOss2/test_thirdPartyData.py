# -*- coding: utf-8 -*-
"""OMS 三方数据 API 接口测试"""
import pytest

from utils.api_helper import (
    current_month_datetime_range,
    first_oms_list_item,
    pick_oms_id,
    post_and_assert_oms,
    query_oms_list,
)

data_start_time, data_end_time = current_month_datetime_range()

_SYNC_LIST_BODY = {
    'startTime': data_start_time,
    'endTime': data_end_time,
    'sourceType': '',
    'syncStatus': '',
    'page': 1,
    'limit': 10,
}


@pytest.mark.oms
def test_thirdPartyData_syncList(global_config):
    """三方数据 - 查询三方数据同步列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/thirdPartyData/syncList',
        dict(_SYNC_LIST_BODY),
        '三方数据同步列表',
        skip_if_empty=True,
    )
    first = first_oms_list_item(json_data, '三方数据同步列表')
    third_party_data_no = first.get('thirdPartyDataNo')
    global_config['thirdPartyDataNo'] = third_party_data_no
    print(f'三方数据 thirdPartyDataNo: {third_party_data_no}')


@pytest.mark.oms
def test_thirdPartyDataDetail(global_config):
    """三方数据 - 三方数据同步列表详情"""
    third_party_data_no = global_config.get('thirdPartyDataNo', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/thirdPartyData/syncList',
        {
            'thirdPartyDataNo': third_party_data_no,
            'page': 1,
            'limit': 10,
        },
        '三方数据同步详情',
        skip_if_empty=True,
    )
    print(f'三方数据同步详情接口查询结果: {json_data}')


@pytest.mark.oms
def test_thirdPartyData_syncDetail(global_config):
    """三方数据 - 先查同步列表取主键，再查详情"""
    list_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/thirdPartyData/syncList',
        dict(_SYNC_LIST_BODY),
        '三方数据同步列表',
        skip_if_empty=True,
    )
    item = first_oms_list_item(list_data, '三方数据同步列表')
    id_key, id_value = pick_oms_id(item, 'syncId', 'id', 'taskId', 'batchNo')
    post_and_assert_oms(
        global_config,
        '/api/oms-admin/api/thirdPartyData/syncDetail',
        {
            id_key: id_value,
            'startTime': data_start_time,
            'endTime': data_end_time,
        },
        '三方数据同步详情',
    )


@pytest.mark.oms
def test_thirdPartyData_channelList(global_config):
    """三方数据 - 查询渠道数据列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/thirdPartyData/channelList',
        {
            'channelCode': '',
            'channelName': '',
            'page': 1,
            'limit': 10,
        },
        '三方数据渠道列表',
        skip_if_empty=True,
    )
    first = first_oms_list_item(json_data, '三方数据渠道列表')
    channel_code = first.get('channelCode')
    global_config['channelCode'] = channel_code
    print(f'三方数据渠道 channelCode: {channel_code}')


@pytest.mark.oms
def test_channelDataDetail(global_config):
    """三方数据 - 渠道数据列表详情"""
    channel_code = global_config.get('channelCode', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/thirdPartyData/channelList',
        {
            'channelCode': channel_code,
            'page': 1,
            'limit': 10,
        },
        '三方数据渠道详情',
        skip_if_empty=True,
    )
    print(f'三方数据渠道详情接口查询结果: {json_data}')
