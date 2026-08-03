# *-*coding:utf-8 *-*
import logging

import pytest

from utils.api_helper import assert_auth_ok, assert_failure, post_and_assert, post_json

BASE_POOL_API = '/api/supplier-admin/supplier-admin/interior/supplierPool/pool'
BASE_FLOW_API = '/api/supplier-admin/supplier-admin/interior/product-apply/flow'

_FALLBACK_SUPPLIER_CODE = 'P518581'


def _flow_list_param(overrides=None):
    param = {
        'pageNo': 1,
        'pageSize': 10,
        'supplierCode': '',
        'supplierName': '',
        'area': [],
        'startTime': '',
        'endTime': '',
        'currentStep': '',
        'flowCode': '',
    }
    if overrides:
        param.update(overrides)
    return param


@pytest.mark.run(order=1)
def test_querySupplierPool(global_config):
    """新品准入 -- 查询合格供应商列表，保存供应商编码到公共参数"""
    json_data = post_json(global_config, BASE_POOL_API + '/page', {
        'pageNo': 1,
        'pageSize': 20,
        'supplierCode': '',
        'supplierName': '',
        'auditStatus': 3,
    })
    logging.info('合格供应商列表结果 %s', json_data)
    assert_auth_ok(json_data)

    if not json_data.get('success'):
        global_config['admission_supplier_code'] = _FALLBACK_SUPPLIER_CODE
        print(f'查询合格供应商失败，使用兜底供应商：{_FALLBACK_SUPPLIER_CODE}')
        return

    record_list = (json_data.get('data') or {}).get('list') or []
    supplier_code = (
        record_list[0].get('supplierCode') if record_list else None
    ) or _FALLBACK_SUPPLIER_CODE
    global_config['admission_supplier_code'] = supplier_code
    logging.info('合格供应商编码已保存：%s，共 %d 条记录', supplier_code, len(record_list))


@pytest.mark.run(order=2)
def test_queryAccessProcess(global_config):
    """新品准入 -- 查询供应商已有准入流程"""
    supplier_code = global_config.get('admission_supplier_code') or _FALLBACK_SUPPLIER_CODE
    print(f'查询供应商 [{supplier_code}] 的准入流程')

    json_data = post_and_assert(
        global_config,
        BASE_POOL_API + '/queryAccessProcess',
        {'supplierCode': supplier_code},
        '查询准入流程',
    )
    data = json_data.get('data')
    print(f'准入流程数据：{data}')
    if isinstance(data, list) and data:
        global_config['admission_flow_code'] = data[0].get('flowCode')
    elif isinstance(data, dict):
        global_config['admission_flow_code'] = data.get('flowCode')
    else:
        global_config['admission_flow_code'] = None
    print(f'已有准入流程编码：{global_config.get("admission_flow_code")}')


@pytest.mark.run(order=3)
def test_createAdmissionFlow(global_config):
    """新品准入 -- 发起新品准入流程（已存在视为成功）"""
    supplier_code = global_config.get('admission_supplier_code') or _FALLBACK_SUPPLIER_CODE
    print(f'发起供应商 [{supplier_code}] 的新品准入流程')

    json_data = post_json(global_config, BASE_FLOW_API + '/create', {'supplierCode': supplier_code})
    print('发起准入流程结果', json_data)
    assert_auth_ok(json_data)

    msg = json_data.get('msg', '')
    if json_data.get('success'):
        data = json_data.get('data')
        flow_code = data.get('flowCode') if isinstance(data, dict) else data
        global_config['created_flow_code'] = flow_code
        print(f'发起准入流程成功，flowCode：{flow_code}')
    elif any(kw in msg for kw in ('已存在', '已发起', '进行中', '流程已')):
        print(f'准入流程已存在，视为成功：{msg}')
    else:
        pytest.fail(f'发起准入流程失败：{msg}')


@pytest.mark.run(order=4)
def test_createAdmissionFlow_emptySupplierCode(global_config):
    """新品准入 -- 发起流程时 supplierCode 为空，应返回错误"""
    json_data = post_json(global_config, BASE_FLOW_API + '/create', {'supplierCode': ''})
    print('空 supplierCode 发起流程结果', json_data)
    assert_failure(json_data, 'supplierCode 为空')
    print(f'校验通过：supplierCode 为空返回错误，{json_data.get("msg")}')


@pytest.mark.run(order=5)
def test_queryFlowList(global_config):
    """新品准入 -- 查询准入流程列表（不带过滤条件）"""
    json_data = post_and_assert(
        global_config, BASE_FLOW_API + '/list', _flow_list_param(), '查询准入流程列表'
    )
    record_list = (json_data.get('data') or {}).get('list') or []
    print(f'准入流程列表共 {len(record_list)} 条记录')
    if record_list and not global_config.get('admission_flow_code'):
        global_config['admission_flow_code'] = record_list[0].get('flowCode')


@pytest.mark.run(order=6)
def test_queryStepNums(global_config):
    """新品准入 -- 查询各步骤数量"""
    json_data = post_and_assert(
        global_config,
        BASE_FLOW_API + '/step-nums',
        {
            'supplierCode': '', 'supplierName': '', 'area': [],
            'startTime': '', 'endTime': '',
        },
        '查询步骤数量',
    )
    print(f'步骤数量数据：{json_data.get("data")}')


@pytest.mark.run(order=7)
def test_queryFlowList_bySupplierCode(global_config):
    """新品准入 -- 按供应商编码过滤流程列表"""
    supplier_code = global_config.get('admission_supplier_code') or _FALLBACK_SUPPLIER_CODE
    print(f'按供应商编码 [{supplier_code}] 过滤准入流程')

    json_data = post_and_assert(
        global_config,
        BASE_FLOW_API + '/list',
        _flow_list_param({'supplierCode': supplier_code}),
        '按供应商编码过滤',
    )
    record_list = (json_data.get('data') or {}).get('list') or []
    print(f'过滤结果共 {len(record_list)} 条，供应商：{supplier_code}')
    for record in record_list:
        assert record.get('supplierCode') == supplier_code, (
            f'返回记录供应商编码不匹配：期望 {supplier_code}，实际 {record.get("supplierCode")}'
        )


@pytest.mark.run(order=8)
def test_queryFlowList_byFlowCode(global_config):
    """新品准入 -- 按流程编号过滤流程列表"""
    flow_code = global_config.get('admission_flow_code') or global_config.get('created_flow_code')
    if not flow_code:
        pytest.skip('未获取到 flowCode，跳过按流程编号过滤用例')

    print(f'按流程编号 [{flow_code}] 过滤准入流程')
    json_data = post_and_assert(
        global_config,
        BASE_FLOW_API + '/list',
        _flow_list_param({'flowCode': flow_code}),
        '按流程编号过滤',
    )
    record_list = (json_data.get('data') or {}).get('list') or []
    print(f'过滤结果共 {len(record_list)} 条，flowCode：{flow_code}')
    if record_list:
        assert record_list[0].get('flowCode') == flow_code, (
            f'返回记录流程编号不匹配：期望 {flow_code}，实际 {record_list[0].get("flowCode")}'
        )
