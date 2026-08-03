# -*- coding: utf-8 -*-
"""OMS 销售订单 API 接口测试"""
import pytest

from utils.api_helper import current_month_datetime_range, query_oms_list

sale_start_time, sale_end_time = current_month_datetime_range()


@pytest.mark.oms
def test_omsSalesOrder_list(global_config):
    """列表展示 OMS 销售订单列表。type/status/submitMode=9 表示“全部”（与前端筛选项一致）。"""
    query_oms_list(
        global_config,
        '/api/oms-admin/api/order/page',
        {
            'orderCreateTimeBegin': sale_start_time,
            'orderCreateTimeEnd': sale_end_time,
            'omsOrderNo': '',
            'thirdOrderNo': '',
            'type': 9,
            'bizType': '',
            'status': 9,
            'submitMode': 9,
            'page': 1,
            'limit': 10,
        },
        'oms 销售订单列表',
        skip_if_empty=False,
    )
