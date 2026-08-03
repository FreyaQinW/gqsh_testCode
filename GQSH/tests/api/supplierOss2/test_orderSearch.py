# *-*coding:utf-8 *-*
import logging
import os

import pytest

from utils.api_helper import assert_success, extract_jindie_order_no, post_and_assert

PURCHASE_QUERY_API = (
    '/api/supplier-admin/supplier-admin/interior/purchase/queryPagePurchaseOrder'
)
PURCHASE_AUDIT_API = '/api/supplier-admin/supplier-admin/interior/purchase/audit'


@pytest.mark.run(order=2)
def test_orderSearch(global_config):
    """查询采购订单"""
    from datetime import datetime

    current_date = datetime.now().strftime('%Y-%m-%d')
    search_order_param = {
        'orgId': None,
        'releaseTime': ['2026-07-08', current_date],
        'pageNo': 1,
        'pageSize': 10,
        'auditEndTime': '',
        'auditStartTime': '',
        'abnormalLevel': None,
        'abnormalState': None,
        'purchaseEndTime': current_date,
        'purchaseStartTime': current_date,
        'deliveryEndTime': '',
        'deliveryStartTime': '',
        'supplierCode': None,
        'warehouseCode': None,
        'billStatusList': [0],
    }

    json_data = post_and_assert(
        global_config, PURCHASE_QUERY_API, search_order_param, '采购订单查询'
    )
    order_no = extract_jindie_order_no(json_data)
    global_config['JINDIE_PURCHASE_ORDER_NO'] = order_no
    os.environ['JINDIE_PURCHASE_ORDER_NO'] = order_no
    print(f'\n【采购订单编码】{order_no}')
    logging.info('采购订单编码为 %s', order_no)


@pytest.mark.run(order=5)
def test_audit(global_config):
    """审核采购订单"""
    order_no = global_config.get('JINDIE_PURCHASE_ORDER_NO')
    if not order_no:
        pytest.fail('采购订单为空，请先获取有效的订单编码')

    purchase_order_no_list = {'purchaseOrderNoList': [order_no]}
    logging.info('采购订单 %s', purchase_order_no_list)

    json_data = post_and_assert(
        global_config, PURCHASE_AUDIT_API, purchase_order_no_list, '采购订单审核'
    )

    if json_data.get('success') is True:
        logging.info(
            '审核成功 code=%s success=%s',
            json_data.get('code'),
            json_data.get('success'),
        )
    elif json_data.get('success') is False:
        logging.info(
            '审核失败 code=%s msg=%s',
            json_data.get('code'),
            json_data.get('msg', ''),
        )
    else:
        pytest.fail(f'未知的审核结果：{json_data}')
