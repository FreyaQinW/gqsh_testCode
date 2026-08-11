#!/bin/bash
# 产品组合管理全链路自动化测试
# 执行顺序：采购SPU产品管理 → 商品售卖区域设置

VENV="$(dirname "$0")/.venv/bin/python"
cd "$(dirname "$0")"

# .venv 不可用时回退到系统 python3
if [ ! -x "$VENV" ]; then
  VENV="python3"
fi

$VENV -m pytest \
  tests/api/ProductOss2/ProductPortfolioManagement/test_PurChaseSpu.py \
  tests/api/ProductOss2/ProductPortfolioManagement/test_ProductSalesRegionSettings.py \
  -v --tb=short -s
