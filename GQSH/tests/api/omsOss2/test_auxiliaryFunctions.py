# *-*coding:utf-8 *-*
"""OMS 辅助功能 API 接口测试"""
import json

import pytest
import requests

from utils.api_helper import assert_oss2_success, first_oss2_list_item, parse_json, post_api

BASE = '/api/oms-admin/OmsErrorMessagePush'


@pytest.mark.run(order=1)
def test_OmsErrorMessagePush_operationLog(global_config):
    """辅助功能 - 异常报文-采购出库单"""
    body = {
        'outInType': '1',
        'page': 1,
        'limit': 10,
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/page', body))
        assert_oss2_success(jd, '异常报文列表')
        data = jd.get('data') or {}
        total = data.get('totalCount', 0)
        print(f'异常报文列表总数: {total}')
        items = data.get('list') or []
        if items:
            first = items[0]
            error_msg_id = first.get('id')
            if error_msg_id:
                global_config['omsErrorMessagePushId'] = error_msg_id
                print(f'异常报文ID: {error_msg_id}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


@pytest.mark.run(order=2)
def test_OmsErrorMessagePush(global_config):
    """辅助功能 - 异常报文-采购入库单"""
    body = {
        'outInType': '2',
        'page': 1,
        'limit': 10,
    }
    try:
        jd = parse_json(post_api(global_config, BASE + '/page', body))
        assert_oss2_success(jd, '采购入库单异常报文列表')
        data = jd.get('data') or {}
        total = data.get('totalCount', 0)
        print(f'采购入库单异常报文列表总数: {total}')
        items = data.get('list') or []
        if items:
            first = items[0]
            error_msg_id = first.get('id')
            if error_msg_id:
                global_config['omsErrorMessagePushId2'] = error_msg_id
                print(f'采购入库单异常报文ID: {error_msg_id}')
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        pytest.fail(str(e))


# @pytest.mark.run(order=2)
# def test_pushJD(global_config):
#     """辅助功能 - 异常报文推送金蝶"""
#     error_msg_id = global_config.get('omsErrorMessagePushId', '')
#     if not error_msg_id:
#         pytest.skip('无异常报文ID，跳过推送金蝶')
#     body = {
#         'id': error_msg_id,
#     }
#     try:
#         jd = parse_json(post_api(global_config, BASE + '/pushJd', body))
#         assert_oss2_success(jd, '异常报文推送金蝶')
#         print(f'推送金蝶响应: {jd}')
#     except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
#         pytest.fail(str(e))



