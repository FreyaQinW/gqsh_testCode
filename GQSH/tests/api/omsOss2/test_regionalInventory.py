# -*- coding: utf-8 -*-
"""OMS 区域实时库存 API 接口测试"""
import pytest

from utils.api_helper import (
    current_month_datetime_range,
    first_oss2_list_item,
    pick_oss2_id,
    post_and_assert_oss2,
    query_oss2_list,
)

data_start_time, data_end_time = current_month_datetime_range()


@pytest.mark.oms
def test_regionalInventory_list(global_config):
    """区域实时库存 - 查询区域库存列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/regionalInventory/page',
        {
            'regionCode': '',
            'regionName': '',
            'materialCode': '',
            'materialName': '',
            'warehouseCode': '',
            'page': 1,
            'limit': 10,
        },
        '区域实时库存列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, '区域实时库存列表')
    region_code = first.get('regionCode')
    global_config['regionCode'] = region_code
    print(f'区域实时库存 regionCode: {region_code}')


@pytest.mark.oms
def test_regionalInventoryDetail(global_config):
    """区域实时库存 - 区域库存列表详情"""
    region_code = global_config.get('regionCode', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/regionalInventory/page',
        {
            'regionCode': region_code,
            'page': 1,
            'limit': 10,
        },
        '区域实时库存详情',
        skip_if_empty=True,
    )
    print(f'区域实时库存详情接口查询结果: {json_data}')


@pytest.mark.oms
def test_regionalInventory_summary(global_config):
    """区域实时库存 - 有列表数据时带 regionCode 查汇总，否则仅传时间范围"""
    list_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/regionalInventory/page',
        {
            'regionCode': '',
            'regionName': '',
            'materialCode': '',
            'materialName': '',
            'warehouseCode': '',
            'page': 1,
            'limit': 10,
        },
        '区域实时库存列表',
        skip_if_empty=True,
    )
    item = first_oss2_list_item(list_data, '区域实时库存列表')
    region_key, region_value = pick_oss2_id(item, 'regionCode', 'regionId', 'id')
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/api/regionalInventory/summary',
        {
            region_key: region_value,
            'startTime': data_start_time,
            'endTime': data_end_time,
        },
        '区域实时库存汇总',
    )


@pytest.mark.oms
def test_regionalInventory_detail(global_config):
    """区域实时库存 - 查询库存明细（尽量带上列表中的区域/仓/物料）"""
    list_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/regionalInventory/page',
        {
            'regionCode': '',
            'regionName': '',
            'materialCode': '',
            'materialName': '',
            'warehouseCode': '',
            'page': 1,
            'limit': 10,
        },
        '区域实时库存列表',
        skip_if_empty=True,
    )
    item = first_oss2_list_item(list_data, '区域实时库存列表')
    body = {
        'regionCode': item.get('regionCode', ''),
        'warehouseCode': item.get('warehouseCode', ''),
        'materialCode': item.get('materialCode', ''),
        'page': 1,
        'limit': 10,
    }
    query_oss2_list(
        global_config,
        '/api/oms-admin/api/regionalInventory/detail',
        body,
        '区域实时库存明细',
        skip_if_empty=True,
    )
