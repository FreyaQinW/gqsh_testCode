# -*- coding: utf-8 -*-
"""OMS 对码表 API 接口测试"""
import pytest

from utils.api_helper import first_oss2_list_item, query_oss2_list


@pytest.mark.oms
def test_jindieMappingWarehouse(global_config):
    """对码表 - 查询 金蝶-旺店通仓库/华鼎仓库 对码列表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jindieMappingWarehouse/page',
        {"code":"","name":"","platform":2,"page":1,"limit":10},
        '金蝶-旺店通仓库对码列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_jindieMappingItem(global_config):
    """对码表 -  商品-金蝶编码 对码表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jindieMappingItem/page',
        {"itemGqCode":"","itemJdCode":"","remark":"","id":None,"page":1,"limit":10},
        '商品-金蝶编码对码列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_jindieMappingCustomer(global_config):
    """对码表 - 客户（店铺）对码表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jindieMappingCustomer/page',
        {"code":"","name":"","platform":2,"page":1,"limit":10},
        '客户（店铺）对码表',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_thirdProduct(global_config):
    """对码表 - 第三方产品 对码表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/thirdProduct/wm/page',
        {"thirdProductCode":"",
         "thirdProductName":"",
         "thirdUnitName":"",
         "gqProductCode":"",
         "gqProductName":"",
         "gqUnitCode":"",
         "page":1,
         "limit":10},
         '第三方产品对码列表',
         skip_if_empty=True,

    )


@pytest.mark.oms
def test_codeMapping_list(global_config):
    """对码表 - 查询对码列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/codeMapping/page',
        {
            'page': 1,
            'limit': 10,
        },
        '对码表列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, '对码表列表')
    code_mapping_no = first.get('codeMappingNo')
    global_config['codeMappingNo'] = code_mapping_no
    print(f'对码表 codeMappingNo: {code_mapping_no}')


@pytest.mark.oms
def test_codeMappingDetail(global_config):
    """对码表 - 对码列表详情"""
    code_mapping_no = global_config.get('codeMappingNo', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/api/codeMapping/page',
        {
            'codeMappingNo': code_mapping_no,
            'page': 1,
            'limit': 10,
        },
        '对码表详情',
        skip_if_empty=True,
    )
    print(f'对码表详情接口查询结果: {json_data}')