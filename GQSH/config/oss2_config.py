# *-*coding:utf-8 *-*
import os

from utils.credentials import load_oss2_credentials


class OSS2Config:
    """OSS2 运营后台系统配置"""

    @staticmethod
    def url() -> str:
        return os.environ.get('OSS2_BASE_URL', 'https://test-oss2.zzgqsh.com').rstrip('/')

    @staticmethod
    def credentials() -> dict:
        return load_oss2_credentials()
