# *-*coding:utf-8 *-*
import os

from utils.credentials import load_scms_credentials


class SCMSConfig:
    """SCMS 供应商端系统配置"""

    @staticmethod
    def url() -> str:
        return os.environ.get('SCMS_BASE_URL', 'https://test-scms.zzgqsh.com').rstrip('/')

    @staticmethod
    def credentials() -> dict:
        return load_scms_credentials()
