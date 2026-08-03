# *-*coding:utf-8 *-*
from datetime import datetime, timedelta
import time
import requests
import pytest
import json

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range

BASE = '/api/supplier-admin/supplier-admin/interior/productSource'

_WAREHOUSE_MODELS = [
    {"warehouseCode": "SHCK011", "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 0},
    {"warehouseCode": "CK009",   "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 1},
    {"warehouseCode": "SHCK012", "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 2},
    {"warehouseCode": "CK833",   "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 3},
    {"warehouseCode": "CK008",   "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 4},
    {"warehouseCode": "CK006",   "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 5},
    {"warehouseCode": "CK028",   "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 6},
    {"warehouseCode": "CK012",   "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 7},
    {"warehouseCode": "CK831",   "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 8},
    {"warehouseCode": "CK005",   "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 9},
    {"warehouseCode": "CK041",   "forbidStatus": 0, "autoPushDown": 0, "miniOrderNum": "1", "orderingCycle": "1", "materialLifeCycle": None, "idx": 10},
]

# 新增接口参数模板
def _build_save_param(overrides=None):
    today = datetime.now()
    param = {
        "type": "add",
        "diaTitle": "新增",
        "warehouseModels": _WAREHOUSE_MODELS,
        "saveWarehouseModels": _WAREHOUSE_MODELS,
        "shelfLifeUnit": "年",
        "forbidStatus": 0,
        "miniNum": 1,
        "shareLine": 0,
        "date": int(time.time() * 1000),
        "effectiveDate": today.strftime('%Y-%m-%d 00:00:00'),
        "expiryDate": (today + timedelta(days=3650)).strftime('%Y-%m-%d 23:59:59'),
        "labelId": None,
        "labelName": "",
        "materialCode": "1054711",
        "materialName": "小炒自助辣子测试空格",
        "specificationName": "1g/串*1串",
        "groupName": "锅圈小炒/小炒二级/小炒三级/小炒四级",
        "purchaseManager": "漫步者2",
        "purchaseSpecialist": "漫步者2",
        "purchaseUnitName": "5",
        "purchaseGroupName": "[\"火锅\",\"设施设备\"]",
        "caseBarCode": "111112211212",
        "bagBarCode": "null",
        "shelfLife": "111",
        "purchasePrice": None,
        "salePrice": 100,
        "supplierName": "aojo-test",
        "supplierCode": "P138131",
        "producerName": "test-001",
        "producerCode": "P514830"
    }
    if overrides:
        param.update(overrides)
    return param




# ──────────────────────────────────────────────
#  货源清单
# ──────────────────────────────────────────────

"货源清单--查询全量列表"
@pytest.mark.run(order=1)
def test_productSourceQueryPage(global_config):
    body = {
        "forbidStatus": None,
        "channelObj": {"supplierCode": ""},
        "producerObj": {"producerCode": ""},
        "releaseTime": [], "pageNo": 1, "pageSize": 10,
        "createDateEnd": "", "createDateStart": "",
        "forbidStatusList": [], "supplierCode": None,
        "producerCode": None,
        "auditStatusList": []   # 不限审核状态，查全量
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '货源清单-查询列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n货源清单总数: {total}')
        if records:
            r = records[0]
            print(f'产品编码：  {r.get("materialCode")}')
            print(f'产品名称：  {r.get("materialName")}')
            print(f'规格型号：  {r.get("specificationName")}')
            print(f'供应商：    {r.get("supplierName")}（{r.get("supplierCode")}）')
            print(f'厂家名称：  {r.get("producerName")}（{r.get("producerCode")}）')
            print(f'货源状态：  {r.get("forbidStatusCn")}')
            print(f'审核状态：  {r.get("auditStatusCn")}')
            print(f'创建人：    {r.get("createUser")}')
            print(f'创建日期：  {r.get("createDate")}')
            global_config['productSourceCode'] = r.get('code')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"货源清单--查询待审核列表"
@pytest.mark.run(order=2)
def test_productSourceQueryPending(global_config):
    body = {
        "forbidStatus": None,
        "channelObj": {"supplierCode": ""},
        "producerObj": {"producerCode": ""},
        "releaseTime": [], "pageNo": 1, "pageSize": 10,
        "createDateEnd": "", "createDateStart": "",
        "forbidStatusList": [], "supplierCode": None,
        "producerCode": None,
        "auditStatusList": [0]   # 0=待审核
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '货源清单-待审核列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n待审核货源清单总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"前置验证--确认 wangqin01 已绑定供应商渠道"
@pytest.mark.run(order=3)
def test_verifyUserBind(global_config):
    body = {"userNames": ["wangqin01"]}
    try:
        jd = parse_json(post_api(global_config, '/api/supplier-admin/supplier-admin/sso/user/bindAllChannel', body))
        assert_success(jd, '用户绑定供应商渠道')
        print('\nwangqin01 已绑定供应商渠道')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"货源清单--新增（完整参数，成功或已存在均视为通过）"
@pytest.mark.run(order=4)
def test_saveDetail_success(global_config):
    supplier_code = global_config.get('inserted_supplier_code') or 'P138131'
    supplier_name = global_config.get('inserted_supplier_name') or 'aojo-test'
    producer_code = global_config.get('inserted_producer_code') or 'P514830'
    producer_name = global_config.get('inserted_producer_name') or 'test-001'
    print(f'\n使用供应商：{supplier_name}（{supplier_code}），生产商：{producer_name}（{producer_code}）')

    param = _build_save_param(overrides={
        'supplierCode': supplier_code, 'supplierName': supplier_name,
        'producerCode': producer_code, 'producerName': producer_name,
    })
    try:
        jd = parse_json(post_api(global_config, BASE + '/saveDetail', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        msg = jd.get('msg', '')
        if jd.get('success'):
            print('新增成功')
        elif '已存在' in msg:
            print(f'记录已存在（视为通过）: {msg}')
        else:
            pytest.fail(f'新增失败：{msg}')

        # 新增成功或已存在，均反查获取 code（不限审核状态）供审核用例使用
        query_body = {
            "forbidStatus": None,
            "channelObj": {"supplierCode": supplier_code},
            "producerObj": {"producerCode": ""},
            "releaseTime": [], "pageNo": 1, "pageSize": 10,
            "createDateEnd": "", "createDateStart": "",
            "forbidStatusList": [], "supplierCode": supplier_code,
            "producerCode": None,
            "auditStatusList": []   # 不限审核状态
        }
        qjd = parse_json(post_api(global_config, BASE + '/queryPage', query_body))
        records = (qjd.get('data') or {}).get('list') or []
        if records:
            code = records[0].get('code')
            audit_status = records[0].get('auditStatusCn')
            global_config['productSourceCode'] = code
            global_config['productSourceAuditStatus'] = records[0].get('auditStatus')
            print(f'货源清单 code: {code}，当前审核状态: {audit_status}')
        else:
            print('未查询到货源清单记录')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"货源清单--新增（物料编码为空，应返回错误）"
@pytest.mark.run(order=5)
def test_saveDetail_emptyMaterial(global_config):
    param = _build_save_param(overrides={"materialCode": "", "materialName": ""})
    try:
        jd = parse_json(post_api(global_config, BASE + '/saveDetail', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), '物料编码为空时不应新增成功'
        print(f'\n校验通过：物料编码为空 → {jd.get("msg")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"货源清单--新增（供应商编码为空，应返回错误）"
@pytest.mark.run(order=6)
def test_saveDetail_emptySupplier(global_config):
    param = _build_save_param(overrides={"supplierCode": "", "supplierName": ""})
    try:
        jd = parse_json(post_api(global_config, BASE + '/saveDetail', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), '供应商编码为空时不应新增成功'
        print(f'\n校验通过：供应商编码为空 → {jd.get("msg")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"货源清单--新增（生产商编码为空，应返回错误）"
@pytest.mark.run(order=7)
def test_saveDetail_emptyProducer(global_config):
    param = _build_save_param(overrides={"producerCode": "", "producerName": ""})
    try:
        jd = parse_json(post_api(global_config, BASE + '/saveDetail', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), '生产商编码为空时不应新增成功'
        print(f'\n校验通过：生产商编码为空 → {jd.get("msg")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"货源清单--新增（仓库列表为空，应返回错误）"
@pytest.mark.run(order=8)
def test_saveDetail_emptyWarehouses(global_config):
    param = _build_save_param(overrides={"warehouseModels": [], "saveWarehouseModels": []})
    try:
        jd = parse_json(post_api(global_config, BASE + '/saveDetail', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), '仓库列表为空时不应新增成功'
        print(f'\n校验通过：仓库列表为空 → {jd.get("msg")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"货源清单--审核（待审核记录审核通过；已审核则跳过）"
@pytest.mark.run(order=9)
def test_auditDetail(global_config):
    code = global_config.get('productSourceCode')
    if not code:
        pytest.skip('未找到货源清单 code，跳过审核用例')

    audit_status = global_config.get('productSourceAuditStatus')
    if audit_status == 1:
        pytest.skip(f'货源清单（code={code}）已是已审核状态，无需重复审核')

    print(f'\n待审核 code：{code}')
    try:
        jd = parse_json(post_api(global_config, BASE + '/auditDetail', {"code": code, "auditStatus": 1}))
        assert_success(jd, '货源清单审核')
        print(f'审核通过 — code: {code}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))

