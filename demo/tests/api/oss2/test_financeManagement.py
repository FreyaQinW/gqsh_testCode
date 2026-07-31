# *-*coding:utf-8 *-*
import json
import pytest
import requests
from datetime import datetime, timedelta

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range

BASE = '/api/supplier-admin/supplier-admin/interior'
COMMON = '/api/supplier-admin/supplier-admin/common'







# ══════════════════════════════════════════════
#  一、财务总账
# ══════════════════════════════════════════════

@pytest.mark.run(order=1)
def test_accounting_queryPage(global_config):
    """XT账务管理--财务总账--查询列表"""
    start_m, end_m = year_range()
    body = {
        "orgId": "1",
        "channelObj": {"supplierId": ""},
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "statEndDate": end_m,
        "statStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accounting/queryPage', body))
        assert_success(jd, '财务总账-查询列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n财务总账总数: {total}')
        if records:
            r = records[0]
            print(f'  统计日期：  {r.get("statDate")}')
            print(f'  供应商编码：{r.get("supplierCode")}')
            print(f'  期初余额：  {r.get("initialBalance")}')
            print(f'  本期应付：  {r.get("currentPayable")}')
            print(f'  期末余额：  {r.get("endingBalance")}')
            print(f'  导入状态：  {r.get("importStatus")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=2)
def test_accounting_sumAmount(global_config):
    """XT账务管理--财务总账--查询金额汇总"""
    start_m, end_m = year_range()
    body = {
        "orgId": "1",
        "channelObj": {"supplierId": ""},
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "statEndDate": end_m,
        "statStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accounting/sumProvAccountingInfoModel', body))
        assert_success(jd, '财务总账-金额汇总')
        data = jd.get('data') or {}
        print(f'\n财务总账金额汇总:')
        print(f'  期初余额合计：{data.get("initialBalanceSum")}')
        print(f'  本期应付合计：{data.get("currentPayableSum")}')
        print(f'  本期已付合计：{data.get("currentPaidAmountSum")}')
        print(f'  采购退料合计：{data.get("refundAmountSum")}')
        print(f'  其他扣款合计：{data.get("otherDeductAmountSum")}')
        print(f'  期末余额合计：{data.get("endingBalanceSum")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ══════════════════════════════════════════════
#  三、财务明细
# ══════════════════════════════════════════════

@pytest.mark.run(order=3)
def test_accountingDetail_queryPage(global_config):
    """XT账务管理--财务明细--查询列表"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m,
        "warehouseCode": None,
        "businessTypes": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingDetail/queryPage', body))
        assert_success(jd, '财务明细-查询列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n财务明细总数: {total}')
        if records:
            r = records[0]
            print(f'  业务日期：{r.get("businessDate")}')
            print(f'  业务类型：{r.get("businessCn")}')
            print(f'  业务单号：{r.get("businessNo")}')
            print(f'  物料名称：{r.get("jindieMaterialName")}')
            print(f'  仓库名称：{r.get("jindieWarehouseName")}')
            print(f'  数量：    {r.get("num")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=4)
def test_accountingDetail_countInfo(global_config):
    """XT账务管理--财务明细--查询数量汇总"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m,
        "warehouseCode": None
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingDetail/countAccountingDetailInfo', body))
        assert_success(jd, '财务明细-数量汇总')
        data = jd.get('data') or []
        print(f'\n财务明细数量汇总:')
        for item in (data if isinstance(data, list) else []):
            print(f'  {item.get("businessTypeCn","全部")}：{item.get("total", 0)} 条')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=5)
def test_accountingDetail_sumAmount(global_config):
    """XT账务管理--财务明细--查询金额汇总"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m,
        "warehouseCode": None
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingDetail/sumAccountingDetailInfo', body))
        assert_success(jd, '财务明细-金额汇总')
        data = jd.get('data') or {}
        print(f'\n财务明细金额汇总:')
        print(f'  数量合计：    {data.get("numSum")}')
        print(f'  金额合计：    {data.get("totalAmountSum")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=6)
def test_accountingDetail_filterByType(global_config):
    """XT账务管理--财务明细--按业务类型筛选(采购入库)"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m,
        "warehouseCode": None,
        "businessTypes": [1]   # 1=采购入库 2=采购退料 3=检测费 4=扣罚款 5=客诉费 6=付款单
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingDetail/queryPage', body))
        assert_success(jd, '财务明细-采购入库筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n财务明细(采购入库)总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ══════════════════════════════════════════════
#  四、往来对账
# ══════════════════════════════════════════════

@pytest.mark.run(order=7)
def test_accountingStatement_queryPage(global_config):
    """XT账务管理--往来对账--查询列表"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "statEndDate": end_m,
        "statStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingStatement/queryPage', body))
        assert_success(jd, '往来对账-查询列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n往来对账总数: {total}')
        if records:
            r = records[0]
            print(f'  统计日期：{r.get("statDate")}')
            print(f'  渠道名称：{r.get("channelName")}')
            print(f'  生成状态：{r.get("generateStatusName")}')
            print(f'  推送状态：{r.get("pushStatus")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=8)
def test_accountingStatement_queryByYear(global_config):
    """XT账务管理--往来对账--按年度查询"""
    start_m, end_m = year_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "statEndDate": end_m,
        "statStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/accountingStatement/queryPage', body))
        assert_success(jd, '往来对账-年度查询')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n往来对账(年度)总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ══════════════════════════════════════════════
#  五、应付单列表
# ══════════════════════════════════════════════

@pytest.mark.run(order=9)
def test_payableOrder_markInvoiceStatusCount(global_config):
    """XT账务管理--应付单列表--查询开票状态数量"""
    start_d, end_d = day_range(33)
    body = {
        "orgId": "1",
        "releaseTime": [start_d, end_d],
        "releaseTime1": [],
        "pageNo": 1, "pageSize": 100,
        "payableEndDate": end_d,
        "payableStartDate": start_d
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/payableOrder/markInvoiceStatusCount', body))
        assert_success(jd, '应付单-开票状态数量')
        data = jd.get('data') or []
        print(f'\n应付单开票状态汇总:')
        for item in (data if isinstance(data, list) else []):
            print(f'  {item.get("markInvoiceStatusName","全部")}：{item.get("total", 0)} 条')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=10)
def test_payableOrder_queryPage(global_config):
    """XT账务管理--应付单列表--查询全量列表"""
    body = {
        "channelObj": {"supplierId": ""},
        "releaseTime": None,
        "pageNo": 1, "pageSize": 10,
        "adminPermissions": True
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/payableOrder/queryPage', body))
        assert_success(jd, '应付单-查询全量列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n应付单总数: {total}')
        if records:
            r = records[0]
            print(f'  金蝶订单号：{r.get("jindieOrderNo")}')
            print(f'  供应商名称：{r.get("supplierName")}')
            print(f'  物料名称：  {r.get("materialName")}')
            print(f'  应付日期：  {r.get("payableDate")}')
            print(f'  开票状态：  {r.get("markInvoiceStatusName")}')
            print(f'  开票金额：  {r.get("markInvoiceAmount")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=11)
def test_payableOrder_getStatistics(global_config):
    """XT账务管理--应付单列表--查询统计汇总"""
    body = {
        "channelObj": {"supplierId": ""},
        "releaseTime": None,
        "pageNo": 1, "pageSize": 10,
        "adminPermissions": True
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/payableOrder/getStatistics', body))
        assert_success(jd, '应付单-统计汇总')
        data = jd.get('data') or {}
        print(f'\n应付单统计汇总:')
        print(f'  数量合计：    {data.get("priceNumSum")}')
        print(f'  含税金额合计：{data.get("taxAmountSum")}')
        print(f'  不含税金额：  {data.get("unTaxAmountSum")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=12)
def test_payableOrder_queryByDate(global_config):
    """XT账务管理--应付单列表--按日期范围查询"""
    start_d, end_d = day_range(90)
    body = {
        "channelObj": {"supplierId": ""},
        "releaseTime": [start_d, end_d],
        "pageNo": 1, "pageSize": 10,
        "adminPermissions": True,
        "payableStartDate": start_d,
        "payableEndDate": end_d
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/payableOrder/queryPage', body))
        assert_success(jd, '应付单-日期筛选')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'\n应付单(近90天)总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ══════════════════════════════════════════════
#  六、付款申请
# ══════════════════════════════════════════════

@pytest.mark.run(order=13)
def test_payApply_selectCount(global_config):
    """XT账务管理--付款申请--查询状态数量汇总"""
    start_d, end_d = day_range(33)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "businessDate": "",
        "pageNo": 1, "pageSize": 100,
        "businessTypeList": None,
        "applyBeginDate": start_d,
        "applyEndDate": end_d,
        "channelCode": None
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/payApply/selectCountGroupByApplyNo', body))
        assert_success(jd, '付款申请-状态数量汇总')
        data = jd.get('data') or []
        print(f'\n付款申请状态汇总:')
        for item in (data if isinstance(data, list) else []):
            print(f'  {item.get("applyStatusName","全部")}：{item.get("total", 0)} 条')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=14)
def test_payApply_queryPage(global_config):
    """XT账务管理--付款申请--查询列表"""
    start_d, end_d = day_range(33)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "businessDate": "",
        "pageNo": 1, "pageSize": 10,
        "businessTypeList": None,
        "applyBeginDate": start_d,
        "applyEndDate": end_d,
        "channelCode": None,
        "applyStatusList": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/payApply/queryPageGroupByApplyNo', body))
        assert_success(jd, '付款申请-查询列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n付款申请总数: {total}')
        if records:
            r = records[0]
            print(f'  申请单号：{r.get("applyNo")}')
            print(f'  申请日期：{r.get("applyDate")}')
            print(f'  渠道名称：{r.get("channelName")}')
            print(f'  业务类型：{r.get("businessTypeCn")}')
            print(f'  申请状态：{r.get("applyStatus")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=15)
def test_payApply_sumAmount(global_config):
    """XT账务管理--付款申请--查询金额汇总"""
    start_d, end_d = day_range(33)
    body = {
        "orgId": "1",
        "channelObj": {"channelCode": ""},
        "releaseTime": [start_d, end_d],
        "businessDate": "",
        "pageNo": 1, "pageSize": 100,
        "businessTypeList": None,
        "applyBeginDate": start_d,
        "applyEndDate": end_d,
        "channelCode": None,
        "applyStatusList": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/payApply/sumGroupByApplyNo', body))
        assert_success(jd, '付款申请-金额汇总')
        data = jd.get('data') or {}
        print(f'\n付款申请金额汇总:')
        print(f'  申请总金额：    {data.get("totalAmountSum")}')
        print(f'  应付金额合计：  {data.get("totalPayableAmountSum")}')
        print(f'  已开票金额合计：{data.get("totalMarkInvoiceAmountSum")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ══════════════════════════════════════════════
#  八、应收账务
# ══════════════════════════════════════════════

@pytest.mark.run(order=16)
def test_receiveAccounting_queryPage(global_config):
    """XT账务管理--应收账务--查询列表"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/receiveAccounting/queryPage', body))
        assert_success(jd, '应收账务-查询列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n应收账务总数: {total}')
        if records:
            r = records[0]
            print(f'  统计日期：{r.get("statDate")}')
            print(f'  渠道名称：{r.get("channelName")}')
            print(f'  应收金额：{r.get("receivableAmount")}')
            print(f'  期初余额：{r.get("initialBalance")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=17)
def test_receiveAccounting_sumAmount(global_config):
    """XT账务管理--应收账务--查询金额汇总"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/receiveAccounting/sumProvReceiveAccountingInfo', body))
        assert_success(jd, '应收账务-金额汇总')
        data = jd.get('data') or {}
        print(f'\n应收账务金额汇总:')
        print(f'  应收金额合计：{data.get("receivableAmountSum")}')
        print(f'  期末余额合计：{data.get("endingBalanceSum")}')
        print(f'  普通扣款合计：{data.get("commonKsAmountSum")}')
        print(f'  特殊扣款合计：{data.get("specialKsAmountSum")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ══════════════════════════════════════════════
#  九、应收明细
# ══════════════════════════════════════════════

@pytest.mark.run(order=18)
def test_receiveAccountingDetail_countInfo(global_config):
    """XT账务管理--应收明细--查询数量汇总"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/receiveAccountingDetail/countReceiveAccountingDetail', body))
        assert_success(jd, '应收明细-数量汇总')
        data = jd.get('data') or []
        print(f'\n应收明细数量汇总:')
        for item in (data if isinstance(data, list) else []):
            print(f'  {item.get("businessName","全部")}：{item.get("total", 0)} 条')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=19)
def test_receiveAccountingDetail_queryPage(global_config):
    """XT账务管理--应收明细--查询列表"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m,
        "businessTypes": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/receiveAccountingDetail/queryPage', body))
        assert_success(jd, '应收明细-查询列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n应收明细总数: {total}')
        if records:
            r = records[0]
            print(f'  业务日期：{r.get("businessDate")}')
            print(f'  业务类型：{r.get("businessCn")}')
            print(f'  业务单号：{r.get("businessNo")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=20)
def test_receiveAccountingDetail_sumAmount(global_config):
    """XT账务管理--应收明细--查询金额汇总"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/receiveAccountingDetail/sumReceiveAccountingDetail', body))
        assert_success(jd, '应收明细-金额汇总')
        data = jd.get('data') or {}
        print(f'\n应收明细金额汇总:')
        print(f'  金额合计：{data.get("amountSum")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# ══════════════════════════════════════════════
#  十、应收收款
# ══════════════════════════════════════════════

@pytest.mark.run(order=21)
def test_receiveOrder_selectAccountConfig(global_config):
    """XT账务管理--应收收款--查询账户配置"""
    try:
        jd = parse_json(post_api(global_config, BASE + '/receiveOrder/selectAccountConfig', {}))
        assert_success(jd, '应收收款-账户配置')
        data = jd.get('data') or {}
        print(f'\n应收收款账户配置:')
        print(f'  账号列表：    {data.get("accountNoList")}')
        print(f'  付款日期配置：{data.get("payDateConfig")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=22)
def test_receiveOrder_countList(global_config):
    """XT账务管理--应收收款--查询数量汇总"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/receiveOrder/countReceiveOrderList', body))
        assert_success(jd, '应收收款-数量汇总')
        data = jd.get('data') or []
        print(f'\n应收收款数量汇总:')
        for item in (data if isinstance(data, list) else []):
            print(f'  {item.get("statusName","全部")}：{item.get("total", 0)} 条')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=23)
def test_receiveOrder_queryPage(global_config):
    """XT账务管理--应收收款--查询列表"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m,
        "businessTypes": []
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/receiveOrder/queryPageReceiveOrderList', body))
        assert_success(jd, '应收收款-查询列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        records = (jd.get('data') or {}).get('list') or []
        print(f'\n应收收款总数: {total}')
        if records:
            r = records[0]
            print(f'  收款单号：{r.get("businessNo")}')
            print(f'  业务日期：{r.get("businessDate")}')
            print(f'  业务类型：{r.get("businessCn")}')
        assert total >= 0
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=24)
def test_receiveOrder_sumAmount(global_config):
    """XT账务管理--应收收款--查询金额汇总"""
    start_m, end_m = month_range()
    body = {
        "orgId": "1",
        "releaseTime": [start_m, end_m],
        "pageNo": 1, "pageSize": 10,
        "businessEndDate": end_m,
        "businessStartDate": start_m
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/receiveOrder/sumReceiveOrderList', body))
        assert_success(jd, '应收收款-金额汇总')
        data = jd.get('data') or {}
        print(f'\n应收收款金额汇总: {data}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
