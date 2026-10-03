#!/bin/bash
# 福娃内容中台系统 - 一键安装脚本
set -e

echo "=========================================="
echo "  福娃内容中台系统 - 一键安装"
echo "=========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi
echo "✅ Python3: $(python3 --version)"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到pip3，请先安装pip"
    exit 1
fi
echo "✅ pip3: $(pip3 --version)"

# 进入后端目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../backend"

cd "$BACKEND_DIR"

# 创建虚拟环境（可选）
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo ""
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 创建必要目录
mkdir -p data uploads

# 初始化数据库
echo ""
echo "🗄️  初始化数据库..."
python -c "
from app.core.database import init_db
init_db()
print('✅ 数据库初始化完成')
"

echo ""
echo "=========================================="
echo "  ✅ 安装完成！"
echo "=========================================="
echo ""
echo "启动命令："
echo "  cd backend && source venv/bin/activate && python main.py"
echo ""
echo "或使用启动脚本："
echo "  bash scripts/start.sh"
echo ""
echo "访问地址："
echo "  前端: http://localhost:8080 (需单独启动)"
echo "  后端API: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
