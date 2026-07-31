# *-*coding:utf-8 *-*
import os
from datetime import datetime

import pytest

from utils.api_helper import assert_auth_ok, assert_failure, post_and_assert, post_json

BASE_API = '/api/supplier-admin/supplier-admin/interior/producer'


def _build_insert_param(overrides=None):
    """构建新增生产商请求体"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]
    param = {
        'forbidStatus': 'A',
        'name': f'test-auto-{timestamp}',
        'areaCode': ['110000', '110100', '110101'],
        'address': '自动化测试地址',
        'qualityUserName': 'wangqin01',
        'qualityRealName': '王钦',
        'province': '110000',
        'city': '110100',
        'district': '110101',
    }
    if overrides is not None:
        param.update(overrides)
    return param


@pytest.mark.run(order=1)
def test_insertProducer_success(global_config):
    """生产商新增 -- 完整信息，应成功创建"""
    param = _build_insert_param()
    producer_name = param['name']
    json_data = post_and_assert(global_config, BASE_API + '/insertProducer', param, '生产商新增')
    print('新增结果', json_data)

    producer_code = json_data.get('data', {}).get('producerCode', '')
    global_config['inserted_producer_name'] = producer_name
    global_config['inserted_producer_code'] = producer_code
    os.environ['INSERTED_PRODUCER_CODE'] = producer_code or ''
    os.environ['INSERTED_PRODUCER_NAME'] = producer_name or ''
    print(f'新增成功 — 生产商名称：{producer_name}，生产商编码：{producer_code}')


@pytest.mark.run(order=2)
def test_insertProducer_emptyName(global_config):
    """生产商新增 -- 名称为空，应返回错误"""
    json_data = post_json(
        global_config, BASE_API + '/insertProducer', _build_insert_param(overrides={'name': ''})
    )
    print('空名称响应', json_data)
    assert_failure(json_data, '生产商名称为空')
    print('校验通过：名称为空返回错误', json_data.get('msg'))


@pytest.mark.run(order=3)
def test_insertProducer_emptyArea(global_config):
    """生产商新增 -- 地区信息为空，应返回错误"""
    json_data = post_json(
        global_config,
        BASE_API + '/insertProducer',
        _build_insert_param(overrides={
            'areaCode': [], 'province': '', 'city': '', 'district': '',
        }),
    )
    print('空地区响应', json_data)
    assert_failure(json_data, '地区信息为空')
    print('校验通过：地区为空返回错误', json_data.get('msg'))


@pytest.mark.run(order=4)
@pytest.mark.xfail(reason='系统Bug：接口未对质检员字段做必填校验，空值可新增成功', strict=False)
def test_insertProducer_emptyQualityUser(global_config):
    """生产商新增 -- 质检员为空，应返回错误"""
    json_data = post_json(
        global_config,
        BASE_API + '/insertProducer',
        _build_insert_param(overrides={'qualityUserName': '', 'qualityRealName': ''}),
    )
    print('空质检员响应', json_data)
    assert_failure(json_data, '质检员为空')
    print('校验通过：质检员为空返回错误', json_data.get('msg'))


@pytest.mark.run(order=5)
def test_insertProducer_emptyAddress(global_config):
    """生产商新增 -- 地址为空，应返回错误"""
    json_data = post_json(
        global_config,
        BASE_API + '/insertProducer',
        _build_insert_param(overrides={'address': ''}),
    )
    print('空地址响应', json_data)
    assert_failure(json_data, '地址为空')
    print('校验通过：地址为空返回错误', json_data.get('msg'))


@pytest.mark.run(order=6)
def test_producerAudit(global_config):
    """生产商审核 -- 审核通过 order=1 新增的生产商"""
    producer_code = global_config.get('inserted_producer_code')
    if not producer_code:
        pytest.skip('未找到 order=1 新增的生产商编码，跳过审核用例')

    print(f'待审核生产商编码：{producer_code}')
    post_and_assert(
        global_config,
        BASE_API + '/producerAudit',
        {'useOrgIds': ['1'], 'producerCode': producer_code},
        '生产商审核',
    )
    print(f'审核通过成功 — 生产商编码：{producer_code}')
