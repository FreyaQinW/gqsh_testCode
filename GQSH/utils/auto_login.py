# *-*coding:utf-8 *-*
import base64
import csv
import json
import os
import time
import requests as _requests

from utils.credentials import load_oss2_credentials, load_scms_credentials

_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def get_oss2_token(username: str, password: str) -> str:
    """调用 SSO 登录接口获取 OSS2 token"""
    secret_info = base64.b64encode(
        json.dumps({
            'password': password,
            'account': username,
            'timestamp': int(time.time() * 1000)
        }).encode()
    ).decode()

    response = _requests.post(
        url='https://test-isigin.zzgqsh.com/api/sigin/auth/api/login',
        json={'secretInfo': secret_info},
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://test-oss2.zzgqsh.com',
            'Referer': 'https://test-oss2.zzgqsh.com/',
        },
        timeout=10
    )
    data = response.json()
    if not data.get('success') or not data.get('data'):
        raise RuntimeError(f'登录失败：{data}')

    return f"Bearer_{data['data']}"


def save_token(token: str, csv_path: str):
    """将 token 写入本地 CSV（已 gitignore，不入库）"""
    os.makedirs(os.path.dirname(csv_path) or '.', exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['token'])
        writer.writerow([token])


def refresh_oss2_token():
    """自动登录并刷新本地 data/Author.csv 中的 token"""
    creds = load_oss2_credentials()
    token = get_oss2_token(creds['username'], creds['password'])
    save_token(token, os.path.join(_DATA_DIR, 'Author.csv'))
    print('[auto_login] OSS2 token 已刷新')
    return token


def get_scms_token(username: str, password: str) -> str:
    """调用 SCMS 登录接口获取 token，返回 'scmsToken=xxx' 格式字符串"""
    response = _requests.post(
        url='https://test-scms.zzgqsh.com/api/supplier-admin/supplier-admin/supplier/sysUser/login',
        json={'name': username, 'password': password, 'agreePrivacy': True},
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://test-scms.zzgqsh.com',
            'Referer': 'https://test-scms.zzgqsh.com/',
        },
        timeout=10
    )
    data = response.json()
    if not data.get('success') or not data.get('data'):
        raise RuntimeError(f'SCMS 登录失败：{data}')
    token_value = data['data']['token']
    return f'scmsToken={token_value}'


def refresh_scms_token():
    """自动登录并刷新本地 data/AuthorSupplier.csv 中的 SCMS token"""
    creds = load_scms_credentials()
    token = get_scms_token(creds['username'], creds['password'])
    save_token(token, os.path.join(_DATA_DIR, 'AuthorSupplier.csv'))
    print('[auto_login] SCMS token 已刷新')
    return token
