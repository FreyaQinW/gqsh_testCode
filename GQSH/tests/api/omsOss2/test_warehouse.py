# *-*coding:utf-8 *-*
"""OMS 仓储 API 接口测试"""
import pytest

from utils.api_helper import (
    current_month_datetime_range,
    first_oss2_list_item,
    parse_json,
    post_api,
    query_oss2_list,
)

data_start_time, data_end_time = current_month_datetime_range()

# ---- paths ----
BASE = '/api/oms-admin'
PATH_STOCK_ORDER_PAGE = BASE + '/stockOrder/page'
PATH_STOCK_ORDER_GET = BASE + '/stockOrder/get'
PATH_STOCK_PAGE = BASE + '/stock/page'
PATH_OTHER_ORDER_PAGE = BASE + '/OmsOtherOrder/page'

# ---- bodies ----
STOCK_TRANSFER_LIST_BODY = {
    'stockOrderType': 2,
    'startTime': '',
    'endTime': '',
    'stockOutOrderNo': '',
    'channelStockOrderNo': '',
    'clientName': '',
    'type': '',
    'orgNo': '',
    'warehouseCode': '',
    'clientPhoneNo': '',
    'page': 1,
    'limit': 10,
}

INVENTORY_LIST_BODY = {
    'stockOrderType': 1,
    'startTime': '',
    'endTime': '',
    'stockOutOrderNo': '',
    'channelStockOrderNo': '',
    'clientName': '',
    'type': '',
    'orgNo': '',
    'warehouseCode': '',
    'clientPhoneNo': '',
    'page': 1,
    'limit': 10,
}

STOCK_INVENTORY_BODY = {
    'platformSkuCode': '',
    'platformSkuName': '',
    'warehouseNo': '',
    'orgNo': '',
    'page': 1,
    'limit': 10,
}

OTHER_ORDER_BODY = {
    'otherOrderNo': '',
    'businessTypeNo': '',
    'warehouseNo': '',
    'startTime': '',
    'endTime': '',
    'source': '',
    'auditState': '',
    'page': 1,
    'limit': 10,
}


@pytest.mark.oms
def test_warehouse_stockTransferList(global_config):
    """仓储 - 库存调拨列表"""
    try:
        json_data = query_oss2_list(
            global_config, PATH_STOCK_ORDER_PAGE,
            dict(STOCK_TRANSFER_LIST_BODY),
            '仓储库存调拨列表',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, '仓储库存调拨列表')
        stock_out_no = first.get('stockOutOrderNo')
        global_config['transferNo'] = stock_out_no
        print(f'仓储库存调拨 stockOutOrderNo: {stock_out_no}')
    except Exception as e:
        pytest.fail(f'仓储库存调拨列表异常: {e}')


@pytest.mark.oms
def test_stockTransferOrderDetail(global_config):
    """仓储 - 库存调拨详情"""
    try:
        stock_out_no = global_config.get('transferNo', '')
        if not stock_out_no:
            pytest.skip('无库存调拨单号，跳过详情查询')
        body = {
            'stockOrderType': '2',
            'stockOutOrderNo': stock_out_no,
        }
        response = post_api(global_config, PATH_STOCK_ORDER_GET, body)
        json_data = parse_json(response, '仓储库存调拨详情')
        detail = (json_data.get('data') or {})
        print(f'仓储库存调拨详情 stockOutOrderNo: {stock_out_no}')
        print(f'状态: {detail.get("status")}, 仓库: {detail.get("warehouseName")}')
    except Exception as e:
        pytest.fail(f'仓储库存调拨详情异常: {e}')


@pytest.mark.oms
def test_warehouse_inventoryList(global_config):
    """仓储 - 出库单列表"""
    try:
        json_data = query_oss2_list(
            global_config, PATH_STOCK_ORDER_PAGE,
            dict(INVENTORY_LIST_BODY),
            '仓储出库单列表',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, '仓储出库单列表')
        stock_out_no = first.get('stockOutOrderNo')
        global_config['inventoryNo'] = stock_out_no
        print(f'仓储出库单号: {stock_out_no}')
    except Exception as e:
        pytest.fail(f'仓储出库单列表异常: {e}')


@pytest.mark.oms
def test_inventoryOrderDetail(global_config):
    """仓储 - 仓库即时库存"""
    try:
        json_data = query_oss2_list(
            global_config, PATH_STOCK_PAGE,
            dict(STOCK_INVENTORY_BODY),
            '仓储仓库即时库存',
            skip_if_empty=True,
        )
        print(f'仓储仓库即时库存查询完成')
    except Exception as e:
        pytest.fail(f'仓储仓库即时库存异常: {e}')


@pytest.mark.oms
def test_warehouse_stockInList(global_config):
    """仓储 - 出库申请单"""
    try:
        json_data = query_oss2_list(
            global_config, PATH_OTHER_ORDER_PAGE,
            dict(OTHER_ORDER_BODY),
            '仓储出库申请单',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, '仓储出库申请单')
        other_order_no = first.get('otherOrderNo')
        print(f'仓储出库申请单 otherOrderNo: {other_order_no}')
    except Exception as e:
        pytest.fail(f'仓储出库申请单异常: {e}')
