# -*- coding: utf-8 -*-
"""OMS 调拨管理 API 接口测试"""
import pytest

from utils.api_helper import (
    current_month_datetime_range,
    first_oss2_list_item,
    pick_oss2_id,
    post_and_assert_oss2,
    query_oss2_list,
)

data_start_time, data_end_time = current_month_datetime_range()

_LIST_BODY = {
    'startTime': data_start_time,
    'endTime': data_end_time,
    'transferOrderNo': '',
    'fromWarehouseCode': '',
    'toWarehouseCode': '',
    'status': '',
    'page': 1,
    'limit': 10,
}


@pytest.mark.oms
def test_transferManagement_list(global_config):
    """调拨管理 - 查询调拨单列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/transferOrder/page',
        dict(_LIST_BODY),
        '调拨单列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, '调拨单列表')
    transfer_order_no = first.get('transferOrderNo')
    global_config['transferOrderNo'] = transfer_order_no
    print(f'调拨单 transferOrderNo: {transfer_order_no}')


@pytest.mark.oms
def test_transferOrderDetail(global_config):
    """调拨管理 - 调拨单列表详情"""
    transfer_order_no = global_config.get('transferOrderNo', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/transferOrder/page',
        {
            'transferOrderNo': transfer_order_no,
            'page': 1,
            'limit': 10,
        },
        '调拨单详情',
        skip_if_empty=True,
    )
    print(f'调拨单详情接口查询结果: {json_data}')


@pytest.mark.oms
def test_transferManagement_detail(global_config):
    """调拨管理 - 先查列表取单号，再查详情"""
    list_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/transferOrder/page',
        dict(_LIST_BODY),
        '调拨单列表',
        skip_if_empty=True,
    )
    item = first_oss2_list_item(list_data, '调拨单列表')
    id_key, id_value = pick_oss2_id(
        item, 'transferOrderNo', 'orderNo', 'id', 'transferNo'
    )
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/api/transferOrder/detail',
        {
            id_key: id_value,
            'startTime': data_start_time,
            'endTime': data_end_time,
        },
        '调拨单详情',
    )


@pytest.mark.oms
def test_transferManagement_inboundList(global_config):
    """调拨管理 - 查询调拨入库单列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/transferInbound/page',
        {
            'startTime': data_start_time,
            'endTime': data_end_time,
            'inboundOrderNo': '',
            'transferOrderNo': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '调拨入库单列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, '调拨入库单列表')
    inbound_order_no = first.get('inboundOrderNo')
    global_config['inboundOrderNo'] = inbound_order_no
    print(f'调拨入库单 inboundOrderNo: {inbound_order_no}')


@pytest.mark.oms
def test_transferInboundOrderDetail(global_config):
    """调拨管理 - 调拨入库单列表详情"""
    inbound_order_no = global_config.get('inboundOrderNo', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/transferInbound/page',
        {
            'inboundOrderNo': inbound_order_no,
            'page': 1,
            'limit': 10,
        },
        '调拨入库单详情',
        skip_if_empty=True,
    )
    print(f'调拨入库单详情接口查询结果: {json_data}')


@pytest.mark.oms
def test_transferManagement_outboundList(global_config):
    """调拨管理 - 查询调拨出库单列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/transferOutbound/page',
        {
            'startTime': data_start_time,
            'endTime': data_end_time,
            'outboundOrderNo': '',
            'transferOrderNo': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '调拨出库单列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, '调拨出库单列表')
    outbound_order_no = first.get('outboundOrderNo')
    global_config['outboundOrderNo'] = outbound_order_no
    print(f'调拨出库单 outboundOrderNo: {outbound_order_no}')


@pytest.mark.oms
def test_transferOutboundOrderDetail(global_config):
    """调拨管理 - 调拨出库单列表详情"""
    outbound_order_no = global_config.get('outboundOrderNo', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/transferOutbound/page',
        {
            'outboundOrderNo': outbound_order_no,
            'page': 1,
            'limit': 10,
        },
        '调拨出库单详情',
        skip_if_empty=True,
    )
    print(f'调拨出库单详情接口查询结果: {json_data}')
