# *-*coding:utf-8 *-*
import requests
import pytest
import json

from utils.api_helper import post_api, get_api, parse_json, assert_success, month_range, year_range, day_range


BASE = '/api/supplier-admin/supplier-admin/supplier'





# ──────────────────────────────────────────────
#  厂家后补报告
# ──────────────────────────────────────────────

"发货管理--厂家后补报告--查询状态枚举"
@pytest.mark.run(order=1)
def test_producerReportStatusEnum(global_config):
    path = BASE + '/qualityscrm/common/enumlist?enumNames=ProducerReportStatusEnum'
    try:
        jd = parse_json(get_api(global_config, path))
        assert_success(jd, '厂家后补报告-状态枚举')
        print('厂家后补报告状态枚举:', jd.get('data'))
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


"发货管理--厂家后补报告--查询列表"
@pytest.mark.run(order=2)
def test_producerReportList(global_config):
    body = {"pageNo": 1, "pageSize": 10}
    try:
        jd = parse_json(post_api(global_config, BASE + '/producer/report/list', body))
        assert_success(jd, '厂家后补报告列表')
        total = (jd.get('data') or {}).get('totalCount', 0)
        print(f'厂家后补报告总数: {total}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))
