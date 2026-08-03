# *-*coding:utf-8 *-*
import os
from datetime import datetime

import pytest

from utils.api_helper import assert_auth_ok, assert_failure, post_and_assert, post_json

BASE_API = '/api/supplier-admin/supplier-admin/interior/baseInfoMessage'
QUERY_BY_PAGE_API = BASE_API + '/querySupplierInfoByPage'


def _build_insert_param(base_overrides=None, finance_overrides=None):
    """构建新增供应商请求体"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]
    param = {
        'createdBy': 'wangqin01',
        'updatedBy': 'wangqin01',
        'supplierBaseInfo': {
            'orgCode': '1',
            'disableStatus': 0,
            'groupCodeList': [],
            'supplierName': f'test-auto-{timestamp}',
            'areaCode': ['620000', '623000', '623022'],
            'supplierDetailedAddress': '自动化测试地址',
            'businessNature': 1,
            'purchaseSpecialist': '802658',
            'purchaseManager': '100147',
            'lifeCycle': 2,
            'businessType': 1,
            'provinceCode': '620000',
            'cityCode': '623000',
            'districtCode': '623022',
        },
        'supplierContactList': [],
        'supplierFinance': {
            'bankBranch': '中国工商银行股份有限公司票据营业部北京分部',
            'bankName': '中国工商银行',
            'bankLinkNo': '102100010022',
            'bankAccount': '102100010022102100010022',
            'accountName': '102100010022',
            'creditCode': '102100010022102100010022',
            'paymentTerm': '9c91bd1db2b9402f9bf7604f4095ad3c',
            'defaultTaxRate': '13',
            'payDateConfig': 3,
            'invoiceType': 1,
        },
        'supplierLicenseInfo': {
            'businessLicenseMediaList': [],
            'haccpMediaList': [],
            'isoMediaList': [],
            'otherMediaList': [],
        },
    }
    if base_overrides is not None:
        param['supplierBaseInfo'].update(base_overrides)
    if finance_overrides is not None:
        param['supplierFinance'] = finance_overrides
    return param


@pytest.mark.run(order=1)
def test_insertSupplierInfo_success(global_config):
    """新增供应商 -- 完整信息，应成功创建"""
    param = _build_insert_param()
    supplier_name = param['supplierBaseInfo']['supplierName']
    json_data = post_and_assert(global_config, BASE_API + '/insertSupplierInfoDetail', param, '供应商新增')
    print('新增结果', json_data)

    query_data = post_and_assert(
        global_config,
        QUERY_BY_PAGE_API,
        {
            'releaseTime': [], 'lifeCycle': [], 'groupCode': [],
            'pageNo': 1, 'pageSize': 10,
            'createDateEnd': '', 'createDateStart': '',
            'cityCode': [], 'districtCode': [], 'provinceCode': [],
            'auditStatusList': [],
            'supplierName': supplier_name,
        },
        '新增后供应商查询',
    )
    supplier_list = query_data.get('data', {}).get('list', [])
    if not supplier_list:
        pytest.fail(f'新增成功但查不到供应商：{supplier_name}')

    supplier_code = supplier_list[0].get('supplierCode')
    supplier_inner_code = supplier_list[0].get('code')
    global_config['inserted_supplier_name'] = supplier_name
    global_config['inserted_supplier_code'] = supplier_code
    global_config['inserted_supplier_inner_code'] = supplier_inner_code
    os.environ['INSERTED_SUPPLIER_CODE'] = supplier_code or ''
    os.environ['INSERTED_SUPPLIER_NAME'] = supplier_name or ''
    os.environ['INSERTED_SUPPLIER_INNER_CODE'] = supplier_inner_code or ''
    print(
        f'新增成功 — 供应商名称：{supplier_name}，'
        f'供应商编码：{supplier_code}，内部code：{supplier_inner_code}'
    )


@pytest.mark.run(order=2)
def test_insertSupplierInfo_emptyName(global_config):
    """新增供应商 -- 供应商名称为空，应返回错误"""
    json_data = post_json(
        global_config,
        BASE_API + '/insertSupplierInfoDetail',
        _build_insert_param(base_overrides={'supplierName': ''}),
    )
    print('空名称响应', json_data)
    assert_failure(json_data, '供应商名称为空')
    print('校验通过：名称为空返回错误', json_data.get('msg'))


@pytest.mark.run(order=3)
@pytest.mark.xfail(reason='系统Bug：接口未对地区字段做必填校验，空地区可新增成功', strict=False)
def test_insertSupplierInfo_emptyArea(global_config):
    """新增供应商 -- 地区信息为空，应返回错误"""
    json_data = post_json(
        global_config,
        BASE_API + '/insertSupplierInfoDetail',
        _build_insert_param(base_overrides={
            'areaCode': [], 'provinceCode': '', 'cityCode': '', 'districtCode': '',
        }),
    )
    print('空地区响应', json_data)
    assert_failure(json_data, '地区信息为空')
    print('校验通过：地区为空返回错误', json_data.get('msg'))


@pytest.mark.run(order=4)
@pytest.mark.xfail(reason='系统Bug：接口未对采购专员字段做必填校验，空值可新增成功', strict=False)
def test_insertSupplierInfo_emptyPurchaseSpecialist(global_config):
    """新增供应商 -- 采购专员为空，应返回错误"""
    json_data = post_json(
        global_config,
        BASE_API + '/insertSupplierInfoDetail',
        _build_insert_param(base_overrides={'purchaseSpecialist': ''}),
    )
    print('空采购专员响应', json_data)
    assert_failure(json_data, '采购专员为空')
    print('校验通过：采购专员为空返回错误', json_data.get('msg'))


@pytest.mark.run(order=5)
@pytest.mark.xfail(reason='系统Bug：接口未对财务信息做必填校验，空值可新增成功', strict=False)
def test_insertSupplierInfo_emptyFinance(global_config):
    """新增供应商 -- 财务信息为空，应返回错误"""
    json_data = post_json(
        global_config,
        BASE_API + '/insertSupplierInfoDetail',
        _build_insert_param(finance_overrides={}),
    )
    print('空财务信息响应', json_data)
    assert_failure(json_data, '财务信息为空')
    print('校验通过：财务信息为空返回错误', json_data.get('msg'))


@pytest.mark.run(order=6)
def test_queryInsertedSupplier(global_config):
    """新增供应商后 -- 验证在列表中能查询到"""
    supplier_name = global_config.get('inserted_supplier_name')
    if not supplier_name:
        pytest.skip('未找到 order=1 新增的供应商名称，跳过验证')

    json_data = post_and_assert(
        global_config,
        QUERY_BY_PAGE_API,
        {
            'releaseTime': [], 'lifeCycle': [], 'groupCode': [],
            'pageNo': 1, 'pageSize': 10,
            'createDateEnd': '', 'createDateStart': '',
            'cityCode': [], 'districtCode': [], 'provinceCode': [],
            'auditStatusList': [],
            'supplierName': supplier_name,
        },
        '新增供应商列表验证',
    )
    supplier_list = json_data.get('data', {}).get('list', [])
    if not supplier_list:
        pytest.fail(f'列表中未找到新增的供应商：{supplier_name}')
    if not any(s.get('supplierName') == supplier_name for s in supplier_list):
        pytest.fail(f'列表中未找到供应商名称 {supplier_name}')
    print(f'验证通过：供应商 {supplier_name} 已存在于列表中')


@pytest.mark.run(order=7)
def test_auditInsertedSupplier(global_config):
    """新增供应商后 -- 审核通过，使供应商状态变为已审核"""
    inner_code = global_config.get('inserted_supplier_inner_code')
    supplier_code = global_config.get('inserted_supplier_code')
    if not inner_code or not supplier_code:
        pytest.skip('未找到 order=1 新增的供应商信息，跳过审核用例')

    print(f'审核供应商 — 编码：{supplier_code}，内部code：{inner_code}')
    post_and_assert(
        global_config,
        BASE_API + '/auditSupplierInfo',
        {'useOrgIds': ['1'], 'code': inner_code, 'supplierCode': supplier_code},
        '供应商审核',
    )
    print(f'供应商审核通过 — {supplier_code}')
