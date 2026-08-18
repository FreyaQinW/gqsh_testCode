# *-*coding:utf-8 *-*
import logging
from datetime import datetime

import pytest

from utils.api_helper import (
    get_jindie_order_no,
    post_and_assert,
    set_jindie_order_no,
    three_months_ago_date,
)

PURCHASE_QUERY_API = (
    '/api/supplier-admin/supplier-admin/interior/purchase/queryPagePurchaseOrder'
)
PURCHASE_AUDIT_API = '/api/supplier-admin/supplier-admin/interior/purchase/audit'


@pytest.mark.run(order=45)
def test_orderSearch(global_config):
    """查询采购订单（优先复用申请审核产出的金蝶单号）"""
    existing = get_jindie_order_no(global_config)
    current_date = datetime.now().strftime('%Y-%m-%d')
    start_date = three_months_ago_date()
    search_order_param = {
        'orgId': None,
        'releaseTime': [start_date, current_date],
        'pageNo': 1,
        'pageSize': 50,
        'auditEndTime': '',
        'auditStartTime': '',
        'abnormalLevel': None,
        'abnormalState': None,
        'purchaseEndTime': current_date,
        'purchaseStartTime': start_date,
        'deliveryEndTime': '',
        'deliveryStartTime': '',
        'supplierCode': None,
        'warehouseCode': None,
        # 不限定单一状态，避免与 SCMS 待确认/待发货状态错位
        'billStatusList': [],
    }

    json_data = post_and_assert(
        global_config, PURCHASE_QUERY_API, search_order_param, '采购订单查询'
    )
    items = (json_data.get('data') or {}).get('list') or []
    order_no = None
    if existing:
        for item in items:
            if item.get('jindiePurchaseOrderNo') == existing:
                order_no = existing
                break
        if not order_no:
            order_no = existing
            print(f'列表未命中，沿用桥接单号: {order_no}')
    elif items:
        order_no = items[0].get('jindiePurchaseOrderNo')

    if not order_no:
        pytest.fail('采购订单查询结果为空')

    set_jindie_order_no(global_config, order_no)
    print(f'\n【采购订单编码】{order_no}')
    logging.info('采购订单编码为 %s', order_no)


@pytest.mark.run(order=48)
def test_audit(global_config):
    """审核采购订单（已审核则视为通过）；须在 SCMS 发货前执行"""
    from utils.api_helper import parse_json, post_api

    order_no = get_jindie_order_no(global_config, required=True)
    purchase_order_no_list = {'purchaseOrderNoList': [order_no]}
    logging.info('采购订单 %s', purchase_order_no_list)
    print(f'\n【审核采购订单】{order_no}')

    response = post_api(global_config, PURCHASE_AUDIT_API, purchase_order_no_list)
    json_data = parse_json(response, '采购订单审核 ')
    audited = False
    if json_data.get('success') is True:
        logging.info('审核成功 code=%s', json_data.get('code'))
        audited = True
    else:
        msg = str(json_data.get('msg') or '')
        if '已审核' in msg:
            logging.info('订单已审核，跳过: %s', msg)
            print(f'订单已审核，跳过: {order_no}')
            audited = True
        else:
            pytest.fail(f'采购订单审核失败：{msg or "未知错误"}')

    if not audited:
        return

    # 回查列表取审核时间
    current_date = datetime.now().strftime('%Y-%m-%d')
    start_date = three_months_ago_date()
    query_body = {
        'orgId': None,
        'releaseTime': [start_date, current_date],
        'pageNo': 1,
        'pageSize': 50,
        'auditEndTime': '',
        'auditStartTime': '',
        'abnormalLevel': None,
        'abnormalState': None,
        'purchaseEndTime': current_date,
        'purchaseStartTime': start_date,
        'deliveryEndTime': '',
        'deliveryStartTime': '',
        'supplierCode': None,
        'warehouseCode': None,
        'billStatusList': [],
    }
    query_json = post_and_assert(global_config, PURCHASE_QUERY_API, query_body, '审核后回查采购订单')
    items = (query_json.get('data') or {}).get('list') or []
    matched = next(
        (item for item in items if item.get('jindiePurchaseOrderNo') == order_no),
        None,
    )
    audit_time = None
    if matched:
        for key in ('auditTime', 'auditDate', 'approveTime', 'checkTime', 'updateTime'):
            if matched.get(key) not in (None, ''):
                audit_time = matched.get(key)
                break
    print(f'【审核 order_no】{order_no}')
    print(f'【审核时间】{audit_time or "未返回"}')
    if matched:
        print(
            f'【审核状态】billStatus={matched.get("billStatus")} '
            f'auditStatus={matched.get("auditStatus")}'
        )
    logging.info('审核 order_no=%s audit_time=%s', order_no, audit_time)
