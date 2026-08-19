# -*- coding: utf-8 -*-
"""OMS 三方数据 API 接口测试"""
import pytest

from utils.api_helper import (
    current_month_datetime_range,
    first_oss2_list_item,
    parse_json,
    pick_oss2_id,
    post_api,
    post_and_assert_oss2,
    query_oss2_list,
)

data_start_time, data_end_time = current_month_datetime_range()

_DY_LIST_BODY = {
    'createTimeBegin': '',
    'createTimeEnd': '',
    'orderNo': '',
    'shopId': '',
    'shopName': '',
    'page': 1,
    'limit': 10,
}

_DY_REFUND_LIST_BODY = {
    'createTimeBegin': '',
    'createTimeEnd': '',
    'refundNo': '',
    'shopId': '',
    'shopName': '',
    'orderNo': '',
    'page': 1,
    'limit': 10,
}

_WDT_SALE_STOCK_OUT_BODY = {
    'createTimeBegin': '',
    'createTimeEnd': '',
    'thirdStockOutNo': '',
    'thirdOrderNo': '',
    'thirdSourceNo': '',
    'relationBillType': '',
    'warehouseCode': '',
    'shopNo': '',
    'syncStockStatus': '',
    'syncJdStatus': '',
    'page': 1,
    'limit': 10,
}

_WDT_REFUND_STOCK_IN_BODY = {
    'createTimeBegin': '',
    'createTimeEnd': '',
    'refundNo': '',
    'shopId': '',
    'shopName': '',
    'orderNo': '',
    'page': 1,
    'limit': 10,
}


@pytest.mark.oms
def test_thirdPartyData_dyList(global_config):
    """三方数据 - 查询抖店订单列表"""
    try:
        json_data = query_oss2_list(
            global_config,
            '/api/oms-admin/thirdOrder/dy/orderPage',
            dict(_DY_LIST_BODY),
            '抖店订单列表',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, '抖店订单列表')
        shop_id = first.get('shopId')
        order_no = first.get('orderNo')
        if shop_id:
            global_config['dyShopId'] = shop_id
            print(f'抖店 shopId: {shop_id}')
        if order_no:
            global_config['dyOrderNo'] = order_no
            print(f'抖店 orderNo: {order_no}')
    except Exception as e:
        pytest.fail(f'抖店订单列表异常: {e}')


@pytest.mark.oms
def test_thirdPartyData_dyDetail(global_config):
    """三方数据 - 查询抖店订单详情"""
    try:
        order_no = global_config.get('dyOrderNo', '')
        shop_id = global_config.get('dyShopId', '')
        if not order_no or not shop_id:
            pytest.skip('无抖店订单参数，跳过详情查询')
        body = {
            'orderNo': order_no,
            'shopId': shop_id,
        }
        response = post_api(global_config, '/api/oms-admin/thirdOrder/dy/orderDetail', body)
        json_data = parse_json(response, '抖店订单详情')
        detail = json_data.get('data') or {}
        print(f'抖店订单详情 orderNo: {order_no}, shopId: {shop_id}')
        print(f'响应数据: {detail}')
    except Exception as e:
        pytest.fail(f'抖店订单详情异常: {e}')


@pytest.mark.oms
def test_thirdPartyData_dy_refundOrderList(global_config):
    """三方数据 - 查询抖店售后列表"""
    try:
        json_data = query_oss2_list(
            global_config,
            '/api/oms-admin/thirdOrder/dy/refundOrderPage',
            dict(_DY_REFUND_LIST_BODY),
            '抖店售后列表',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, '抖店售后列表')
        refund_no = first.get('refundNo')
        if refund_no:
            global_config['dyRefundNo'] = refund_no
            print(f'抖店售后 refundNo: {refund_no}')
    except Exception as e:
        pytest.fail(f'抖店售后列表异常: {e}')


@pytest.mark.oms
def test_third_wdt_saleStockOutList(global_config):
    """三方数据 - 查询旺店通销售出库列表"""
    try:
        json_data = query_oss2_list(
            global_config,
            '/api/oms-admin/api/third/wdt/saleStockOut/page',
            dict(_WDT_SALE_STOCK_OUT_BODY),
            '旺店通销售出库列表',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, '旺店通销售出库列表')
        third_stock_out_no = first.get('thirdStockOutNo')
        if third_stock_out_no:
            global_config['wdtThirdStockOutNo'] = third_stock_out_no
            print(f'旺店通销售出库 thirdStockOutNo: {third_stock_out_no}')
    except Exception as e:
        pytest.fail(f'旺店通销售出库列表异常: {e}')


@pytest.mark.oms
def test_third_wdt_saleStockOutDetail(global_config):
    """三方数据 - 查询旺店通销售出库单据详情"""
    try:
        third_stock_out_no = global_config.get('wdtThirdStockOutNo', '')
        if not third_stock_out_no:
            pytest.skip('无旺店通销售出库单号，跳过详情查询')
        body = {
            'thirdStockOutNo': third_stock_out_no,
        }
        response = post_api(global_config, '/api/oms-admin/api/third/wdt/saleStockOut/detail', body)
        json_data = parse_json(response, '旺店通销售出库单据详情')
        detail = json_data.get('data') or {}
        print(f'旺店通销售出库单据详情 thirdStockOutNo: {third_stock_out_no}')
        print(f'响应数据: {detail}')
    except Exception as e:
        pytest.fail(f'旺店通销售出库单据详情异常: {e}')


@pytest.mark.oms
def test_third_wdt_refundStockInList(global_config):
    """三方数据 - 查询旺店通销售退货列表"""
    try:
        json_data = query_oss2_list(
            global_config,
            '/api/oms-admin/api/third/wdt/refundStockIn/page',
            dict(_WDT_REFUND_STOCK_IN_BODY),
            '旺店通销售退货列表',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, '旺店通销售退货列表')
        refund_no = first.get('thirdRefundNo')
        if refund_no:
            global_config['wdtThirdRefundNo'] = refund_no
            print(f'旺店通销售退货 thirdRefundNo: {refund_no}')
    except Exception as e:
        pytest.fail(f'旺店通销售退货列表异常: {e}')


@pytest.mark.oms
def test_third_wdt_refundStockInDetail(global_config):
    """三方数据 - 查询旺店通销售退货详情"""
    try:
        third_refund_no = global_config.get('wdtThirdRefundNo', '')
        if not third_refund_no:
            pytest.skip('无旺店通销售退货单号，跳过详情查询')
        body = {
            'thirdRefundNo': third_refund_no,
        }
        response = post_api(global_config, '/api/oms-admin/api/third/wdt/refundStockIn/detail', body)
        json_data = parse_json(response, '旺店通销售退货详情')
        detail = json_data.get('data') or {}
        print(f'旺店通销售退货详情 thirdRefundNo: {third_refund_no}')
        print(f'响应数据: {detail}')
    except Exception as e:
        pytest.fail(f'旺店通销售退货详情异常: {e}')