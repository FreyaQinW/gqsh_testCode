# -*- coding: utf-8 -*-
"""OMS 设置 API 接口测试"""
import pytest

from utils.api_helper import first_oms_list_item, post_and_assert_oms, query_oms_list


@pytest.mark.oms
def test_settings_userList(global_config):
    """设置 - 查询用户列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/api/settings/user/page',
        {
            'username': '',
            'realName': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '设置用户列表',
        skip_if_empty=False,
    )


@pytest.mark.oms
def test_settings_roleList(global_config):
    """设置 - 查询角色列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/api/settings/role/page',
        {
            'roleName': '',
            'roleCode': '',
            'status': '',
            'page': 1,
            'limit': 10,
        },
        '设置角色列表',
        skip_if_empty=False,
    )


@pytest.mark.oms
def test_settings_dictList(global_config):
    """设置 - 查询数据字典列表"""
    query_oms_list(
        global_config,
        '/api/oms-admin/api/settings/dict/page',
        {
            'dictType': '',
            'dictName': '',
            'page': 1,
            'limit': 10,
        },
        '设置数据字典列表',
        skip_if_empty=False,
    )


@pytest.mark.oms
def test_settings_systemConfig(global_config):
    """设置 - 查询系统配置"""
    post_and_assert_oms(
        global_config,
        '/api/oms-admin/api/settings/systemConfig',
        {},
        '设置系统配置',
    )


@pytest.mark.oms
def test_settings_list(global_config):
    """设置 - 查询设置列表"""
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/settings/page',
        {
            'page': 1,
            'limit': 10,
        },
        '设置列表',
        skip_if_empty=True,
    )
    first = first_oms_list_item(json_data, '设置列表')
    settings_no = first.get('settingsNo')
    global_config['settingsNo'] = settings_no
    print(f'设置 settingsNo: {settings_no}')


@pytest.mark.oms
def test_settingsDetail(global_config):
    """设置 - 设置列表详情"""
    settings_no = global_config.get('settingsNo', '')
    json_data = query_oms_list(
        global_config,
        '/api/oms-admin/api/settings/page',
        {
            'settingsNo': settings_no,
            'page': 1,
            'limit': 10,
        },
        '设置详情',
        skip_if_empty=True,
    )
    print(f'设置详情接口查询结果: {json_data}')
