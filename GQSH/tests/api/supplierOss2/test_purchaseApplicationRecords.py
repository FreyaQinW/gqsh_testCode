# *-*coding:utf-8 *-*
import logging
from datetime import datetime, timedelta

import pytest

from utils.api_helper import assert_list_not_empty, assert_success, post_and_assert

ADD_API = (
    '/api/supplier-admin/supplier-admin/interior/purchaseApplicationRecords/addPurchaseApplication'
)
QUERY_API = (
    '/api/supplier-admin/supplier-admin/interior/purchaseApplicationRecords/queryByPage'
)
AUDIT_API = (
    '/api/supplier-admin/supplier-admin/interior/purchaseApplicationRecords/auditV1'
)


def _query_params(approval_status_list):
    current_date = datetime.now().strftime('%Y-%m-%d')
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    return {
        'mcIdList': [],
        'materialCodeList': [],
        'warehouseCodeList': [],
        'closedStatus': 0,
        'documentSourceList': [],
        'pageNo': 1,
        'pageSize': 100,
        'applyDateStart': current_date,
        'applyDateEnd': future_date,
        'approvalStatusList': approval_status_list,
    }


@pytest.mark.run(order=1)
def test_purchaseOrderAdd(global_config):
    """采购申请单新增"""
    apply_date = datetime.now().strftime('%Y-%m-%d')
    arrival_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    body = {
        'mcName': '王钦',
        'applyDate': apply_date,
        'materialInfos': [
            {
                'arrivalDate': arrival_date,
                'isDelete': 0,
                'materialCode': '1056341',
                'materialName': '自动化测试商品',
                'mcId': '208',
                'gift': False,
                'mcName': '王钦',
                'producerCode': 'P644212',
                'producerName': '自动化测试厂商',
                'quantity': '234',
                'materialChannel': 1,
                'channelQuantity': '234',
                'warehouseCode': 'CK005',
                'warehouseName': '华鼎郑州普洛斯',
                'unitCode': 'SPZXDWZ0325326',
                'remark': '',
            }
        ],
        'addOrderType': None,
        'orderType': 1,
        'mcId': '208',
        'remark': '新增采购申请',
        'orgId': '1',
    }
    json_data = post_and_assert(global_config, ADD_API, body, '采购申请单新增')
    logging.info('采购申请单新增完成 %s', json_data)


@pytest.mark.run(order=2)
def test_purchaseApplicationOrderSearch(global_config):
    """条件查询待审核的采购申请单"""
    body = _query_params([0])
    json_data = post_and_assert(global_config, QUERY_API, body, '待审核采购申请单查询')
    logging.info('采购申请单列表 %s', json_data)
    assert_list_not_empty(json_data, '待审核采购申请单')
    order_no = json_data.get('data', {}).get('list', [{}])[0].get('documentNo')
    if not order_no:
        pytest.fail('请重新查询采购订单编码')
    global_config['documentNo'] = order_no
    logging.info('采购申请单编码为 %s', order_no)


@pytest.mark.run(order=3)
def test_purchaseApplicationAudit(global_config):
    """采购申请审核---最新版本"""
    logging.info('%s', global_config['documentNo'])
    body = [
        {
            'checkWdt': False,
            'planNo': '',
            'documentNo': global_config['documentNo'],
            'sourceGifts': [],
            'supplierCode': 'P170403',
        }
    ]
    json_data = post_and_assert(global_config, AUDIT_API, body, '采购申请单审核')
    logging.info('采购申请单列表 %s', json_data)


@pytest.mark.run(order=4)
def test_purchaseApplicationApprovedOrderSearch(global_config):
    """条件查询审核通过的采购申请单"""
    body = _query_params([1])
    logging.info('请求参数为 %s', body)
    json_data = post_and_assert(global_config, QUERY_API, body, '已审核采购申请单查询')
    logging.info('采购申请单列表 %s', json_data)
    assert_list_not_empty(json_data, '已审核采购申请单')
    order_no = json_data.get('data', {}).get('list', [{}])[0].get('relatedOrder')
    if not order_no:
        pytest.fail('请重新查询采购订单编码')
    global_config['JINDIE_PURCHASE_ORDER_NO'] = order_no
    logging.info('采购申请单编码为 %s', order_no)
