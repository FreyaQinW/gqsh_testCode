#!/bin/bash
# 供应商基础资料全链路自动化测试
# 执行顺序：新增供应商 → 供应商信息 → 新增生产商 → 货源清单 → 采购价目表

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
  tests/api/supplierOss2/test_supplierInfoQualified.py \
  tests/api/supplierOss2/test_supplierInfo.py \
  tests/api/supplierOss2/test_producer.py \
  tests/api/supplierOss2/test_productSource.py \
  tests/api/supplierOss2/test_purchasePrice.py \
  -v --tb=short -s
