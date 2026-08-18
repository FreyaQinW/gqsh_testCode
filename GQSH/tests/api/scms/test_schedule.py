# *-*coding:utf-8 *-*
import json

import pytest
import requests

from utils.api_helper import assert_success, day_range, get_jindie_order_no, parse_json, post_api

BASE = '/api/supplier-admin/supplier-admin/supplier/product/schedule'


"排产管理--排产批次列表--分页查询"
@pytest.mark.run(order=200)
def test_pageScheduleAndBatch(global_config):
    body = {
        "limit": 10,
        "page": 1,
        "productNameCode": "",
        "supplierNameCode": "",
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/pageScheduleAndBatch', body))
        assert_success(jd, '排产批次列表')
        print(f'响应参数: {json.dumps(jd, ensure_ascii=False, indent=2)}')
        data = jd.get('data') or {}
        page_response = data.get('pageResponse') or {}
        total = page_response.get('totalCount', 0)
        print(f'排产批次列表总数: {total}')
        records = page_response.get('list') or []
        if records:
            first_code = records[0].get('code')
            global_config['scheduleCode'] = first_code
            print(f'第一条数据Code: {first_code}')
        else:
            pytest.skip('排产批次列表为空，跳过参数提取')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


