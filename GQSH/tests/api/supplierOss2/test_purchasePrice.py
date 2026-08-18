# *-*coding:utf-8 *-*
import json
import pytest
import requests
from datetime import datetime, timedelta

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range

BASE = '/api/supplier-admin/supplier-admin/interior/purchasePrice'




def _normalize_material_list(data):
    """将 queryMaterial 返回规范为 dict 列表（兼容 data 为 list / {list} / 纯编码字符串）。"""
    if isinstance(data, dict):
        raw = data.get('list') or data.get('records') or []
    else:
        raw = data or []
    if not isinstance(raw, list):
        return []

    materials = []
    for item in raw:
        if isinstance(item, dict):
            materials.append(item)
        elif isinstance(item, str) and item.strip():
            materials.append({'materialCode': item.strip(), 'unitList': []})
    return materials


def _iter_material_units(material):
    """产出 (material_dict, unit_dict)；无 unitList 时回退默认单位。"""
    if not isinstance(material, dict):
        return
    unit_list = material.get('unitList') or []
    if not unit_list:
        unit_list = [
            {'unitName': '56', 'unitCode': 'SPZXDWZ0329330'},
            {'unitName': '5', 'unitCode': 'SPZXDWZ0329331'},
        ]
    for unit in unit_list:
        if isinstance(unit, dict):
            yield material, unit
        elif isinstance(unit, str) and unit.strip():
            yield material, {'unitCode': unit.strip(), 'unitName': unit.strip()}


def _build_detail(global_config, overrides=None):
    """构建 detailReqs 单条明细，effectiveDate 动态取今天"""
    today = datetime.now()
    detail = {
        "materialCode":  global_config.get('purchase_material_code') or '1054711',
        "materialName":  global_config.get('purchase_material_name') or '小炒自助辣子测试空格',
        "specName":      global_config.get('purchase_spec_name')     or '1g/串*1串',
        "purchaseUnit":  global_config.get('purchase_unit')          or '5',
        "lifeCycle":     global_config.get('purchase_life_cycle')     or '',
        "productGroup":  global_config.get('purchase_product_group') or '锅圈小炒/小炒二级/小炒三级/小炒四级',
        "purchaseGroup": global_config.get('purchase_purchase_group') or '["火锅","设施设备"]',
        "currencyType":  "人民币",
        "unitList": global_config.get('purchase_unit_list') or [
            {"unitName": "56", "unitCode": "SPZXDWZ0329330"},
            {"unitName": "5",  "unitCode": "SPZXDWZ0329331"}
        ],
        "unitCode":       global_config.get('purchase_used_unit_code') or 'SPZXDWZ0329331',
        "unitName":       global_config.get('purchase_used_unit_name') or '5',
        "price":          "49.557522",
        "taxRate":        "13",
        "taxPrice":       "56",
        "downPrice":      "56",
        "upPrice":        "56",
        "priceCoefficient": 1,
        "remark":         None,
        "effectiveDate":  today.strftime('%Y-%m-%d 00:00:00'),           # 动态今天
        "expireDate":     (today + timedelta(days=3650)).strftime('%Y-%m-%d 23:59:59'),
    }
    if overrides:
        detail.update(overrides)
    return detail


def _build_param(global_config, overrides=None, detail_overrides=None):
    supplier_code = global_config.get('inserted_supplier_code') or 'P138131'
    param = {
        "orgId": "1",
        "supplierCode": supplier_code,
        "detailReqs": [_build_detail(global_config, detail_overrides)]
    }
    if overrides:
        param.update(overrides)
    return param


# ──────────────────────────────────────────────
#  采购价目表
# ──────────────────────────────────────────────

"采购价目表--查询全量列表"
@pytest.mark.run(order=1)
def test_queryPage(global_config):
    body = {
        "channelObj": {"supplierCode": ""},
        "producerObj": {"jindieProducerId": ""},
        "releaseTime": [], "pageNo": 1, "pageSize": 10,
        "createDateEnd": "", "createDateStart": "",
        "supplierCode": None, "auditStatus": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '采购价目表-查询全量')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n采购价目表总数: {total}')
        if records:
            r = records[0]
            print(f'产品编码：  {r.get("materialCode")}')
            print(f'产品名称：  {r.get("materialName")}')
            print(f'产品规格：  {r.get("specName")}')
            print(f'供应商：    {r.get("supplierName")}')
            print(f'单价：      {r.get("price")}')
            print(f'税率：      {r.get("tasRate")}')
            print(f'含税单价：  {r.get("taxPrice")}')
            print(f'禁用状态：  {r.get("forbidStatusAttr")}')
            print(f'所属组织：  {r.get("orgName")}')
            print(f'审核状态：  {r.get("auditStatusAttr")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--查询待审核列表"
@pytest.mark.run(order=2)
def test_queryPendingAudit(global_config):
    body = {
        "channelObj": {"supplierCode": ""},
        "producerObj": {"jindieProducerId": ""},
        "releaseTime": [], "pageNo": 1, "pageSize": 10,
        "createDateEnd": "", "createDateStart": "",
        "supplierCode": None, "auditStatus": [1]    # 1=待审核
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '采购价目表-待审核列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n待审核采购价目总数: {total}')
        if records:
            code = records[0].get('code')
            global_config['purchase_price_code'] = code
            print(f'第一条待审核 code: {code}')
            print(f'供应商：    {records[0].get("supplierName")}')
            print(f'产品编码：  {records[0].get("materialCode")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--查询已审核列表"
@pytest.mark.run(order=3)
def test_queryApprovedList(global_config):
    body = {
        "channelObj": {"supplierCode": ""},
        "producerObj": {"jindieProducerId": ""},
        "releaseTime": [], "pageNo": 1, "pageSize": 10,
        "createDateEnd": "", "createDateStart": "",
        "supplierCode": None, "auditStatus": [0]    # 0=已审核
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '采购价目表-已审核列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n已审核采购价目总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--查询供应商物料列表，保存到公共参数"
@pytest.mark.run(order=4)
def test_queryMaterial(global_config):
    supplier_code = global_config.get('inserted_supplier_code') or 'P138131'
    body = {"supplierCode": supplier_code, "sk": "", "pageNo": 1, "pageSize": 20}
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryMaterial', body))
        assert_success(jd, '采购价目表-查询物料')
        material_list = _normalize_material_list(jd.get('data'))
        print(f'\n供应商 [{supplier_code}] 物料数: {len(material_list)}')
        if material_list:
            sample = material_list[0]
            print(f'首条物料类型字段: materialCode={sample.get("materialCode")}, unitList={sample.get("unitList")}')
        if not material_list:
            pytest.skip(f'供应商 [{supplier_code}] 无可用物料，跳过后续新增用例')
        global_config['purchase_material_list'] = material_list
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--新增（完整参数，遍历物料找未添加的组合）"
@pytest.mark.run(order=5)
def test_savePurchasePrice_success(global_config):
    supplier_code = global_config.get('inserted_supplier_code') or 'P138131'
    material_list = global_config.get('purchase_material_list') or []
    if not material_list:
        pytest.skip('未查询到物料列表，跳过新增用例')

    for material in material_list:
        if not isinstance(material, dict):
            print(f'跳过非 dict 物料项: {material!r}')
            continue
        for material, unit in _iter_material_units(material):
            unit_list = material.get('unitList') or [unit]
            global_config.update({
                'purchase_material_code':   material.get('materialCode'),
                'purchase_material_name':   material.get('materialName'),
                'purchase_spec_name':       material.get('specName'),
                'purchase_unit':            material.get('purchaseUnit'),
                'purchase_life_cycle':      material.get('lifeCycle') or '',
                'purchase_product_group':   material.get('productGroup'),
                'purchase_purchase_group':  material.get('purchaseGroup'),
                'purchase_unit_list':       unit_list if isinstance(unit_list, list) else [unit],
                'purchase_used_unit_code':  unit.get('unitCode'),
                'purchase_used_unit_name':  unit.get('unitName'),
            })
            param = _build_param(global_config)
            try:
                jd = parse_json(post_api(global_config, BASE + '/savePurchasePrice', param))
                if jd.get('code') == 401:
                    pytest.fail('请重新登录')
                msg = jd.get('msg', '')
                if jd.get('success'):
                    print(
                        f'\n新增成功：materialCode={material.get("materialCode")} '
                        f'unitCode={unit.get("unitCode")} supplier={supplier_code}'
                    )
                    return
                elif '已添加' in msg or '已存在' in msg:
                    print(f'组合已存在，尝试下一个：{msg}')
                    continue
                else:
                    pytest.fail(f'采购价目表新增失败：{msg}')
            except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
                pytest.fail(str(e))

    pytest.skip('所有组合均已添加，无法测试新增')


"采购价目表--重复提交相同组合，应拒绝"
@pytest.mark.run(order=6)
def test_savePurchasePrice_duplicate(global_config):
    if not global_config.get('purchase_used_unit_code'):
        pytest.skip('order=5 未成功新增记录，跳过重复提交验证')
    param = _build_param(global_config)
    try:
        jd = parse_json(post_api(global_config, BASE + '/savePurchasePrice', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), '重复提交相同组合时不应新增成功'
        msg = jd.get('msg', '')
        assert '已添加' in msg or '已存在' in msg, f'重复提交应返回已存在，实际：{msg}'
        print(f'\n校验通过：重复提交被拒绝 → {msg}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--新增（orgId 为空，应返回错误）"
@pytest.mark.run(order=7)
def test_savePurchasePrice_emptyOrgId(global_config):
    param = _build_param(global_config, overrides={"orgId": ""})
    try:
        jd = parse_json(post_api(global_config, BASE + '/savePurchasePrice', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), 'orgId 为空时不应新增成功'
        print(f'\n校验通过：orgId 为空 → {jd.get("msg")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--新增（supplierCode 为空，应返回错误）"
@pytest.mark.run(order=8)
def test_savePurchasePrice_emptySupplierCode(global_config):
    param = _build_param(global_config, overrides={"supplierCode": ""})
    try:
        jd = parse_json(post_api(global_config, BASE + '/savePurchasePrice', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), 'supplierCode 为空时不应新增成功'
        print(f'\n校验通过：supplierCode 为空 → {jd.get("msg")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--新增（materialCode 为空，应返回错误）"
@pytest.mark.xfail(reason="系统Bug：materialCode 为空时后端未校验，新供应商可直接新增成功", strict=False)
@pytest.mark.run(order=9)
def test_savePurchasePrice_emptyMaterialCode(global_config):
    param = _build_param(global_config, detail_overrides={"materialCode": ""})
    try:
        jd = parse_json(post_api(global_config, BASE + '/savePurchasePrice', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), 'materialCode 为空时不应新增成功'
        print(f'\n校验通过：materialCode 为空 → {jd.get("msg")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--新增（price 为空，应返回错误）"
@pytest.mark.xfail(reason="系统Bug：price 为空时后端未校验，仍可新增成功", strict=False)
@pytest.mark.run(order=10)
def test_savePurchasePrice_emptyPrice(global_config):
    param = _build_param(global_config, detail_overrides={"price": ""})
    try:
        jd = parse_json(post_api(global_config, BASE + '/savePurchasePrice', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), 'price 为空时不应新增成功'
        print(f'\n校验通过：price 为空 → {jd.get("msg")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--新增（effectiveDate 为空，应返回错误）"
@pytest.mark.run(order=11)
def test_savePurchasePrice_emptyEffectiveDate(global_config):
    param = _build_param(global_config, detail_overrides={"effectiveDate": ""})
    try:
        jd = parse_json(post_api(global_config, BASE + '/savePurchasePrice', param))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        assert not jd.get('success'), 'effectiveDate 为空时不应新增成功'
        print(f'\n校验通过：effectiveDate 为空 → {jd.get("msg")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"采购价目表--批量审核待审核记录"
@pytest.mark.run(order=12)
def test_auditPurchasePrice(global_config):
    code = global_config.get('purchase_price_code')
    if not code:
        pytest.skip('未找到待审核采购价目 code，跳过审核用例')
    body = {"code": code}
    try:
        jd = parse_json(post_api(global_config, BASE + '/auditPurchasePrice', body))
        if jd.get('code') == 401:
            pytest.fail('请重新登录')
        # 审核成功或已审核均视为通过
        msg = jd.get('msg', '')
        if jd.get('success') or '已审核' in msg:
            print(f'\n审核通过 — code: {code}')
        else:
            pytest.fail(f'审核失败：{msg}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
