#!/bin/bash
# 采购订单全链路自动化测试
# 顺序：申请10-40 → OSS2订单审核45-48 → SCMS确认发货50-100 → 发货查询110-130

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

VENV="$ROOT/.venv/bin/python"
if [ ! -x "$VENV" ]; then
  VENV="python3"
fi

if [ -f "$ROOT/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$ROOT/.env"
  set +a
fi

"$VENV" -m pytest \
  tests/api/supplierOss2/test_purchaseApplicationRecords.py \
  tests/api/supplierOss2/test_orderSearch.py \
  tests/api/scms/test_supplierOrder.py \
  tests/api/scms/test_deliveryManagement.py \
  -v --tb=short -s
