# *-*coding:utf-8 *-*
import csv


def load_csv_data(file_path):
    """从CSV文件加载测试数据，返回第二行第一列的值"""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头
        second_row = next(reader)
        return second_row[0]


def load_csv_row(file_path):
    """从CSV文件加载第二行，返回字典（表头为key）"""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return next(reader)
