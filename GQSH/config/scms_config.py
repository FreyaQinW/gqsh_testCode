# *-*coding:utf-8 *-*
import os
from utils.csv_reader import load_csv_row

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CSV_PATH = os.path.join(_BASE_DIR, 'data', 'AuthorSCMS.csv')


class SCMSConfig:
    """SCMS 供应商端系统配置"""

    @staticmethod
    def url() -> str:
        return 'https://test-scms.zzgqsh.com'

    @staticmethod
    def credentials() -> dict:
        row = load_csv_row(_CSV_PATH)
        return {
            'username': row['username'],
            'password': row['password'],
        }
