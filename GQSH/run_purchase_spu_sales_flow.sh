#!/bin/bash
# 产品组合管理全链路自动化测试
# 执行顺序：采购SPU产品管理 → 商品售卖区域设置 → 云埔SKU

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

VENV="$ROOT/.venv/bin/python"
if [ ! -x "$VENV" ]; then
  VENV="python3"
fi

# 可选：从 .env 加载本地凭证（文件已 gitignore）
if [ -f "$ROOT/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$ROOT/.env"
  set +a
fi

"$VENV" -m pytest \
  tests/api/ProductOss2/ProductPortfolioManagement/test_PurChaseSpu.py \
  tests/api/ProductOss2/ProductPortfolioManagement/test_ProductSalesRegionSettings.py \
  tests/api/ProductOss2/ProductPortfolioManagement/test_productCloudSku_Old.py \
  -v --tb=short -s
