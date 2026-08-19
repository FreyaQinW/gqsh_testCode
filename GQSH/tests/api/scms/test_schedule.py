# *-*coding:utf-8 *-*
import json
import os

import pytest
import requests

from utils.api_helper import assert_success, day_range, get_jindie_order_no, parse_json, post_api

BASE = '/api/supplier-admin/supplier-admin/supplier/product/schedule'


"""排产管理--排产批次列表--分页查询"""
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


@pytest.mark.run(order=201)
def test_excelImport(global_config):
    """排产管理 - 生产排产Excel导入"""
    file_path = '/Users/a123456/Documents/需要导入的文件/协同scms/P170403生产排产导入20260819152040.xlsx'
    try:
        url = global_config['test_URL'] + BASE + '/excelImport'
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post(
                url=url,
                files=files,
                headers={k: v for k, v in global_config['header'].items() if k.lower() != 'content-type'},
                timeout=30,
                verify=True,
            )
        jd = parse_json(response, '生产排产Excel导入')
        assert_success(jd, '生产排产Excel导入')
        print(f'响应参数: {json.dumps(jd, ensure_ascii=False, indent=2)}')
    except FileNotFoundError:
        pytest.fail(f'导入文件不存在: {file_path}')
    except requests.exceptions.RequestException as e:
        pytest.fail(f'网络请求失败: {e}')
