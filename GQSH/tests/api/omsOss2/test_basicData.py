# -*- coding: utf-8 -*-
"""OMS 基础数据 API 接口测试"""
import pytest

from utils.api_helper import first_oss2_list_item, post_and_assert_oss2, post_json, query_oss2_list


@pytest.mark.oms
def test_basicData_supplierList(global_config):
    """基础数据 - 商品列表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/product/queryProductList',
        {
            "name":"","code":"","page":1,"limit":10
        },
        '基础数据商品列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_basicData_getShopListByPage(global_config):
    """基础数据 - 门店信息列表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/shop/getShopListByPage',
        {"shopName":"","shopCode":"","areaAddress":"","isSync":"","page":1,"limit":10},
        '门店信息列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_basicData_syncAllShopCenterData(global_config):
    """基础数据 - 全量同步店铺中心店铺数据"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/shop/syncAllShopCenterData',
        {},
        '全量同步店铺中心店铺数据',
    )




@pytest.mark.oms
def test_basicData_syncAllShopData(global_config):
    """基础数据 - 全量更新店铺中心数据"""
    jd = post_json(global_config, '/api/oms-admin/shop/syncAllShopData', {})
    print(f'全量更新店铺中心数据 响应: {jd}')


@pytest.mark.oms
def test_basicData_warehouseListpage(global_config):
    """基础数据 - 查询仓库列表"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieWarehouse/page',
        {"jdWarehouseCode":"","jdWarehouseName":"","page":1,"limit":10},
        '基础数据仓库列表',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_basicData_warehouseListsync(global_config):
    """基础数据 - 仓库同步金蝶数据"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieWarehouse/sync',
        {},
        '仓库同步金蝶数据',
    )


@pytest.mark.oms
def test_basicData_jinDieCustomerpage(global_config):
    """基础数据 - 查询客户信息"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieCustomer/page',
        {"jdCustomerCode":"","jdCustomerName":"","page":1,"limit":10},
        '查询客户信息',
        skip_if_empty=True,
    )


@pytest.mark.oms
def test_basicData_jinDieCustomersync(global_config):
    """基础数据 - 全量同步金蝶客户信息"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieCustomer/sync',
        {},
        '全量同步金蝶客户信息',
    )


@pytest.mark.oms
def test_basicData_jinDieSupplier(global_config):
    """基础数据 - 查询供应商信息"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieSupplier/page',
        {"jdSupplierCode":"","jdSupplierName":"","address":"","page":1,"limit":10},
        '查询供应商信息',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jinDieSuppliersync(global_config):
    """基础数据 - 同步金蝶全量供应商信息"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieSupplier/sync',
        {},
        '同步金蝶全量供应商信息',
    )



@pytest.mark.oms
def test_basicData_jinDieManufacturerpage(global_config):
    """基础数据 - 查询金蝶生产厂家"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieManufacturer/page',
        {"jdSupplierCode":"","jdSupplierName":"","address":"","page":1,"limit":10},
        '查询金蝶生产厂家',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jinDieManufacturerpagesync(global_config):
    """基础数据 - 同步金蝶生产厂家"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieManufacturer/sync',
        {},
        '同步金蝶生产厂家',
    )



@pytest.mark.oms
def test_basicData_jindieProductRelationManufacturerPage(global_config):
    """基础数据 - 查询物流与厂家的关系"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jindieProductRelationManufacturer/page',
        {"productCode":"","productName":"","manufacturerCode":"","manufacturerName":"","supplierCode":"","supplierName":"","page":1,"limit":10},
        '查询物流与厂家的关系',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jindieProductRelationManufacturersync(global_config):
    """基础数据 - 同步金蝶物流与厂家的关系"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jindieProductRelationManufacturer/sync',
        {},
        '同步金蝶物流与厂家的关系',
    )



@pytest.mark.oms
def test_basicData_jindieMaterielRelationOrganizationPage(global_config):
    """基础数据 - 查询物料与组织关系"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jindieMaterielRelationOrganization/page',
        {"materielCode":"","materielName":"","organizationCode":"","organizationName":"","page":1,"limit":10},
        '查询金蝶物流与厂家的关系',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jindieMaterielRelationOrganizationsync(global_config):
    """基础数据 - 同步金蝶物料与组织关系"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jindieMaterielRelationOrganization/sync',
        {},
        '同步金蝶物料与组织关系',
    )



@pytest.mark.oms
def test_basicData_jinDieAssistInfoPageCksqlx(global_config):
    """基础数据 - 查询出库申请单类型"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieAssistInfo/page/cksqlx',
        {"childCode":"","childName":"","page":1,"limit":10},
        '查询出库申请单类型',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jinDieAssistInfoPagesyncCksqlx(global_config):
    """基础数据 - 同步金蝶出库申请单类型"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieAssistInfo/sync/cksqlx',
        {},
        '同步金蝶出库申请单类型',
    )



@pytest.mark.oms
def test_basicData_jinDieDepartmentPage(global_config):
    """基础数据 - 查询金蝶部门"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieDepartment/page',
        {"departmentCode":"","departmentName":"","page":1,"limit":10},
        '查询金蝶部门',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jinDieDepartmentsync(global_config):
    """基础数据 - 同步金蝶部门"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieDepartment/sync',
        {},
        '同步金蝶部门',
    )



@pytest.mark.oms
def test_basicData_jinDieUnitPage(global_config):
    """基础数据 - 查询计量单位"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieUnit/page',
        {"groupName":"","groupCode":"","page":1,"limit":10},
        '查询计量单位',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jinDieUnitSync(global_config):
    """基础数据 - 同步金蝶计量单位"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieUnit/sync',
        {},
        '同步金蝶计量单位',
    )



@pytest.mark.oms
def test_basicData_jinDieBusinessGroupPage(global_config):
    """基础数据 - 查询金蝶业务组"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieBusinessGroup/page',
        {"businessGroupNumber":"","businessGroupName":"","page":1,"limit":10},
        '查询金蝶业务组',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jinDieBusinessGroupsync(global_config):
    """基础数据 - 同步金蝶业务组"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieBusinessGroup/sync',
        {},
        '同步金蝶业务组',
    )



@pytest.mark.oms
def test_basicData_jinDieBusinessOperator(global_config):
    """基础数据 - 查询金蝶业务员"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieBusinessOperator/page',
        {"businessOperatorNumber":"","businessOperatorName":"","page":1,"limit":10},
        '查询金蝶业务员',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jinDieBusinessOperatorSync(global_config):
    """基础数据 - 同步金蝶业务员"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieBusinessOperator/sync',
        {},
        '同步金蝶业务员',
    )



@pytest.mark.oms
def test_basicData_jinDieSettleTypePage(global_config):
    """基础数据 - 查询金蝶结算方式"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/jinDieSettleType/page',
        {"settleTypeNumber":"","settleTypeName":"","page":1,"limit":10},
        '查询金蝶结算方式',
        skip_if_empty=True,
    )



@pytest.mark.oms
def test_basicData_jinDieSettleTypesync(global_config):
    """基础数据 - 同步金蝶结算方式"""
    post_and_assert_oss2(
        global_config,
        '/api/oms-admin/jinDieSettleType/sync',
        {},
        '同步金蝶结算方式',
    )



@pytest.mark.oms
def test_basicData_dictPage(global_config):
    """基础数据 - 数据字典"""
    query_oss2_list(
        global_config,
        '/api/oms-admin/dict/page',
        {"name":"","code":"","page":1,"limit":10},
        '查询数据字典',
        skip_if_empty=True,
    ) 


@pytest.mark.oms
def test_basicData_list(global_config):
    """基础数据 - 查询基础数据列表"""
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/product/queryProductList',
        {
            'page': 1,
            'limit': 10,
        },
        '基础数据列表',
        skip_if_empty=True,
    )
    first = first_oss2_list_item(json_data, '基础数据列表')
    basic_data_no = first.get('basicDataNo')
    global_config['basicDataNo'] = basic_data_no
    print(f'基础数据 basicDataNo: {basic_data_no}')


@pytest.mark.oms
def test_basicDataDetail(global_config):
    """基础数据 - 基础数据列表详情"""
    basic_data_no = global_config.get('basicDataNo', '')
    json_data = query_oss2_list(
        global_config,
        '/api/oms-admin/product/queryProductList',
        {
            'basicDataNo': basic_data_no,
            'page': 1,
            'limit': 10,
        },
        '基础数据详情',
        skip_if_empty=True,
    )
    print(f'基础数据详情接口查询结果: {json_data}')

