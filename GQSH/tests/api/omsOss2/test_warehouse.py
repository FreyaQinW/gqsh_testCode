# -*- coding: utf-8 -*-
"""OMS 仓储 API 接口测试"""
import pytest

from utils.api_helper import current_month_datetime_range, first_oms_list_item, query_oms_list

data_start_time, data_end_time = current_month_datetime_range()


@pytest.mark.oms
def test_warehouse_stockTransferList(global_config):
    """仓储 - 查询库存调拨列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/stockTransfer/page',
        {
            'startTime': data_start_time,
            'endTime': data_end_time,
            'transferNo': '',
            'fromWarehouse': '',
            'toWarehouse': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '仓储库存调拨列表',
        skip_if_empty=True,
    )
    first = first_oms_list_item(json_data, '仓储库存调拨列表')
    transfer_no = first.get('transferNo')
    global_config['transferNo'] = transfer_no
    print(f'仓储库存调拨 transferNo: {transfer_no}')


@pytest.mark.oms
def test_stockTransferOrderDetail(global_config):
    """仓储 - 库存调拨列表详情"""
    transfer_no = global_config.get('transferNo', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/stockTransfer/page',
        {
            'transferNo': transfer_no,
            'page': 1,
            'limit': 10,
        },
        '仓储库存调拨详情',
        skip_if_empty=True,
    )
    print(f'仓储库存调拨详情接口查询结果: {json_data}')


@pytest.mark.oms
def test_warehouse_inventoryList(global_config):
    """仓储 - 查询仓库库存列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/inventory/page',
        {
            'warehouseCode': '',
            'materialCode': '',
            'materialName': '',
            'page': 1,
            'limit': 10,
        },
        '仓储仓库库存列表',
        skip_if_empty=True,
    )
    first = first_oms_list_item(json_data, '仓储仓库库存列表')
    inventory_no = first.get('inventoryNo')
    global_config['inventoryNo'] = inventory_no
    print(f'仓储仓库库存 inventoryNo: {inventory_no}')


@pytest.mark.oms
def test_inventoryOrderDetail(global_config):
    """仓储 - 仓库库存列表详情"""
    inventory_no = global_config.get('inventoryNo', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/inventory/page',
        {
            'inventoryNo': inventory_no,
            'page': 1,
            'limit': 10,
        },
        '仓储仓库库存详情',
        skip_if_empty=True,
    )
    print(f'仓储仓库库存详情接口查询结果: {json_data}')


@pytest.mark.oms
def test_warehouse_stockInList(global_config):
    """仓储 - 查询入库单列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/stockIn/page',
        {
            'startTime': data_start_time,
            'endTime': data_end_time,
            'stockInNo': '',
            'warehouseCode': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '仓储入库单列表',
        skip_if_empty=True,
    )
    first = first_oms_list_item(json_data, '仓储入库单列表')
    stock_in_no = first.get('stockInNo')
    global_config['stockInNo'] = stock_in_no
    print(f'仓储入库单 stockInNo: {stock_in_no}')


@pytest.mark.oms
def test_stockInOrderDetail(global_config):
    """仓储 - 入库单列表详情"""
    stock_in_no = global_config.get('stockInNo', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/stockIn/page',
        {
            'stockInNo': stock_in_no,
            'page': 1,
            'limit': 10,
        },
        '仓储入库单详情',
        skip_if_empty=True,
    )
    print(f'仓储入库单详情接口查询结果: {json_data}')


@pytest.mark.oms
def test_warehouse_stockOutList(global_config):
    """仓储 - 查询出库单列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/stockOut/page',
        {
            'startTime': data_start_time,
            'endTime': data_end_time,
            'stockOutNo': '',
            'warehouseCode': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '仓储出库单列表',
        skip_if_empty=True,
    )
    first = first_oms_list_item(json_data, '仓储出库单列表')
    stock_out_no = first.get('stockOutNo')
    global_config['stockOutNo'] = stock_out_no
    print(f'仓储出库单 stockOutNo: {stock_out_no}')


@pytest.mark.oms
def test_stockOutOrderDetail(global_config):
    """仓储 - 出库单列表详情"""
    stock_out_no = global_config.get('stockOutNo', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/stockOut/page',
        {
            'stockOutNo': stock_out_no,
            'page': 1,
            'limit': 10,
        },
        '仓储出库单详情',
        skip_if_empty=True,
    )
    print(f'仓储出库单详情接口查询结果: {json_data}')


@pytest.mark.oms
def test_warehouse_warehouseList(global_config):
    """仓储 - 查询仓库列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/list',
        {
            'warehouseCode': '',
            'warehouseName': '',
            'page': 1,
            'limit': 10,
        },
        '仓储仓库列表',
        skip_if_empty=False,
    )
    first = first_oms_list_item(json_data, '仓储仓库列表')
    warehouse_code = first.get('warehouseCode')
    global_config['warehouseCode'] = warehouse_code
    print(f'仓储仓库 warehouseCode: {warehouse_code}')


@pytest.mark.oms
def test_warehouseDetail(global_config):
    """仓储 - 仓库列表详情"""
    warehouse_code = global_config.get('warehouseCode', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/warehouse/list',
        {
            'warehouseCode': warehouse_code,
            'page': 1,
            'limit': 10,
        },
        '仓储仓库详情',
        skip_if_empty=True,
    )
    print(f'仓储仓库详情接口查询结果: {json_data}')
