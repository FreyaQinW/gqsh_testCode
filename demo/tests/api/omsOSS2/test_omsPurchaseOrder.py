# -*- coding: utf-8 -*-
import pytest

from utils.api_helper import current_month_datetime_range, query_oms_list

purchase_start_time, purchase_end_time = current_month_datetime_range()


@pytest.mark.run(order=1)
def test_omsPurchaseOrder_list(global_config):
    """列表展示 OMS 采购订单列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/omsPurchaseOrder/page',
        {
            'purchaseStartTime': purchase_start_time,
            'purchaseEndTime': purchase_end_time,
            'purchaseOrderNo': '',
            'thirdPartyPurchaseOrderNo': '',
            'deliveryStartDate': '',
            'deliveryEndDate': '',
            'supplierNo': '',
            'supplierName': '',
            'status': '',
            'terminationStatus': '',
            'type': '',
            'closeStatus': '',
            'page': 1,
            'limit': 10,
        },
        'oms 采购订单列表',
    )


@pytest.mark.run(order=2)
def test_omsPurchaseNoticeOrder_list(global_config):
    """查询 OMS 来料通知单列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/omsPurchaseNoticeOrder/page',
        {
            'shipStartDate': purchase_start_time,
            'shipEndDate': purchase_end_time,
            'noticeOrderNo': '',
            'supplierCode': '',
            'supplierName': '',
            'thirdPartyPurchaseOrderNo': '',
            'thirdPartyNoticeOrderNo': '',
            'inspectOrderNo': '',
            'pushDownStatus': '',
            'purchaseOrderNo': '',
            'page': 1,
            'limit': 10,
        },
        'oms 来料通知单列表',
    )


@pytest.mark.run(order=3)
def test_omsPurchaseStockInOrder_list(global_config):
    """查询 OMS 采购入库单列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/api/stock/in/page',
        {
            'startTime': purchase_start_time,
            'endTime': purchase_end_time,
            'stockInOrderNo': '',
            'warehouseCode': '',
            'supplierNo': '',
            'supplierName': '',
            'thirdOrderNo': '',
            'orgOrderNo': '',
            'syncJinDieStatus': '',
            'page': 1,
            'limit': 10,
        },
        'oms 采购入库单列表',
    )


@pytest.mark.run(order=4)
def test_omsRejectedMaterial_list(global_config):
    """查询 OMS 退料单列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/OmsRejectedMaterial/page',
        {
            'beginDate': purchase_start_time,
            'endDate': purchase_end_time,
            'supplierName': '',
            'returnOrderNo': '',
            'returnType': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        'oms OmsRejectedMaterial 列表',
    )
