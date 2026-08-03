# *-*coding:utf-8 *-*
import pytest

from utils.api_helper import parse_json, post_api

BASE_API = '/api/supplier-admin/supplier-admin/sso/user/bindAllChannel'


@pytest.mark.run(order=1)
def test_bindAllChannel_success(global_config):
    """运营门户用户绑定供应商渠道 -- 正常绑定有效用户"""
    json_data = parse_json(
        post_api(global_config, BASE_API, {'userNames': ['wangqin01']})
    )
    print('绑定结果', json_data)
    if json_data.get('code') == 401:
        pytest.fail('请重新登录')
    if not json_data.get('success'):
        pytest.fail(f"绑定失败：{json_data.get('msg', '未知错误')}")
    print('绑定成功')


@pytest.mark.run(order=2)
def test_bindAllChannel_emptyUserNames(global_config):
    """运营门户用户绑定供应商渠道 -- userNames 为空列表，应返回错误"""
    json_data = parse_json(post_api(global_config, BASE_API, {'userNames': []}))
    print('空用户名响应', json_data)
    if json_data.get('code') == 401:
        pytest.fail('请重新登录')
    if json_data.get('success'):
        pytest.fail('userNames 为空时不应绑定成功')
    print('校验通过：userNames 为空返回错误', json_data.get('msg'))


@pytest.mark.run(order=3)
def test_bindAllChannel_invalidUser(global_config):
    """运营门户用户绑定供应商渠道 -- 不存在的用户名，应返回错误"""
    json_data = parse_json(
        post_api(global_config, BASE_API, {'userNames': ['nonexistent_user_xxx']})
    )
    print('无效用户响应', json_data)
    if json_data.get('code') == 401:
        pytest.fail('请重新登录')
    if json_data.get('success'):
        pytest.fail('不存在的用户名不应绑定成功')
    print('校验通过：无效用户名返回错误', json_data.get('msg'))
