# -*- coding: utf-8 -*-
"""OMS 调拨管理 API 接口测试"""
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

_LIST_BODY = {"applyEndDate":"","applyBeginDate":"","outWareNo":"","inWareNo":"","applyOrderNo":"","status":"","type":"","closeStatus":"","remark":"","createUserName":"","thirdApplyOrderNo":"","page":1,"limit":10}

_OUT_WARE_BODY = {"beginStockTime":"","endStockTime":"","outWareNo":"","inWareNo":"","transferOutOrderNo":"","billStatus":"","type":"","transferApplyNo":"","remark":"","createUserName":"","channelStockOrderNo":"","page":1,"limit":10}

_IN_WARE_BODY = {"beginStockTime":"","endStockTime":"","outWareNo":"","inWareNo":"","transferOutOrderNo":"","billStatus":"","type":"","transferApplyNo":"","remark":"","createUserName":"","page":1,"limit":10}


@pytest.mark.oms
def test_transferManagement_list(global_config):
    """调拨管理 - 查询调拨单列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/transfer/apply/page',
        dict(_LIST_BODY),
        '调拨单列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, '调拨单列表')
    transfer_order_no = first.get('applyOrderNo')
    global_config['applyOrderNo'] = transfer_order_no
    print(f'调拨单 applyOrderNo: {transfer_order_no}')


@pytest.mark.oms
def test_transferApplyDetail(global_config):
    """调拨管理 - 调拨申请单详情"""
    try:
        apply_order_no = global_config.get('applyOrderNo', '')
        if not apply_order_no:
            pytest.skip('无调拨申请单号，跳过详情查询')
        body = {'applyOrderNo': apply_order_no}
        response = post_api(global_config, '/api/oms-admin/transfer/apply/detail', body)
        json_data = parse_json(response, '调拨申请单详情')
        detail = json_data.get('data') or {}
        if isinstance(detail, list):
            detail = detail[0] if detail else {}
        print(f'调拨申请单详情 applyOrderNo: {apply_order_no}')
        print(f'响应数据: {detail}')
    except Exception as e:
        pytest.fail(f'调拨申请单详情异常: {e}')


@pytest.mark.oms
def test_transferBillOutWarePageList(global_config):
    """调拨管理 - 调拨出库单"""
    try:
        json_data = query_oss2_list(
            global_config,
            '/api/oms-admin/transfer/bill/outWare/page',
            dict(_OUT_WARE_BODY),
            '调拨出库单',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, '调拨出库单')
        transfer_stock_order_no = first.get('transferStockOrderNo')
        apply_order_no = first.get('applyOrderNo')
        if transfer_stock_order_no:
            global_config['transferStockOrderNo'] = transfer_stock_order_no
            print(f'调拨出库单 transferStockOrderNo: {transfer_stock_order_no}')
        if apply_order_no:
            global_config['applyOrderNo'] = apply_order_no
            print(f'调拨出库单 applyOrderNo: {apply_order_no}')
    except Exception as e:
        pytest.fail(f'调拨出库单异常: {e}')


@pytest.mark.oms
def test_transferBillDetail(global_config):
    """调拨管理 - 调拨出库单详情"""
    try:
        apply_order_no = global_config.get('applyOrderNo', '')
        transfer_stock_order_no = global_config.get('transferStockOrderNo', '')
        if not apply_order_no or not transfer_stock_order_no:
            pytest.skip('无调拨单号参数，跳过出库单详情查询')
        body = {
            'applyOrderNo': apply_order_no,
            'transferStockOrderNo': transfer_stock_order_no,
        }
        response = post_api(global_config, '/api/oms-admin/transfer/bill/detail', body)
        json_data = parse_json(response, '调拨出库单详情')
        detail = json_data.get('data') or {}
        if isinstance(detail, list):
            detail = detail[0] if detail else {}
        print(f'调拨出库单详情 applyOrderNo: {apply_order_no}, transferStockOrderNo: {transfer_stock_order_no}')
        print(f'响应数据: {detail}')
    except Exception as e:
        pytest.fail(f'调拨出库单详情异常: {e}')


@pytest.mark.oms
def test_transferBillinWareList(global_config):
    """调拨管理 - 调拨入库单"""
    try:
        json_data = query_oss2_list(
            global_config,
            '/api/oms-admin/transfer/bill/inWare/page',
            dict(_IN_WARE_BODY),
            '调拨入库单',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, '调拨入库单')
        transfer_stock_order_no = first.get('transferStockOrderNo')
        apply_order_no = first.get('applyOrderNo')
        if transfer_stock_order_no:
            global_config['inWareTransferStockOrderNo'] = transfer_stock_order_no
            print(f'调拨入库单 transferStockOrderNo: {transfer_stock_order_no}')
        if apply_order_no:
            global_config['inWareApplyOrderNo'] = apply_order_no
            print(f'调拨入库单 applyOrderNo: {apply_order_no}')
    except Exception as e:
        pytest.fail(f'调拨入库单异常: {e}')


@pytest.mark.oms
def test_transferBillinWareDetail(global_config):
    """调拨管理 - 调拨入库单详情"""
    try:
        apply_order_no = global_config.get('inWareApplyOrderNo', '')
        transfer_stock_order_no = global_config.get('inWareTransferStockOrderNo', '')
        if not apply_order_no or not transfer_stock_order_no:
            pytest.skip('无调拨入库单号参数，跳过详情查询')
        body = {
            'applyOrderNo': apply_order_no,
            'transferStockOrderNo': transfer_stock_order_no,
        }
        response = post_api(global_config, '/api/oms-admin/transfer/bill/detail', body)
        json_data = parse_json(response, '调拨入库单详情')
        detail = json_data.get('data') or {}
        if isinstance(detail, list):
            detail = detail[0] if detail else {}
        print(f'调拨入库单详情 applyOrderNo: {apply_order_no}, transferStockOrderNo: {transfer_stock_order_no}')
        print(f'响应数据: {detail}')
    except Exception as e:
        pytest.fail(f'调拨入库单详情异常: {e}')


