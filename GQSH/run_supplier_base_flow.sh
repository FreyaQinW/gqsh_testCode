#!/bin/bash
# 供应商基础资料全链路自动化测试
# 执行顺序：新增供应商 → 供应商信息 → 新增生产商 → 货源清单 → 采购价目表

VENV="/Users/freya/Desktop/code/demo/.venv/bin/python"
cd "$(dirname "$0")"

$VENV -m pytest \
  tests/api/oss2/test_supplierInfoQualified.py \
  tests/api/oss2/test_supplierInfo.py \
  tests/api/oss2/test_producer.py \
  tests/api/oss2/test_productSource.py \
  tests/api/oss2/test_purchasePrice.py \
  -v --tb=short -s
