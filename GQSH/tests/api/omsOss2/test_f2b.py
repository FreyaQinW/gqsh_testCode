# -*- coding: utf-8 -*-
"""OMS F2B API 接口测试"""
import json

import pytest

from utils.api_helper import first_oss2_list_item, query_oss2_list


@pytest.mark.oms
@pytest.mark.order(1)
def test_f2b_Order(global_config):
    """F2B - 订单列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/f2bOrder/page',
        {
            'orderCreateTimeBegin': '',
            'orderCreateTimeEnd': '',
            'omsOrderNo': '',
            'thirdOrderNo': '',
            'type': 9,
            'bizType': '',
            'status': 9,
            'submitMode': 9,
            'page': 1,
            'limit': 10,
        },
        'f2b 订单列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, 'f2b 订单列表')
    oms_order_no = first.get('omsOrderNo')
    global_config['omsOrderNo'] = oms_order_no
    print(f'【F2B订单编码】{oms_order_no}')


@pytest.mark.oms
@pytest.mark.order(2)
def test_f2b_orderDetail(global_config):
    """F2B - 按 omsOrderNo 查询订单详情并校验关键字段"""
    oms_order_no = global_config.get('omsOrderNo') or ''
    if not oms_order_no:
        list_data = query_oss2_list(
            global_config,
            '/api/oms-admin/api/f2bOrder/page',
            {
                'orderCreateTimeBegin': '',
                'orderCreateTimeEnd': '',
                'omsOrderNo': '',
                'thirdOrderNo': '',
                'type': 9,
                'bizType': '',
                'status': 9,
                'submitMode': 9,
                'page': 1,
                'limit': 10,
            },
            'f2b 订单列表',
            skip_if_empty=True,
        )
        oms_order_no = first_oss2_list_item(list_data, 'f2b 订单列表').get('omsOrderNo')
        global_config['omsOrderNo'] = oms_order_no

    if not oms_order_no:
        pytest.skip('无可用 omsOrderNo，跳过订单详情')

    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/f2bOrder/page',
        {
            'orderCreateTimeBegin': '',
            'orderCreateTimeEnd': '',
            'omsOrderNo': oms_order_no,
            'thirdOrderNo': '',
            'type': 9,
            'bizType': '',
            'status': 9,
            'submitMode': 9,
            'page': 1,
            'limit': 10,
        },
        'f2b 订单详情',
        skip_if_empty=False,
    )
    print(f'f2b 订单详情完整响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    detail = first_oss2_list_item(json_data, 'f2b 订单详情', skip_if_empty=False)
    required_fields = (
        'omsOrderNo',
        'thirdOrderNo',
        'orderAmount',
        'type',
        'bizType',
        'status',
        'source',
        'pushStatus',
        'submitMode',
        'deliveryCo',
        'deliveryDepot',
        'payType',
        'orderCreateTime',
        'payTime',
        'cargoOrgNo',
        'cargoOrgName',
    )
    missing = [f for f in required_fields if f not in detail]
    if missing:
        pytest.fail(f'订单详情缺少字段: {missing}')

    if detail.get('omsOrderNo') != oms_order_no:
        pytest.fail(
            f'订单号不匹配，期望={oms_order_no}，实际={detail.get("omsOrderNo")}'
        )

    print(
        '【订单详情】\n'
        f'  omsOrderNo:      {detail.get("omsOrderNo")}\n'
        f'  thirdOrderNo:    {detail.get("thirdOrderNo")}\n'
        f'  orderAmount:     {detail.get("orderAmount")}\n'
        f'  type/bizType:    {detail.get("type")}/{detail.get("bizType")}\n'
        f'  status:          {detail.get("status")}\n'
        f'  source:          {detail.get("source")}\n'
        f'  pushStatus:      {detail.get("pushStatus")}\n'
        f'  submitMode:      {detail.get("submitMode")}\n'
        f'  deliveryCo:      {detail.get("deliveryCo")}\n'
        f'  deliveryDepot:   {detail.get("deliveryDepot")}\n'
        f'  payType:         {detail.get("payType")}\n'
        f'  orderCreateTime: {detail.get("orderCreateTime")}\n'
        f'  payTime:         {detail.get("payTime")}\n'
        f'  cargoOrgNo:      {detail.get("cargoOrgNo")}\n'
        f'  cargoOrgName:    {detail.get("cargoOrgName")}\n'
        f'  cancelStatus:    {detail.get("cancelStatus")}\n'
        f'  push:            {detail.get("push")}\n'
        f'  memo:            {detail.get("memo")}\n'
        f'  jinDieOrderNos:  {detail.get("jinDieOrderNos")}\n'
        f'  jinDieDeliveryNos: {detail.get("jinDieDeliveryNos")}'
    )


@pytest.mark.oms
@pytest.mark.order(3)
def test_f2b_deliveryList(global_config):
    """F2B - 查询 F2B 发货单列表"""
    oms_order_no = global_config.get('omsOrderNo', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/f2bDelivery/page',
        {
            'beginDate': '',
            'endDate': '',
            'deliveryNo': '',
            'omsOrderNo': oms_order_no,
            'pushStatus': 9,
            'tagNo': '',
            'page': 1,
            'limit': 10,
        },
        'F2B发货列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, 'F2B发货列表')
    delivery_no = first.get('deliveryNo')
    global_config['deliveryNo'] = delivery_no
    print(f'F2B发货单 deliveryNo: {delivery_no}')


@pytest.mark.oms
@pytest.mark.order(4)
def test_f2bDeliveryDetail(global_config):
    """F2B - 发货单列表详情"""
    delivery_no = global_config.get('deliveryNo', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/f2bDelivery/page',
        {
            'deliveryNo': delivery_no,
            'page': 1,
            'limit': 10,
        },
        'F2B发货单详情',
        skip_if_empty=True,
    )
    print(f'F2B发货单详情接口查询结果: {json_data}')
