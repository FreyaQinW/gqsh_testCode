# *-*coding:utf-8 *-*
import json

import pytest
import requests

from utils.api_helper import assert_success, day_range, get_jindie_order_no, parse_json, post_api

BASE = '/api/supplier-admin/supplier-admin/supplier'


"发货管理--发货列表--查询列表"
@pytest.mark.run(order=110)
def test_deliveryOrderQueryPage(global_config):
    start_d, end_d = day_range(60)
    body = {
        "deliverTime": [start_d, end_d],
        "handTime": [],
        "pageNo": 1,
        "pageSize": 10,
        "supplierDeliveryEndDate": end_d,
        "supplierDeliveryStartDate": start_d,
        "expectedArriveTimeEnd": "",
        "expectedArriveTimeStart": "",
        "jindieWarehouseId": None
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/deliveryOrder/queryPage', body))
        assert_success(jd, '发货列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'发货列表总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"发货管理--发货列表--根据采购订单号查询发货记录"
@pytest.mark.run(order=120)
def test_deliveryOrderQueryByOrderNo(global_config):
    order_no = get_jindie_order_no(global_config)
    if not order_no:
        pytest.skip('未找到采购订单号，请与 test_supplierOrder.py 联合运行')
    start_d, end_d = day_range(60)
    body = {
        "deliverTime": [start_d, end_d],
        "handTime": [],
        "pageNo": 1,
        "pageSize": 10,
        "supplierDeliveryEndDate": end_d,
        "supplierDeliveryStartDate": start_d,
        "expectedArriveTimeEnd": "",
        "expectedArriveTimeStart": "",
        "jindieWarehouseId": None,
        "jindiePurchaseOrderNo": order_no
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/deliveryOrder/queryPage', body))
        assert_success(jd, '按订单号查询发货记录')
        records = (jd.get('data') or {}).get('list') or []
        if not records:
            pytest.skip(f'采购订单 {order_no} 暂无发货记录（请确认上一环 savedeliveryOrder 已成功）')
        record = records[0]
        delivery_no = record.get('deliveryNo') or record.get('deliveryOrderNo')
        ork_no = record.get('huadingStockInNo')
        appointment_no = record.get('appointmentNo')
        global_config['deliveryOrderNo'] = delivery_no
        print(f'\n采购订单编码：{order_no}')
        print(f'发货单号：    {delivery_no}')
        print(f'ORK单号：     {ork_no}')
        print(f'预约单号：    {appointment_no}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"发货管理--发货列表--查询金额汇总"
@pytest.mark.run(order=130)
def test_deliveryOrderSum(global_config):
    start_d, end_d = day_range(60)
    body = {
        "deliverTime": [start_d, end_d],
        "handTime": [],
        "pageNo": 1,
        "pageSize": 10,
        "supplierDeliveryEndDate": end_d,
        "supplierDeliveryStartDate": start_d,
        "expectedArriveTimeEnd": "",
        "expectedArriveTimeStart": "",
        "jindieWarehouseId": None
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/deliveryOrder/sumDeliveryOrder', body))
        assert_success(jd, '发货列表-金额汇总')
        print('发货金额汇总:', jd.get('data'))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
