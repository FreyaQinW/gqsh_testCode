# *-*coding:utf-8 *-*
import pytest

from utils.api_helper import assert_auth_ok, assert_failure, post_and_assert, post_json

BASE = '/api/supplier-admin/supplier-admin/interior/baseInfoMessage'
QUERY_BY_PAGE_API = BASE + '/querySupplierInfoByPage'


def _query_supplier_by_page(global_config, extra_params):
    """按条件分页查询供应商"""
    params = {
        'releaseTime': [],
        'lifeCycle': [],
        'groupCode': [],
        'pageNo': 1,
        'pageSize': 10,
        'createDateEnd': '',
        'createDateStart': '',
        'cityCode': [],
        'districtCode': [],
        'provinceCode': [],
        'auditStatusList': [],
    }
    params.update(extra_params)
    return post_and_assert(global_config, QUERY_BY_PAGE_API, params, '供应商分页查询')


@pytest.mark.run(order=1)
def test_queryUserInfo(global_config):
    """供应商端--查询采购经理，并保存到公共参数中"""
    json_data = post_and_assert(
        global_config,
        BASE + '/queryUserInfo',
        {'name': '王'},
        '采购经理查询',
    )
    name = json_data.get('data', [])[0].get('name')
    name_code = json_data.get('data', [])[0].get('nameCode')
    if not name:
        pytest.fail('没有查到采购经理名称')
    global_config['name'] = name
    global_config['nameCode'] = name_code
    print('采购经理名称为', name, '采购经理编码', name_code)


@pytest.mark.run(order=2)
def test_updateSupplierInfoDetail(global_config):
    """供应商端 -- 修改供应商基础信息"""
    body = {
        'createdBy': 'wangqin01',
        'updatedBy': 'wangqin01',
        'supplierBaseInfo': {
            'code': 'ca4246cf563c48fb9f8282a22f39d57a',
            'supplierCode': 'P334664',
            'supplierName': 'test-Chrome1',
            'supplierDetailedAddress': '测试',
            'orgName': '上海锅圈',
            'orgCode': '1',
            'purchaseSpecialist': '822328',
            'purchaseSpecialistStr': '王方林',
            'purchaseManager': '258041',
            'purchaseManagerStr': '王赛丽',
            'postalCode': '',
            'provinceCode': '620000',
            'cityCode': '623000',
            'districtCode': '623023',
            'provinceName': '甘肃省',
            'cityName': '甘南藏族自治州',
            'districtName': '舟曲县',
            'auditStatus': 0,
            'lifeCycle': 1,
            'lifeCycleStr': '新增',
            'disableStatus': 0,
            'disableStatusStr': '启用',
            'businessNature': 1,
            'businessNatureStr': '生产商',
            'businessType': 1,
            'businessTypeStr': '食材',
            'supplierGroupInfoList': [],
            'groupCodeList': [],
            'areaCode': ['620000', '623000', '623023'],
        },
        'supplierContactList': [],
        'supplierFinance': {
            'code': '3224f30e7f1b4ce087bdc9bbe1a2b994',
            'supplierCode': 'P334664',
            'paymentTerm': '9c91bd1db2b9402f9bf7604f4095ad3c',
            'paymentTermStr': None,
            'defaultTaxRate': 13,
            'accountName': 'test-Chrome',
            'bankBranch': '中国工商银行赞皇支行',
            'bankName': '中国工商银行',
            'bankAccount': '102121000295102121000295',
            'bankLinkNo': '102121000295',
            'creditCode': '102121000295102121000295',
            'invoiceType': None,
            'invoiceTypeStr': None,
            'payDateConfig': 1,
            'payDateConfigName': '每月支付 4 次（每周四）',
        },
        'supplierLicenseInfo': {
            'businessLicenseMediaList': [],
            'haccpMediaList': [],
            'isoMediaList': [],
            'otherMediaList': [],
        },
    }
    json_data = post_and_assert(global_config, BASE + '/updateSupplierInfoDetail', body, '修改供应商信息')
    print('响应结果', json_data)


@pytest.mark.run(order=3)
def test_querySupplierInfoByPage(global_config):
    """供应商条件查询：查询待审核的供应商信息"""
    json_data = _query_supplier_by_page(global_config, {'auditStatusList': [0]})
    print('响应结果', json_data)


@pytest.mark.run(order=4)
def test_queryAllSuppliers(global_config):
    """查询全部供应商（不过滤审核状态）"""
    json_data = _query_supplier_by_page(global_config, {'auditStatusList': []})
    total_count = json_data.get('data', {}).get('totalCount', 0)
    assert total_count > 0, '全部供应商列表不应为空'
    print('全部供应商数量:', total_count)


@pytest.mark.run(order=5)
def test_queryApprovedSuppliers(global_config):
    """查询审核通过的供应商"""
    json_data = _query_supplier_by_page(global_config, {'auditStatusList': [1]})
    total_count = json_data.get('data', {}).get('totalCount', 0)
    assert total_count > 0, '审核通过的供应商列表不应为空'
    print('审核通过供应商数量:', total_count)


@pytest.mark.run(order=6)
def test_queryBySupplierName(global_config):
    """按供应商名称模糊查询"""
    json_data = _query_supplier_by_page(global_config, {'supplierName': 'test'})
    print('按名称查询结果数量:', json_data.get('data', {}).get('totalCount', 0))


@pytest.mark.run(order=7)
def test_queryBySupplierCode(global_config):
    """按供应商编码精确查询"""
    json_data = _query_supplier_by_page(global_config, {'supplierCode': 'P334664'})
    total_count = json_data.get('data', {}).get('totalCount', 0)
    assert total_count > 0, '按编码 P334664 查询应有结果'
    print('按编码查询结果数量:', total_count)


@pytest.mark.run(order=8)
def test_queryByBusinessType(global_config):
    """按经营类型查询（食材=1）"""
    json_data = _query_supplier_by_page(global_config, {'businessType': [1]})
    print('经营类型=食材 供应商数量:', json_data.get('data', {}).get('totalCount', 0))


@pytest.mark.run(order=9)
def test_queryByLifeCycle(global_config):
    """按生命周期查询（新增=1）"""
    json_data = _query_supplier_by_page(global_config, {'lifeCycle': [1]})
    print('生命周期=新增 供应商数量:', json_data.get('data', {}).get('totalCount', 0))


@pytest.mark.run(order=10)
def test_querySupplierInfoDetail(global_config):
    """查看单个供应商详情"""
    json_data = post_and_assert(
        global_config,
        BASE + '/querySupplierInfoDetail',
        {'code': 'ca4246cf563c48fb9f8282a22f39d57a'},
        '供应商详情查询',
    )
    assert json_data.get('data') is not None, '供应商详情数据不应为空'
    print('供应商详情获取成功')


@pytest.mark.run(order=11)
def test_auditSupplierInfo(global_config):
    """审核通过一条待审核的供应商"""
    list_data = post_json(global_config, QUERY_BY_PAGE_API, {
        'releaseTime': [], 'lifeCycle': [], 'groupCode': [],
        'pageNo': 1, 'pageSize': 10,
        'createDateEnd': '', 'createDateStart': '',
        'cityCode': [], 'districtCode': [], 'provinceCode': [],
        'auditStatusList': [0],
    })
    assert_auth_ok(list_data)
    supplier_list = list_data.get('data', {}).get('list', [])
    if not supplier_list:
        pytest.skip('当前无待审核供应商，跳过审核用例')

    audited = False
    for supplier in supplier_list:
        supplier_code = supplier.get('supplierCode')
        supplier_name = supplier.get('supplierName')
        inner_code = supplier.get('code')
        print(f'尝试审核 — 名称：{supplier_name}，编码：{supplier_code}')

        json_data = post_json(global_config, BASE + '/auditSupplierInfo', {
            'useOrgIds': ['1'],
            'code': inner_code,
            'supplierCode': supplier_code,
        })
        print('审核结果', json_data)
        assert_auth_ok(json_data)
        if json_data.get('success'):
            print(f'审核通过成功 — 供应商：{supplier_name}（{supplier_code}）')
            audited = True
            break
        print(f'跳过（数据不完整）：{json_data.get("msg")}')

    if not audited:
        pytest.skip('待审核列表中无可审核的完整供应商数据，跳过审核用例')
