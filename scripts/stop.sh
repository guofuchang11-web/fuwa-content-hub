#!/bin/bash
# 福娃内容中台系统 - 停止脚本
set -e

echo "🛑 停止福娃内容中台系统..."

# 停止后端
if pgrep -f "python main.py" > /dev/null; then
    pkill -f "python main.py"
    echo "✅ 后端服务已停止"
else
    echo "ℹ️  后端服务未运行"
fi

# 停止前端
if pgrep -f "http.server 8080" > /dev/null; then
    pkill -f "http.server 8080"
    echo "✅ 前端服务已停止"
else
    echo "ℹ️  前端服务未运行"
fi

echo ""
echo "✅ 所有服务已停止"
