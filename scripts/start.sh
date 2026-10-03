#!/bin/bash
# 福娃内容中台系统 - 启动脚本
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../backend"
LOG_FILE="/tmp/youguo-backend.log"

cd "$BACKEND_DIR"

# 检查是否已在运行
if pgrep -f "python main.py" > /dev/null; then
    echo "⚠️  后端服务已在运行中"
    echo "   日志: tail -f $LOG_FILE"
    echo "   停止: bash scripts/stop.sh"
    exit 0
fi

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 创建必要目录
mkdir -p data uploads

echo "🚀 启动福娃内容中台系统后端..."
echo "   日志文件: $LOG_FILE"

# 后台启动
nohup python main.py > "$LOG_FILE" 2>&1 &
PID=$!

echo "   进程PID: $PID"
echo ""

# 等待启动
sleep 3

# 检查健康状态
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 后端服务启动成功！"
    echo "   API地址: http://localhost:8000"
    echo "   API文档: http://localhost:8000/docs"
    echo "   健康检查: http://localhost:8000/health"
else
    echo "⚠️  服务可能还在启动中，请检查日志："
    echo "   tail -f $LOG_FILE"
fi

# 启动前端
echo ""
read -p "是否同时启动前端服务？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd "$SCRIPT_DIR/../assets"
    nohup python3 -m http.server 8080 > /tmp/youguo-frontend.log 2>&1 &
    echo "✅ 前端服务已启动: http://localhost:8080"
fi
