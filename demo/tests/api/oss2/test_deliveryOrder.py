# *-*coding:utf-8 *-*
import pytest

from utils.api_helper import assert_list_not_empty, post_and_assert

DELIVERY_QUERY_API = '/api/supplier-admin/supplier-admin/interior/deliveryOrder/queryPage'


@pytest.mark.run(order=1)
def test_deliveryOrderSearch(global_config):
    """条件查询发货单列表"""
    search_order_param = {
        'channelObj': {'supplierId': ''},
        'deliverTime': None,
        'handTime': [],
        'materialChannelList': [],
        'stockObj': {
            'jindieWarehouseId': '738335',
            'channelName': '华鼎郑州普洛斯',
            'jindieWarehouseCode': 'CK005',
            'code': '2f4cf69c98cf438dac7b7a11f18c1507',
        },
        'pageNo': 1,
        'pageSize': 10,
        'supplierDeliveryEndDate': '',
        'supplierDeliveryStartDate': '',
        'expectedArriveTimeEnd': '',
        'expectedArriveTimeStart': '',
        'supplierCode': None,
        'jindieWarehouseId': '738335',
    }
    json_data = post_and_assert(
        global_config, DELIVERY_QUERY_API, search_order_param, '发货单列表查询'
    )
    print('发货列表', json_data)
    assert_list_not_empty(json_data, '发货单列表')
