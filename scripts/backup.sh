#!/bin/bash
# 福娃内容中台系统 - 数据备份脚本
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/../backend"
BACKUP_DIR="$SCRIPT_DIR/../backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "💾 福娃内容中台系统 - 数据备份"
echo "   备份时间: $(date)"
echo "   备份目录: $BACKUP_DIR"
echo ""

# 备份数据库
if [ -f "$BACKEND_DIR/data/content_hub.db" ]; then
    cp "$BACKEND_DIR/data/content_hub.db" "$BACKUP_DIR/content_hub_$DATE.db"
    echo "✅ 数据库已备份: content_hub_$DATE.db"
else
    echo "ℹ️  数据库文件不存在，跳过"
fi

# 备份上传文件
if [ -d "$BACKEND_DIR/uploads" ] && [ "$(ls -A $BACKEND_DIR/uploads 2>/dev/null)" ]; then
    tar -czf "$BACKUP_DIR/uploads_$DATE.tar.gz" -C "$BACKEND_DIR" uploads/
    echo "✅ 上传文件已备份: uploads_$DATE.tar.gz"
else
    echo "ℹ️  上传目录为空，跳过"
fi

# 打包完整备份
echo ""
echo "📦 创建完整备份包..."
tar -czf "$BACKUP_DIR/youguo_backup_$DATE.tar.gz" \
    -C "$BACKUP_DIR" \
    data/ \
    uploads/ \
    2>/dev/null || true

echo "✅ 完整备份: youguo_backup_$DATE.tar.gz"

# 显示备份文件大小
echo ""
echo "📊 备份文件大小:"
du -sh "$BACKUP_DIR"/*_$DATE* 2>/dev/null || true

# 清理旧备份（保留最近10个）
echo ""
echo "🗑️  清理旧备份（保留最近10个）..."
ls -t "$BACKUP_DIR"/youguo_backup_*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm -f
ls -t "$BACKUP_DIR"/content_hub_*.db 2>/dev/null | tail -n +11 | xargs -r rm -f
ls -t "$BACKUP_DIR"/uploads_*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm -f

echo ""
echo "✅ 备份完成！"
echo "   备份目录: $BACKUP_DIR"
