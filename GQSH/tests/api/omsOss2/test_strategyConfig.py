# -*- coding: utf-8 -*-
"""OMS 策略配置 API 接口测试"""
import pytest

from utils.api_helper import first_oms_list_item, query_oms_list


@pytest.mark.oms
def test_strategyConfig_routingList(global_config):
    """策略配置 - 查询订单路由策略列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/api/strategy/routing/page',
        {
            'strategyName': '',
            'strategyType': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '订单路由策略列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_strategyConfig_allocationList(global_config):
    """策略配置 - 查询分仓策略列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/api/strategy/allocation/page',
        {
            'strategyName': '',
            'warehouseCode': '',
            'regionCode': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '分仓策略列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_strategyConfig_inventoryStrategyList(global_config):
    """策略配置 - 查询库存策略列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/api/strategy/inventory/page',
        {
            'strategyName': '',
            'warehouseCode': '',
            'materialCode': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '库存策略列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_strategyConfig_list(global_config):
    """策略配置 - 查询策略配置列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/strategyConfig/page',
        {
            'page': 1,
            'limit': 10,
        },
        '策略配置列表',
        skip_if_empty=True,
    )
    first = first_oms_list_item(json_data, '策略配置列表')
    strategy_config_no = first.get('strategyConfigNo')
    global_config['strategyConfigNo'] = strategy_config_no
    print(f'策略配置 strategyConfigNo: {strategy_config_no}')


@pytest.mark.oms
def test_strategyConfigDetail(global_config):
    """策略配置 - 策略配置列表详情"""
    strategy_config_no = global_config.get('strategyConfigNo', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/strategyConfig/page',
        {
            'strategyConfigNo': strategy_config_no,
            'page': 1,
            'limit': 10,
        },
        '策略配置详情',
        skip_if_empty=True,
    )
    print(f'策略配置详情接口查询结果: {json_data}')
