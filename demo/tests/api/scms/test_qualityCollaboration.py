# *-*coding:utf-8 *-*
import pytest

from utils.api_helper import assert_success, day_range, get_api, month_range, parse_json, post_and_assert


# ──────────────────────────────────────────────
#  普通客诉
# ──────────────────────────────────────────────

@pytest.mark.run(order=1)
def test_normalComplainStatusList(global_config):
    """质量协同--普通客诉--查询状态汇总列表"""
    start_month, end_month = month_range()
    param = {
        'dutyType': 1,
        'bizMonth': [start_month, end_month],
        'pageNo': 1,
        'pageSize': 10,
        'beginAuditTime': '',
        'endAuditTime': '',
        'beginBizMonth': start_month,
        'endBizMonth': end_month,
        'statusList': [],
    }
    json_data = post_and_assert(
        global_config,
        '/api/supplier-admin/supplier-admin/supplier/normal/complain/status/list',
        param,
        '普通客诉状态汇总',
    )
    print('普通客诉状态汇总:', json_data.get('data'))


@pytest.mark.run(order=2)
def test_normalComplainList(global_config):
    """质量协同--普通客诉--查询列表"""
    start_month, end_month = month_range()
    param = {
        'dutyType': 1,
        'bizMonth': [start_month, end_month],
        'pageNo': 1,
        'pageSize': 10,
        'beginBizMonth': start_month,
        'endBizMonth': end_month,
        'statusList': [],
    }
    json_data = post_and_assert(
        global_config,
        '/api/supplier-admin/supplier-admin/supplier/normal/complain/list',
        param,
        '普通客诉列表',
    )
    total = json_data.get('data', {}).get('totalCount', 0)
    print(f'普通客诉列表总数: {total}')


# ──────────────────────────────────────────────
#  典型客诉
# ──────────────────────────────────────────────

@pytest.mark.run(order=3)
def test_typicalComplainEnumList(global_config):
    """质量协同--典型客诉--查询状态枚举"""
    path = (
        '/api/supplier-admin/supplier-admin/supplier/qualityscrm/common/enumlist'
        '?enumNames=TypicalComplainStatusEnum'
    )
    json_data = parse_json(get_api(global_config, path))
    assert_success(json_data, '典型客诉状态枚举')
    print('典型客诉状态枚举:', json_data.get('data'))


@pytest.mark.run(order=4)
def test_typicalComplainStatusList(global_config):
    """质量协同--典型客诉--查询状态汇总列表"""
    start_date, end_date = day_range(30)
    param = {
        'dutyType': 1,
        'bizDate': [start_date, end_date],
        'pageNo': 1,
        'pageSize': 10,
        'beginBizDate': start_date,
        'endBizDate': end_date,
    }
    json_data = post_and_assert(
        global_config,
        '/api/supplier-admin/supplier-admin/supplier/typical/complain/status/list',
        param,
        '典型客诉状态汇总',
    )
    print('典型客诉状态汇总:', json_data.get('data'))


@pytest.mark.run(order=5)
def test_typicalComplainList(global_config):
    """质量协同--典型客诉--查询列表"""
    start_date, end_date = day_range(30)
    param = {
        'dutyType': 1,
        'bizDate': [start_date, end_date],
        'pageNo': 1,
        'pageSize': 10,
        'beginBizDate': start_date,
        'endBizDate': end_date,
        'statusList': [],
    }
    json_data = post_and_assert(
        global_config,
        '/api/supplier-admin/supplier-admin/supplier/typical/complain/list',
        param,
        '典型客诉列表',
    )
    total = json_data.get('data', {}).get('totalCount', 0)
    print(f'典型客诉列表总数: {total}')


# ──────────────────────────────────────────────
#  产品拒收
# ──────────────────────────────────────────────

@pytest.mark.run(order=6)
def test_productRejectionStatusList(global_config):
    """质量协同--产品拒收--查询状态汇总列表"""
    json_data = post_and_assert(
        global_config,
        '/api/supplier-admin/supplier-admin/supplier/product/rejection/status/list',
        {},
        '产品拒收状态汇总',
    )
    print('产品拒收状态汇总:', json_data.get('data'))


@pytest.mark.run(order=7)
def test_productRejectionList(global_config):
    """质量协同--产品拒收--查询列表"""
    json_data = post_and_assert(
        global_config,
        '/api/supplier-admin/supplier-admin/supplier/product/rejection/list',
        {'pageNo': 1, 'pageSize': 10},
        '产品拒收列表',
    )
    total = json_data.get('data', {}).get('totalCount', 0)
    print(f'产品拒收列表总数: {total}')


# ──────────────────────────────────────────────
#  质量事故
# ──────────────────────────────────────────────

@pytest.mark.run(order=8)
def test_qualityAccidentStatusList(global_config):
    """质量协同--质量事故--查询状态汇总列表"""
    param = {'statusList': [2, 3, 4, 5]}
    json_data = post_and_assert(
        global_config,
        '/api/supplier-admin/supplier-admin/supplier/quality/accident/status/list',
        param,
        '质量事故状态汇总',
    )
    print('质量事故状态汇总:', json_data.get('data'))


@pytest.mark.run(order=9)
def test_qualityAccidentList(global_config):
    """质量协同--质量事故--查询列表"""
    param = {'statusList': [2, 3, 4, 5]}
    json_data = post_and_assert(
        global_config,
        '/api/supplier-admin/supplier-admin/supplier/quality/accident/list',
        param,
        '质量事故列表',
    )
    total = json_data.get('data', {}).get('totalCount', 0)
    print(f'质量事故列表总数: {total}')
