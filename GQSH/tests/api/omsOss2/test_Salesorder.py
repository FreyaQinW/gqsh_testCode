# -*- coding: utf-8 -*-
"""OMS 销售订单 API 接口测试----协同直供报货单"""
import pytest

from utils.api_helper import current_month_datetime_range, first_oss2_list_item, parse_json, post_api, query_oss2_list

sale_start_time, sale_end_time = current_month_datetime_range()


@pytest.mark.oms
def test_omsSalesOrder_list(global_config):
    """列表展示 OMS 销售订单列表。type/status/submitMode=9 表示“全部”（与前端筛选项一致）。"""
    try:
        json_data = query_oss2_list(
            global_config,
            '/api/oms-admin/api/order/page',
            {"orderCreateTimeBegin":"","orderCreateTimeEnd":"","omsOrderNo":"","thirdOrderNo":"","type":9,"bizType":"","status":9,"submitMode":9,"page":1,"limit":10},
            'oms 销售订单列表',
            skip_if_empty=True,
        )
        first = first_oss2_list_item(json_data, 'oms 销售订单列表')
        oms_order_no = first.get('omsOrderNo')
        third_order_no = first.get('thirdOrderNo')
        if oms_order_no:
            global_config['omsOrderNo'] = oms_order_no
            print(f'销售订单 omsOrderNo: {oms_order_no}')
        if third_order_no:
            global_config['thirdOrderNo'] = third_order_no
            print(f'销售订单 thirdOrderNo: {third_order_no}')
    except Exception as e:
        pytest.fail(f'oms 销售订单列表异常: {e}')


@pytest.mark.oms
def test_zgorderDetail(global_config):
    """销售订单 - 直供订单详情"""
    try:
        oms_order_no = global_config.get('omsOrderNo', '')
        if not oms_order_no:
            pytest.skip('无omsOrderNo参数，跳过直供订单详情查询')
        body = {'omsOrderNo': oms_order_no}
        response = post_api(global_config, '/api/oms-admin/api/order/orderDetail', body)
        json_data = parse_json(response, '直供订单详情')
        detail = json_data.get('data') or {}
        print(f'直供订单详情 omsOrderNo: {oms_order_no}')
        print(f'响应数据: {detail}')
    except Exception as e:
        pytest.fail(f'直供订单详情异常: {e}')
