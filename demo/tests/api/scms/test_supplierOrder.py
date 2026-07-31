# *-*coding:utf-8 *-*
from datetime import datetime, timedelta

import pytest

from utils.api_helper import (
    format_time_hm,
    post_and_assert,
    purchase_order_search_params,
    extract_jindie_order_no,
)

PURCHASE_ORDER_API = (
    '/api/supplier-admin/supplier-admin/supplier/purchase/order/queryPagePurchaseOrder'
)
CONFIRM_ORDER_API = (
    '/api/supplier-admin/supplier-admin/supplier/purchase/order/savePurchaseOrderConfirmDetail'
)
MATERIAL_INFO_API = (
    '/api/supplier-admin/supplier-admin/supplier/deliveryOrder/mergeDelivery/selectMaterialInfo'
)
WAREHOUSE_CAPACITY_API = (
    '/api/supplier-admin/supplier-admin/supplier/deliveryOrder/listWarehouseTransportCapacity'
)
DELIVERY_SAVE_API = (
    '/api/supplier-admin/supplier-admin/supplier/deliveryOrder/mergeDelivery/save'
)


def _search_and_save_order_no(global_config, bill_status, label):
    """查询采购订单并保存金蝶订单号到 global_config"""
    params = purchase_order_search_params(bill_status)
    json_data = post_and_assert(global_config, PURCHASE_ORDER_API, params, label)
    print('请求参数', params)
    print('响应数据', json_data)
    order_no = extract_jindie_order_no(json_data)
    global_config['JINDIE_PURCHASE_ORDER_NO'] = order_no
    print('采购订单编码为', order_no)
    return order_no


@pytest.mark.run(order=1)
def test_orderSearch(global_config):
    """供应商端--查询采购订单，查询待确认的采购订单"""
    _search_and_save_order_no(global_config, [10], '待确认采购订单查询')


@pytest.mark.run(order=2)
def test_OrderConfirmDetail(global_config):
    """供应商端--采购订单确认"""
    post_and_assert(
        global_config,
        CONFIRM_ORDER_API,
        {
            'confirmDesc': '',
            'jindiePurchaseOrderNo': global_config['JINDIE_PURCHASE_ORDER_NO'],
        },
        '采购订单确认',
    )


@pytest.mark.run(order=3)
def test_orderStatusSearch(global_config):
    """供应商端--查询采购订单，查询待发货的采购订单"""
    _search_and_save_order_no(global_config, [20], '待发货采购订单查询')


@pytest.mark.run(order=4)
def test_selectMaterialInfo(global_config):
    """查询当前订单是否有库存"""
    json_data = post_and_assert(
        global_config,
        MATERIAL_INFO_API,
        {'jindiePurchaseOrderNos': [global_config['JINDIE_PURCHASE_ORDER_NO']]},
        '库存查询',
    )

    if not json_data.get('data'):
        pytest.fail('响应数据中缺少 data 字段')

    item = json_data['data'][0]
    batch = item.get('batchNoResVos', [{}])[0]
    inventory_num = batch.get('inventoryNum')

    global_config['batchNo'] = batch.get('batchNo')
    global_config['inventoryBatchCode'] = batch.get('inventoryBatchCode')
    global_config['inventoryNum'] = inventory_num
    global_config['materialCode'] = item.get('materialCode')
    global_config['materialName'] = item.get('materialName')
    global_config['materialSpec'] = item.get('materialSpec')
    global_config['purchaseOrderDetailCode'] = item.get('purchaseOrderDetailCode')

    if inventory_num is None:
        pytest.fail('请重新查询当前供应商的库存信息')
    if isinstance(inventory_num, str) and not inventory_num.strip():
        pytest.fail('库存数量为空')
    if isinstance(inventory_num, (int, float)) and inventory_num <= 0:
        pytest.fail(f'库存数量不足：{inventory_num}')

    print(
        '库存日期、编码、数量为',
        global_config['batchNo'],
        global_config['inventoryBatchCode'],
        global_config['inventoryNum'],
    )


@pytest.mark.run(order=5)
def test_WarehouseTransportCapacity(global_config):
    """查询华鼎仓储数量"""
    json_data = post_and_assert(
        global_config,
        WAREHOUSE_CAPACITY_API,
        {'houseCode': 'CK005'},
        '华鼎仓储运能查询',
    )

    if not json_data.get('data'):
        pytest.fail('响应数据中缺少 data 字段')

    record = json_data['data'][0]
    appoint_date = datetime.strptime(record['appointDate'], '%Y-%m-%d').strftime('%Y-%m-%d')
    detail_list = record['detailResList']
    start_time = detail_list[1]['startTime']
    end_time = detail_list[1]['endTime']
    capacity = detail_list[2]['capacity']

    global_config['appointDate'] = appoint_date
    global_config['startTime'] = start_time
    global_config['endTime'] = end_time
    global_config['capacity'] = capacity
    global_config['capacityRemained'] = detail_list[3]['capacityRemained']

    if not appoint_date.strip():
        pytest.fail('华鼎仓库无预约时间')
    if isinstance(capacity, (int, float)) and capacity <= 0:
        pytest.fail(f'华鼎仓储运能数量不足：{capacity}')

    print('华鼎仓储时间段为', start_time, end_time)
    print('华鼎仓储日期为', appoint_date)
    print('华鼎仓储库存数量为', capacity)


@pytest.mark.run(order=6)
def test_savedeliveryOrder(global_config):
    """供应商端--采购订单发货"""
    if not global_config.get('appointDate'):
        pytest.fail(f'缺少 appointDate 参数，当前值：{global_config.get("appointDate")}')
    if not global_config.get('startTime'):
        pytest.fail('缺少 startTime 参数，请先执行 test_WarehouseTransportCapacity')
    if not global_config.get('endTime'):
        pytest.fail(f'缺少 endTime 参数，当前值：{global_config.get("endTime")}')

    start_time_formatted = format_time_hm(global_config['startTime'])
    end_time_formatted = format_time_hm(global_config['endTime'])
    plan_arrival_time = f'{start_time_formatted}-{end_time_formatted}'

    appoint_date_str = str(global_config['appointDate'])
    try:
        start_datetime = datetime.strptime(
            f'{appoint_date_str} {start_time_formatted}:00', '%Y-%m-%d %H:%M:%S'
        )
        end_datetime = datetime.strptime(
            f'{appoint_date_str} {end_time_formatted}:00', '%Y-%m-%d %H:%M:%S'
        )
        plan_arrival_start = int(start_datetime.timestamp() * 1000)
        plan_arrival_end = int(end_datetime.timestamp() * 1000)
    except ValueError as e:
        pytest.fail(f'时间戳转换失败：{e}')

    next_day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d') + ' 00:00:00'
    delivery_order_param = {
        'deliveryMaterialBatchList': [
            {
                'purchaseOrderDetailCode': global_config['purchaseOrderDetailCode'],
                'jindiePurchaseOrderNo': global_config['JINDIE_PURCHASE_ORDER_NO'],
                'warehouseInfo': {
                    'code': '2f4cf69c98cf438dac7b7a11f18c1507',
                    'name': '华鼎郑州普洛斯',
                    'principal': '0',
                    'tel': '',
                    'address': '',
                    'jindieWarehouseId': '738335',
                    'property': '1',
                    'jindieWarehouseCode': 'CK005',
                    'propertyCn': '普通仓库',
                    'useOrgId': '105382',
                    'useOrgName': '锅圈供应链仓库',
                    'isReplenish': 1,
                    'isMainWarehouse': 1,
                    'mainWarehouseCode': '',
                    'queryWarehouseListOrder': 99,
                    'channelCn': '华鼎',
                },
                'purchaseDate': None,
                'producerCode': 'P644212',
                'producerName': '自动化测试厂商',
                'materialCode': global_config['materialCode'],
                'materialName': global_config['materialName'],
                'materialSpec': global_config['materialSpec'],
                'purchaseUnit': '件',
                'deliveryDate': next_day,
                'purchaseNum': '10.00',
                'channelTotalPurchaseNum': 10,
                'materialChannel': 1,
                'materialChannelCn': '通用',
                'deliveredNum': None,
                'notDeliveredNum': None,
                'oweNum': '10.00',
                'producerChannelMaterialCode': '942457c516b149ebb3ff465d5641b171',
                'supplierCode': 'P170403',
                'batchNoResVos': [
                    {
                        'batchNo': global_config['batchNo'],
                        'inventoryBatchCode': global_config['inventoryBatchCode'],
                        'inventoryNum': global_config['inventoryNum'],
                    }
                ],
                'deliveryNum': '10',
                'reportSet': 1,
                'reportResModels': [],
                'batchNo': '20260716',
                'inventoryBatchCode': global_config['inventoryBatchCode'],
            }
        ],
        'deliveryWay': 10,
        'warehouseCode': 'CK005',
        'selfDelivery': {
            'deliveryWay': 10,
            'driverName': '王钦',
            'driverMobile': '15000975800',
            'carNumber': 'A123456',
            'planArrivalTime': [global_config['appointDate'], plan_arrival_time],
            'carId': 721378666554064900,
            'carType': '6.8米冷藏厢货',
        },
        'planArrivalTimeStart': plan_arrival_start,
        'planArrivalTimeEnd': plan_arrival_end,
    }

    json_data = post_and_assert(
        global_config, DELIVERY_SAVE_API, delivery_order_param, '采购订单发货'
    )
    print('采购订单发货', json_data)
    print(f'\n【发货成功】采购订单编码：{global_config.get("JINDIE_PURCHASE_ORDER_NO")}')
