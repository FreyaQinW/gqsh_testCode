# *-*coding:utf-8 *-*
from datetime import datetime, timedelta
import requests
import pytest
import json

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range



BASE = '/api/supplier-admin/supplier-admin/supplier'
COMMON = '/api/supplier-admin/supplier-admin/common'




# ──────────────────────────────────────────────
#  厂商列表
# ──────────────────────────────────────────────

"基础资料--厂商列表--查询渠道枚举"
@pytest.mark.run(order=1)
def test_manufacturerChannelEnum(global_config):
    body = {"typeList": ["wx_msg_channel"]}
    try:
        jd = parse_json(post_api(global_config, COMMON + '/conditionsQuery/queryConditionListByType', body))
        assert_success(jd, '厂商列表-渠道枚举')
        print('渠道枚举:', list((jd.get('data') or {}).keys()))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--厂商列表--查询列表"
@pytest.mark.run(order=2)
def test_manufacturerQueryPage(global_config):
    body = {"pageNo": 1, "pageSize": 10}
    try:
        jd = parse_json(post_api(global_config, BASE + '/producer/queryPageProducerBindChannel', body))
        assert_success(jd, '厂商列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'厂商列表总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ──────────────────────────────────────────────
#  厂家物料列表
# ──────────────────────────────────────────────

"基础资料--厂家物料列表--查询仓库绑定状态枚举"
@pytest.mark.run(order=3)
def test_manufacturerMaterialEnum(global_config):
    body = {"typeList": ["bind_warehouse_status"]}
    try:
        jd = parse_json(post_api(global_config, COMMON + '/conditionsQuery/queryConditionListByType', body))
        assert_success(jd, '厂家物料-仓库状态枚举')
        print('仓库绑定状态枚举:', list((jd.get('data') or {}).keys()))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--厂家物料列表--查询列表"
@pytest.mark.run(order=4)
def test_manufacturerMaterialQueryPage(global_config):
    body = {
        "channelObj": {"supplierId": ""},
        "pageNo": 1, "pageSize": 10,
        "channelCode": None, "warehouseCode": None
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/producerChannelMaterial/queryPage', body))
        assert_success(jd, '厂家物料列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'厂家物料列表总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ──────────────────────────────────────────────
#  物料对照表
# ──────────────────────────────────────────────

"基础资料--物料对照表--查询审核状态枚举"
@pytest.mark.run(order=5)
def test_materialMappingEnum(global_config):
    body = {"typeList": ["account_audit_status"]}
    try:
        jd = parse_json(post_api(global_config, COMMON + '/conditionsQuery/queryConditionListByType', body))
        assert_success(jd, '物料对照表-审核状态枚举')
        print('审核状态枚举:', list((jd.get('data') or {}).keys()))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--物料对照表--查询列表"
@pytest.mark.run(order=6)
def test_materialContrastQueryPage(global_config):
    body = {
        "releaseTime": [],
        "pageNo": 1, "pageSize": 10,
        "updateTimeEnd": "", "updateTimeStart": ""
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/materialContrast/queryPage', body))
        assert_success(jd, '物料对照表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'物料对照表总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ──────────────────────────────────────────────
#  供应商资质
# ──────────────────────────────────────────────

"基础资料--供应商资质--查询资质类型枚举"
@pytest.mark.run(order=7)
def test_qualificationTypeEnum(global_config):
    body = {"typeList": ["supplier_qualification_type"]}
    try:
        jd = parse_json(post_api(global_config, COMMON + '/conditionsQuery/queryConditionListByType', body))
        assert_success(jd, '供应商资质-类型枚举')
        print('资质类型枚举:', list((jd.get('data') or {}).keys()))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--供应商资质--查询状态数量汇总"
@pytest.mark.run(order=8)
def test_qualificationSelectStatusCount(global_config):
    body = {
        "channelObj": {"channelCode": ""},
        "updateTime": [], "pageNo": 1, "pageSize": 10
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/qualification/selectStatusCount', body))
        assert_success(jd, '供应商资质-状态数量')
        print('资质状态数量:', jd.get('data'))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--供应商资质--查询列表"
@pytest.mark.run(order=9)
def test_qualificationQueryPage(global_config):
    body = {
        "channelObj": {"channelCode": ""},
        "updateTime": [], "pageNo": 1, "pageSize": 10, "statusList": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/qualification/queryPage', body))
        assert_success(jd, '供应商资质列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'供应商资质总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ──────────────────────────────────────────────
#  在线注册
# ──────────────────────────────────────────────

"基础资料--在线注册--查询供应商基础信息"
@pytest.mark.run(order=10)
def test_poolInfoQueryBase(global_config):
    try:
        jd = parse_json(post_api(global_config, BASE + '/pool/info/queryBase', {}))
        assert_success(jd, '在线注册-供应商基础信息')
        print('供应商基础信息:', jd.get('data'))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--在线注册--查询城市列表"
@pytest.mark.run(order=11)
def test_getAllCityList(global_config):
    body = {"businessType": "13", "channel": "5"}
    try:
        jd = parse_json(post_api(global_config, BASE + '/common/getAllCityList', body))
        assert_success(jd, '在线注册-城市列表')
        print(f'城市列表数量: {len(jd.get("data") or [])}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--在线注册--查询供应商行业类型"
@pytest.mark.run(order=12)
def test_getAllSupplierIndustry(global_config):
    try:
        jd = parse_json(post_api(global_config, BASE + '/pool/info/getAllSupplierIndustry', {}))
        assert_success(jd, '在线注册-行业类型')
        print(f'行业类型数量: {len(jd.get("data") or [])}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--在线注册--查询供应商性质"
@pytest.mark.run(order=13)
def test_getAllSupplierNature(global_config):
    try:
        jd = parse_json(post_api(global_config, BASE + '/pool/info/getAllSupplierNature', {}))
        assert_success(jd, '在线注册-供应商性质')
        print(f'供应商性质数量: {len(jd.get("data") or [])}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--在线注册--查询供应商产品类型"
@pytest.mark.run(order=14)
def test_getAllSupplierProductType(global_config):
    try:
        jd = parse_json(post_api(global_config, BASE + '/pool/info/getAllSupplierProductType', {}))
        assert_success(jd, '在线注册-产品类型')
        print(f'产品类型数量: {len(jd.get("data") or [])}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"基础资料--在线注册--查询供应商服务区域"
@pytest.mark.run(order=15)
def test_getAllSupplierServeArea(global_config):
    try:
        jd = parse_json(post_api(global_config, BASE + '/pool/info/getAllSupplierServeArea', {}))
        assert_success(jd, '在线注册-服务区域')
        print(f'服务区域数量: {len(jd.get("data") or [])}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ──────────────────────────────────────────────
#  审厂管理
# ──────────────────────────────────────────────

"基础资料--审厂管理--查询审厂结果列表"
@pytest.mark.run(order=16)
def test_auditFactoryQueryPage(global_config):
    start_d, end_d = day_range(30)
    body = {
        "releaseTime": [start_d, end_d],
        "pageNo": 1, "pageSize": 10,
        "auditTimeEnd": end_d,
        "auditTimeStart": start_d
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/quality/queryOfProducerAuditResultsPage', body))
        assert_success(jd, '审厂管理列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'审厂管理总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
