#!/bin/bash
# 采购订单全链路自动化测试
# 执行顺序：采购申请 → 采购订单 → 供应商发货 → 发货查询

''' 执行文件路径'''
#VENV="/Users/freya/supplierTest1224/SupplierCenter/.venv/bin/python"  绝对路径
#"$(dirname "$0")/.venv/bin/python"
#VENV="$(dirname "$0")/.venv/bin/python"  #自动检测文件路径


VENV="$(dirname "$0")/.venv/bin/python" # 相对路径



$VENV -m pytest \
  tests/api/oss2/test_purchaseApplicationRecords.py \
  tests/api/oss2/test_orderSearch.py \
  tests/api/scms/test_supplierOrder.py \
  tests/api/scms/test_deliveryManagement.py \
  -v --tb=short -s
