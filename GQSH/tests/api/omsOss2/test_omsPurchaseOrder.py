# -*- coding: utf-8 -*-
"""OMS 采购相关 API 接口测试：采购订单 / 来料通知单 / 采购入库单 / 退料单"""
import json

import pytest

from utils.api_helper import (
    assert_oss2_success,
    current_month_datetime_range,
    first_oss2_list_item,
    oss2_page_payload,
    parse_json,
    post_api,
    query_oss2_list,
)

purchase_start_time, purchase_end_time = current_month_datetime_range()

# ---- paths ----
PATH_PURCHASE_ORDER = '/api/oms-admin/omsPurchaseOrder/page'
PATH_NOTICE_ORDER = '/api/oms-admin/omsPurchaseNoticeOrder/page'
PATH_STOCK_IN = '/api/oms-admin/api/stock/in/page'
PATH_REJECTED = '/api/oms-admin/OmsRejectedMaterial/page'

# ---- list bodies ----
PURCHASE_ORDER_LIST_BODY = {
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
}

NOTICE_ORDER_LIST_BODY = {
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
}

STOCK_IN_LIST_BODY = {
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
}

REJECTED_LIST_BODY = {
    'beginDate': purchase_start_time,
    'endDate': purchase_end_time,
    'supplierName': '',
    'returnOrderNo': '',
    'returnType': '',
    'status': '',
    'page': 1,
    'limit': 10,
}


def _query_list_items(global_config, path, body, label):
    """POST 分页列表，返回 list（允许为空，不 skip）。"""
    response = post_api(global_config, path, body)
    json_data = parse_json(response, f'{label} ')
    assert_oss2_success(json_data, label)
    page = oss2_page_payload(json_data) or {}
    items = page.get('list') or []
    print(f'{label}: totalCount={page.get("totalCount", 0)}, pageSize={len(items)}')
    return items


def _fetch_biz_no(global_config, path, body, id_key, label, date_keys):
    """取首条业务单号；当月无数据时清空 date_keys 再查一次。"""
    items = _query_list_items(global_config, path, dict(body), label)
    if items and items[0].get(id_key):
        return items[0].get(id_key)

    fallback = dict(body)
    for key in date_keys:
        fallback[key] = ''
    items = _query_list_items(global_config, path, fallback, f'{label}(全量)')
    if not items:
        return None
    return items[0].get(id_key)


def _ensure_ctx_no(global_config, ctx_key, fetch_fn, skip_msg):
    """从上下文取单号，缺失则回查；仍无则 skip。"""
    biz_no = global_config.get(ctx_key) or ''
    if not biz_no:
        biz_no = fetch_fn(global_config) or ''
        global_config[ctx_key] = biz_no
    if not biz_no:
        pytest.skip(skip_msg)
    return biz_no


def _assert_required_fields(detail, required_fields, label):
    missing = [f for f in required_fields if f not in detail]
    if missing:
        pytest.fail(f'{label}缺少字段: {missing}')


def _assert_detail_by_filter(
    global_config,
    *,
    path,
    filter_body,
    id_key,
    expected_id,
    label,
    required_fields,
    summary_rows,
):
    """按单号查详情页 → 打完整响应 → 校验字段/单号 → 打印摘要。"""
    json_data = query_oss2_list(
        global_config,
        path,
        filter_body,
        label,
        skip_if_empty=False,
    )
    print(f'{label}完整响应: {json.dumps(json_data, ensure_ascii=False, indent=2)}')

    detail = first_oss2_list_item(json_data, label, skip_if_empty=False)
    _assert_required_fields(detail, required_fields, label)
    if detail.get(id_key) != expected_id:
        pytest.fail(f'{label}单号不匹配，期望={expected_id}，实际={detail.get(id_key)}')

    lines = '\n'.join(f'  {k}: {v}' for k, v in summary_rows(detail))
    print(f'【{label}】\n{lines}')
    return detail


def _fetch_purchase_order_no(global_config):
    return _fetch_biz_no(
        global_config,
        PATH_PURCHASE_ORDER,
        PURCHASE_ORDER_LIST_BODY,
        'purchaseOrderNo',
        'oms 采购订单列表',
        ('purchaseStartTime', 'purchaseEndTime'),
    )


def _fetch_notice_order_no(global_config):
    body = dict(NOTICE_ORDER_LIST_BODY)
    body['purchaseOrderNo'] = global_config.get('purchaseOrderNo') or ''
    return _fetch_biz_no(
        global_config,
        PATH_NOTICE_ORDER,
        body,
        'noticeOrderNo',
        'oms 来料通知单列表',
        ('shipStartDate', 'shipEndDate'),
    )


def _fetch_stock_in_order_no(global_config):
    return _fetch_biz_no(
        global_config,
        PATH_STOCK_IN,
        STOCK_IN_LIST_BODY,
        'stockInOrderNo',
        'oms 采购入库单列表',
        ('startTime', 'endTime'),
    )


def _fetch_return_order_no(global_config):
    return _fetch_biz_no(
        global_config,
        PATH_REJECTED,
        REJECTED_LIST_BODY,
        'returnOrderNo',
        'oms 退料单列表',
        ('beginDate', 'endDate'),
    )


# ---- 采购订单 ----


@pytest.mark.oms
@pytest.mark.order(1)
def test_omsPurchaseOrder_list(global_config):
    """列表展示 OMS 采购订单列表，写入上下文 purchaseOrderNo"""
    purchase_order_no = _fetch_purchase_order_no(global_config)
    if not purchase_order_no:
        pytest.skip('无可用采购订单，跳过列表上下文写入')
    global_config['purchaseOrderNo'] = purchase_order_no
    print(f'【采购订单编码】{purchase_order_no}')


@pytest.mark.oms
@pytest.mark.order(2)
def test_omsPurchaseOrderDetail(global_config):
    """按上下文 purchaseOrderNo 查询采购订单详情并校验关键字段"""
    purchase_order_no = _ensure_ctx_no(
        global_config,
        'purchaseOrderNo',
        _fetch_purchase_order_no,
        '无可用 purchaseOrderNo，跳过采购订单详情',
    )

    def summary_rows(detail):
        lines = detail.get('detailList') or []
        line = lines[0] if lines else {}
        return [
            ('purchaseOrderNo', detail.get('purchaseOrderNo')),
            ('thirdPartyPurchaseOrderNo', detail.get('thirdPartyPurchaseOrderNo')),
            ('jinDiePurchaseOrderNo', detail.get('jinDiePurchaseOrderNo')),
            ('type/typeName', f'{detail.get("type")}/{detail.get("typeName")}'),
            ('status', detail.get('status')),
            ('source/sourceName', f'{detail.get("source")}/{detail.get("sourceName")}'),
            ('orderAmount', detail.get('orderAmount')),
            ('supplier', f'{detail.get("supplierNo")}/{detail.get("supplierName")}'),
            ('receiveOrg', f'{detail.get("receiveOrgNo")}/{detail.get("receiveOrgName")}'),
            ('receiveWare', f'{detail.get("receiveWareNo")}/{detail.get("receiveWareName")}'),
            ('closeStatus', detail.get('closeStatus')),
            ('payType', f'{detail.get("payType")}/{detail.get("payTypeName")}'),
            ('purchaseOrg', f'{detail.get("purchaseOrgNo")}/{detail.get("purchaseOrgName")}'),
            ('purchaseTime', detail.get('purchaseTime')),
            ('cargoOrgName', detail.get('cargoOrgName')),
            ('deliveryCoName', detail.get('deliveryCoName')),
            ('detailList.count', len(lines)),
            ('detail[0].gqItemName', line.get('gqItemName')),
            ('detail[0].jdItemCode', line.get('jdItemCode')),
            ('detail[0].purchaseQuantity', line.get('purchaseQuantity')),
            ('detail[0].unitPriceIncludingTax', line.get('unitPriceIncludingTax')),
        ]

    detail = _assert_detail_by_filter(
        global_config,
        path=PATH_PURCHASE_ORDER,
        filter_body={'purchaseOrderNo': purchase_order_no, 'page': 1, 'limit': 10},
        id_key='purchaseOrderNo',
        expected_id=purchase_order_no,
        label='oms 采购订单详情',
        required_fields=(
            'purchaseOrderNo',
            'thirdPartyPurchaseOrderNo',
            'type',
            'typeName',
            'status',
            'source',
            'sourceName',
            'orderAmount',
            'supplierNo',
            'supplierName',
            'receiveOrgNo',
            'receiveOrgName',
            'receiveWareNo',
            'receiveWareName',
            'closeStatus',
            'payType',
            'payTypeName',
            'purchaseOrgNo',
            'purchaseOrgName',
            'purchaseTime',
            'detailList',
        ),
        summary_rows=summary_rows,
    )
    if not isinstance(detail.get('detailList'), list):
        pytest.fail('采购订单 detailList 应为列表')


# ---- 来料通知单 ----


@pytest.mark.oms
@pytest.mark.order(3)
def test_omsPurchaseNoticeOrder_list(global_config):
    """查询 OMS 来料通知单列表，优先关联采购订单号"""
    notice_order_no = _fetch_notice_order_no(global_config)
    if not notice_order_no:
        pytest.skip('无可用来料通知单，跳过列表上下文写入')
    global_config['noticeOrderNo'] = notice_order_no
    print(f'【来料通知单编码】{notice_order_no}')


@pytest.mark.oms
@pytest.mark.order(4)
def test_omsPurchaseNoticeOrderDetail(global_config):
    """按上下文 noticeOrderNo 查询来料通知单详情并校验关键字段"""
    notice_order_no = _ensure_ctx_no(
        global_config,
        'noticeOrderNo',
        _fetch_notice_order_no,
        '无可用 noticeOrderNo，跳过来料通知单详情',
    )

    def summary_rows(detail):
        lines = detail.get('details') or []
        line = lines[0] if lines else {}
        return [
            ('noticeOrderNo', detail.get('noticeOrderNo')),
            ('purchaseOrderNo', detail.get('purchaseOrderNo')),
            ('thirdPartyNoticeOrderNo', detail.get('thirdPartyNoticeOrderNo')),
            ('type/typeName', f'{detail.get("type")}/{detail.get("typeName")}'),
            ('status', detail.get('status')),
            ('pushDownStatus', detail.get('pushDownStatus')),
            ('supplier', f'{detail.get("supplierCode")}/{detail.get("supplierName")}'),
            ('receiveWare', f'{detail.get("receiveWareNo")}/{detail.get("receiveWareName")}'),
            ('shipDate', detail.get('shipDate')),
            ('details.count', len(lines)),
            ('details[0].gqItemName', line.get('gqItemName')),
            ('details[0].jdItemCode', line.get('jdItemCode')),
            ('details[0].arrivalQuantity', line.get('arrivalQuantity')),
        ]

    detail = _assert_detail_by_filter(
        global_config,
        path=PATH_NOTICE_ORDER,
        filter_body={'noticeOrderNo': notice_order_no, 'page': 1, 'limit': 10},
        id_key='noticeOrderNo',
        expected_id=notice_order_no,
        label='oms 来料通知单详情',
        required_fields=(
            'noticeOrderNo',
            'purchaseOrderNo',
            'type',
            'typeName',
            'status',
            'pushDownStatus',
            'supplierCode',
            'supplierName',
            'receiveWareNo',
            'receiveWareName',
            'shipDate',
            'details',
        ),
        summary_rows=summary_rows,
    )
    if not isinstance(detail.get('details'), list):
        pytest.fail('来料通知单 details 应为列表')


# ---- 采购入库单 ----


@pytest.mark.oms
@pytest.mark.order(5)
def test_omsPurchaseStockInOrder_list(global_config):
    """查询 OMS 采购入库单列表，写入上下文 stockInOrderNo"""
    stock_in_order_no = _fetch_stock_in_order_no(global_config)
    if not stock_in_order_no:
        pytest.skip('无可用采购入库单，跳过列表上下文写入')
    global_config['stockInOrderNo'] = stock_in_order_no
    print(f'【采购入库单编码】{stock_in_order_no}')


@pytest.mark.oms
@pytest.mark.order(6)
def test_omsPurchaseStockInOrderDetail(global_config):
    """按上下文 stockInOrderNo 查询采购入库单详情并校验关键字段"""
    stock_in_order_no = _ensure_ctx_no(
        global_config,
        'stockInOrderNo',
        _fetch_stock_in_order_no,
        '无可用 stockInOrderNo，跳过采购入库单详情',
    )

    def summary_rows(detail):
        return [
            ('stockInOrderNo', detail.get('stockInOrderNo')),
            ('type/typeName', f'{detail.get("type")}/{detail.get("typeName")}'),
            ('stockInTime', detail.get('stockInTime')),
            ('org', f'{detail.get("orgNo")}/{detail.get("orgName")}'),
            ('warehouse', f'{detail.get("warehouseCode")}/{detail.get("warehouseName")}'),
            ('supplier', f'{detail.get("supplierNo")}/{detail.get("supplierName")}'),
            ('platform', f'{detail.get("platformCode")}/{detail.get("platformName")}'),
            ('thirdOrderNo', detail.get('thirdOrderNo')),
            ('orgOrderNo', detail.get('orgOrderNo')),
            ('jinDieStockInOrder', detail.get('jinDieStockInOrder')),
            ('purchaseOrgName', detail.get('purchaseOrgName')),
        ]

    _assert_detail_by_filter(
        global_config,
        path=PATH_STOCK_IN,
        filter_body={'stockInOrderNo': stock_in_order_no, 'page': 1, 'limit': 10},
        id_key='stockInOrderNo',
        expected_id=stock_in_order_no,
        label='oms 采购入库单详情',
        required_fields=(
            'stockInOrderNo',
            'type',
            'typeName',
            'stockInTime',
            'warehouseCode',
            'warehouseName',
            'supplierNo',
            'supplierName',
            'thirdOrderNo',
            'orgOrderNo',
        ),
        summary_rows=summary_rows,
    )


# ---- 退料单 ----


@pytest.mark.oms
@pytest.mark.order(7)
def test_omsRejectedMaterial_list(global_config):
    """查询 OMS 退料单列表，写入上下文 returnOrderNo"""
    return_order_no = _fetch_return_order_no(global_config)
    if not return_order_no:
        pytest.skip('无可用退料单，跳过列表上下文写入')
    global_config['returnOrderNo'] = return_order_no
    print(f'【退料单编码】{return_order_no}')


@pytest.mark.oms
@pytest.mark.order(8)
def test_omsRejectedMaterialDetail(global_config):
    """按上下文 returnOrderNo 查询退料单详情并校验关键字段"""
    return_order_no = _ensure_ctx_no(
        global_config,
        'returnOrderNo',
        _fetch_return_order_no,
        '无可用 returnOrderNo，跳过退料单详情',
    )

    def summary_rows(detail):
        return [
            ('returnOrderNo', detail.get('returnOrderNo')),
            ('purchaseOrderNo', detail.get('purchaseOrderNo')),
            ('thirdPartyReturnOrderNo', detail.get('thirdPartyReturnOrderNo')),
            ('bizType/returnType', f'{detail.get("bizType")}/{detail.get("returnType")}'),
            ('status', detail.get('status')),
            ('returnMaterTime', detail.get('returnMaterTime')),
            ('supplier', f'{detail.get("supplierNo")}/{detail.get("supplierName")}'),
            ('receiveWare', f'{detail.get("receiveWareNo")}/{detail.get("warehouseName")}'),
            ('syncJdStatus', detail.get('syncJdStatus')),
            ('syncHdStatus', detail.get('syncHdStatus')),
            ('hdReturnMaterialOrderNo', detail.get('hdReturnMaterialOrderNo')),
        ]

    _assert_detail_by_filter(
        global_config,
        path=PATH_REJECTED,
        filter_body={'returnOrderNo': return_order_no, 'page': 1, 'limit': 10},
        id_key='returnOrderNo',
        expected_id=return_order_no,
        label='oms 退料单详情',
        required_fields=(
            'returnOrderNo',
            'purchaseOrderNo',
            'bizType',
            'returnType',
            'status',
            'returnMaterTime',
            'supplierNo',
            'supplierName',
            'receiveWareNo',
            'warehouseName',
        ),
        summary_rows=summary_rows,
    )
