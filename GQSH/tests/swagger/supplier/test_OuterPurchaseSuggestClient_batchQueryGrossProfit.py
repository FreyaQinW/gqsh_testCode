# *-*coding:utf-8 *-*
"""智能补货采购建议 - 批量查询商品成本、效率、毛利、毛利率"""
import json

import pytest
import requests

from utils.api_helper import assert_success, parse_json

SWAGGER_PATH = '/supplier-center/h/com.guoquan.supplier.center.api.outer.purchasesuggest.OuterPurchaseSuggestClient'

'''
    毛利 ：（商品中心的售卖价格/(1+税率)-商品对应的加权平均成本)*时间区间涉及天数*MTD

    商品对应的加权平均成本：多个供应商存在一个品，取采购价目审核通过的值进行累加/供应商的数量

    毛利率：毛利/（商品中心的售卖价格/(1+税率)*天数*MTD）
'''
@pytest.mark.run(order=1)
def test_batchQueryGrossProfit(global_config):
    """智能补货采购建议 - 批量查询商品成本、效率、毛利、毛利率"""
    body = {
        'items': [
            {
                'materialCode': '1054101',
                'warehouseCode': 'SHCK011',
                'startTime': '2026-08-01 00:00:00',
                'endTime': '2026-08-31 23:59:59',
            }
        ],
    }
    try:
        url = global_config['test_URL'] + SWAGGER_PATH + '/batchQueryGrossProfit'
        print(f'请求URL: {url}')
        print(f'请求参数: {json.dumps(body, ensure_ascii=False)}')
        response = requests.post(
            url=url,
            data={'reqModel': json.dumps(body, ensure_ascii=False)},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=30,
            verify=True,
        )
        print(f'响应状态码: {response.status_code}')
        print(f'响应内容: {response.text}')
        jd = parse_json(response, '批量查询商品成本效率毛利毛利率')
        print(f'响应参数: {json.dumps(jd, ensure_ascii=False, indent=2)}')
    except requests.exceptions.RequestException as e:
        pytest.fail(f'网络请求失败: {e}')


OSS2_BASE = '/api/supplier-admin/supplier-admin/interior/purchasePriceChange'


@pytest.mark.run(order=2)
def test_queryPurchasePriceChange(global_config):
    """查询商品采购价目数据列表"""
    body = {
        'releaseTime': [],
        'releaseTime1': [],
        'releaseTime2': [],
        'channelObj': {'supplierCode': ''},
        'producerObj': {'producerCode': ''},
        'materialCode': '1054101',
        'pageNo': 1,
        'pageSize': 10,
        'createDateEnd': '',
        'createDateStart': '',
        'effectiveEndDate': '',
        'effectiveStartDate': '',
        'expireEndDate': '',
        'expireStartDate': '',
        'supplierCode': None,
        'auditStatus': [],
        'effectiveStatus': [],
    }
    try:
        url = global_config['oss2_URL'] + OSS2_BASE + '/queryPage'
        print(f'请求URL: {url}')
        response = requests.post(
            url=url,
            json=body,
            headers=global_config['header'],
            timeout=30,
            verify=True,
        )
        jd = parse_json(response, '商品采购价目数据列表')
        assert_success(jd, '商品采购价目数据列表')
        data = jd.get('data') or {}
        total = data.get('totalCount', 0)
        print(f'商品采购价目数据总数: {total}')
        records = data.get('list') or []
        if records:
            r = records[0]
            print(f'产品编码：  {r.get("materialCode")}')
            print(f'产品名称：  {r.get("materialName")}')
            print(f'供应商：    {r.get("supplierName")}')
            print(f'单价：      {r.get("price")}')
            print(f'税率：      {r.get("taxRate")}')
            print(f'含税单价：  {r.get("taxPrice")}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))



