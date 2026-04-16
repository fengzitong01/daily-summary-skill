#!/bin/bash
# 设置每日总结定时任务

# 检查是否安装了 cron
if ! command -v crontab &> /dev/null; then
    echo "❌ 错误: cron 未安装"
    echo "请先安装 cron: sudo apt-get install cron"
    exit 1
fi

# 脚本路径
SCRIPT_PATH="/home/gem/.openclaw/workspace/skills/daily-summary/scripts/daily_summary.py"
PYTHON_PATH="/usr/bin/python3"

# 检查脚本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ 错误: 脚本不存在: $SCRIPT_PATH"
    exit 1
fi

# 检查 Python 是否存在
if [ ! -f "$PYTHON_PATH" ]; then
    echo "❌ 错误: Python 不存在: $PYTHON_PATH"
    exit 1
fi

# 创建 cron 任务（每天 20:00 运行）
CRON_JOB="0 20 * * * $PYTHON_PATH $SCRIPT_PATH --verbose >> /tmp/daily_summary.log 2>&1"

# 检查是否已存在相同的 cron 任务
if crontab -l | grep -q "daily_summary.py"; then
    echo "⚠️  警告: daily_summary 的 cron 任务已存在"
    echo "是否要更新？(y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        # 删除旧的 cron 任务
        crontab -l | grep -v "daily_summary.py" | crontab -
        echo "✅ 已删除旧的 cron 任务"
    else
        echo "❌ 取消操作"
        exit 0
    fi
fi

# 添加新的 cron 任务
(crontab -l; echo "$CRON_JOB") | crontab -

echo "✅ 定时任务创建成功！"
echo ""
echo "📋 配置信息:"
echo "   - 执行时间: 每天 20:00"
echo "   - 脚本路径: $SCRIPT_PATH"
echo "   - 日志文件: /tmp/daily_summary.log"
echo ""
echo "🔍 查看定时任务:"
echo "   crontab -l"
echo ""
echo "📄 查看执行日志:"
echo "   tail -f /tmp/daily_summary.log"
echo ""
echo "🗑️  删除定时任务:"
echo "   crontab -l | grep -v 'daily_summary.py' | crontab -"

exit 0
