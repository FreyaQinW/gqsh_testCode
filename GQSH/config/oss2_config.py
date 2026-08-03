# *-*coding:utf-8 *-*
import os
from utils.csv_reader import load_csv_row

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CSV_PATH = os.path.join(_BASE_DIR, 'data', 'AuthorOSS2.csv')


class OSS2Config:
    """OSS2 运营后台系统配置"""

    @staticmethod
    def url() -> str:
        return 'https://test-oss2.zzgqsh.com'

    @staticmethod
    def credentials() -> dict:
        row = load_csv_row(_CSV_PATH)
        return {
            'username': row['username'],
            'password': row['password'],
        }
