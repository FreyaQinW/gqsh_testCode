# *-*coding:utf-8 *-*
"""凭证加载：优先环境变量，其次本地 data/*.csv（均不入库）。"""
import os

from utils.csv_reader import load_csv_row

_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def _require_pair(username, password, *, env_user, env_pass, csv_name):
    if username and password:
        return {'username': username, 'password': password}
    raise RuntimeError(
        f'缺少登录凭证。请设置环境变量 {env_user}/{env_pass}，'
        f'或复制 data/{csv_name}.example 为 data/{csv_name} 后填写。'
    )


def load_oss2_credentials():
    """OSS2：OSS2_USERNAME/OSS2_PASSWORD → data/AuthorOSS2.csv"""
    username = os.environ.get('OSS2_USERNAME', '').strip()
    password = os.environ.get('OSS2_PASSWORD', '').strip()
    if username and password:
        return {'username': username, 'password': password}

    csv_path = os.path.join(_DATA_DIR, 'AuthorOSS2.csv')
    if os.path.isfile(csv_path):
        row = load_csv_row(csv_path)
        return _require_pair(
            (row.get('username') or '').strip(),
            (row.get('password') or '').strip(),
            env_user='OSS2_USERNAME',
            env_pass='OSS2_PASSWORD',
            csv_name='AuthorOSS2.csv',
        )
    return _require_pair(
        '',
        '',
        env_user='OSS2_USERNAME',
        env_pass='OSS2_PASSWORD',
        csv_name='AuthorOSS2.csv',
    )


def load_scms_credentials():
    """SCMS：SCMS_USERNAME/SCMS_PASSWORD → data/AuthorSCMS.csv"""
    username = os.environ.get('SCMS_USERNAME', '').strip()
    password = os.environ.get('SCMS_PASSWORD', '').strip()
    if username and password:
        return {'username': username, 'password': password}

    csv_path = os.path.join(_DATA_DIR, 'AuthorSCMS.csv')
    if os.path.isfile(csv_path):
        row = load_csv_row(csv_path)
        return _require_pair(
            (row.get('username') or '').strip(),
            (row.get('password') or '').strip(),
            env_user='SCMS_USERNAME',
            env_pass='SCMS_PASSWORD',
            csv_name='AuthorSCMS.csv',
        )
    return _require_pair(
        '',
        '',
        env_user='SCMS_USERNAME',
        env_pass='SCMS_PASSWORD',
        csv_name='AuthorSCMS.csv',
    )
