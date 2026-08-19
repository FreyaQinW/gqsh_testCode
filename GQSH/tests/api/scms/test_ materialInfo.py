# *-*coding:utf-8 *-*
"""原料库存、包材库存数据更新"""
import json
import os

import pytest
import requests

from utils.api_helper import assert_success, parse_json, post_api

BASE = '/api/supplier-admin/supplier-admin/supplier/materialDetail'


@pytest.mark.run(order=1)
def test_materialDetail_Type1(global_config):
    """原料库存页查询"""
    body = {
        'materialInfo': '',
        'type': 1,
        'pageNo': 1,
        'pageSize': 10,
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '原料库存分页查询')
        print(f'响应参数: {json.dumps(jd, ensure_ascii=False, indent=2)}')
        data = jd.get('data') or {}
        records = data.get('list') or []
        ids = [item.get('id') for item in records if item.get('id') is not None]
        if ids:
            global_config['materialDetailIds'] = ids
            print(f'原料库存ID列表: {ids}')
        else:
            pytest.skip('原料库存列表为空，跳过ID提取')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=2)
def test_materialDetail_Type2(global_config):
    """包材库存页查询"""
    body = {
        'materialInfo': '',
        'type': 2,
        'pageNo': 1,
        'pageSize': 10,
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/queryPage', body))
        assert_success(jd, '包材库存分页查询')
        print(f'响应参数: {json.dumps(jd, ensure_ascii=False, indent=2)}')
        data = jd.get('data') or {}
        records = data.get('list') or []
        ids = [item.get('id') for item in records if item.get('id') is not None]
        if ids:
            global_config['materialDetailIds2'] = ids
            print(f'包材库存ID列表: {ids}')
        else:
            pytest.skip('包材库存列表为空，跳过ID提取')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=3)
def test_delete(global_config):
    """批量删除原料库存"""
    ids = global_config.get('materialDetailIds', [])
    if not ids:
        pytest.skip('无原料库存ID列表，跳过批量删除')
    body = {
        'ids': ids,
        'type': 1,
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/delete', body))
        assert_success(jd, '批量删除原料库存')
        print(f'响应参数: {json.dumps(jd, ensure_ascii=False, indent=2)}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=4)
def test_delete1(global_config):
    """批量删除包材库存"""
    ids = global_config.get('materialDetailIds2', [])
    if not ids:
        pytest.skip('无包材库存ID列表，跳过批量删除')
    body = {
        'ids': ids,
        'type': 2,
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/delete', body))
        assert_success(jd, '批量删除包材库存')
        print(f'响应参数: {json.dumps(jd, ensure_ascii=False, indent=2)}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))

@pytest.mark.run(order=5)
def test_materialDetailLead(global_config):
    """导入原料库存、包材库存"""
    file_path = '/Users/a123456/Documents/需要导入的文件/协同scms/P170403原料_包材详情导入模板20260818103250.xlsx'
    try:
        url = global_config['test_URL'] + BASE + '/lead'
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = requests.post(
                url=url,
                files=files,
                headers={k: v for k, v in global_config['header'].items() if k.lower() != 'content-type'},
                timeout=30,
                verify=True,
            )
        jd = parse_json(response, '导入原料库存、包材库存')
        assert_success(jd, '导入原料库存、包材库存')
        print(f'响应参数: {json.dumps(jd, ensure_ascii=False, indent=2)}')
    except FileNotFoundError:
        pytest.fail(f'导入文件不存在: {file_path}')
    except requests.exceptions.RequestException as e:
        pytest.fail(f'网络请求失败: {e}')
