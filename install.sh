#!/bin/bash

# 每日业务复盘Skill - 安装脚本
# 使用方法: bash install.sh

set -e

echo "🦞 每日业务复盘Skill - 安装向导"
echo "================================"
echo ""

# 检测OpenClaw安装路径
if [ -z "$OPENCLAW_HOME" ]; then
    OPENCLAW_HOME="$HOME/.openclaw"
fi

SKILL_DIR="$OPENCLAW_HOME/workspace/skills/daily-summary"

# 检查是否已安装
if [ -d "$SKILL_DIR" ]; then
    echo "⚠️  检测到已安装，是否重新安装？"
    read -p "   (y/n): " reinstall
    if [ "$reinstall" != "y" ]; then
        echo "❌ 安装已取消"
        exit 0
    fi
    echo "📦 备份旧配置..."
    [ -f "$SKILL_DIR/config.json" ] && cp "$SKILL_DIR/config.json" "$SKILL_DIR/config.json.backup"
fi

echo ""
echo "📋 配置向导"
echo "------------"

# 询问飞书配置
echo ""
echo "1️⃣  飞书应用配置"
echo "   请访问 https://open.feishu.cn/app 创建应用并获取凭证"
echo ""
read -p "   飞书 App ID: " FEISHU_APP_ID
read -p "   飞书 App Secret: " FEISHU_APP_SECRET
read -p "   飞书文档ID (从文档URL获取): " FEISHU_DOCUMENT_ID

# 询问定时任务配置
echo ""
echo "2️⃣  定时任务配置"
read -p "   执行时间 (默认 20:00, 格式: HH:MM): " SCHEDULE_TIME
SCHEDULE_TIME=${SCHEDULE_TIME:-20:00}
HOUR=$(echo $SCHEDULE_TIME | cut -d: -f1)
MINUTE=$(echo $SCHEDULE_TIME | cut -d: -f2)

# 询问通知配置
echo ""
echo "3️⃣  通知配置"
read -p "   是否发送完成通知？(y/n, 默认n): " SEND_NOTIFICATION
SEND_NOTIFICATION=${SEND_NOTIFICATION:-n}

if [ "$SEND_NOTIFICATION" = "y" ]; then
    read -p "   通知接收用户ID: " NOTIFICATION_USER
fi

echo ""
echo "🚀 开始安装..."
echo "------------"

# 创建目录
echo "📁 创建目录..."
mkdir -p "$SKILL_DIR"/{scripts,output,data,templates}

# 复制文件
echo "📦 复制文件..."
cp -r "$(dirname "$0")/scripts/"* "$SKILL_DIR/scripts/"
cp "$(dirname "$0")/SKILL.md" "$SKILL_DIR/"
cp "$(dirname "$0")/README.md" "$SKILL_DIR/"
cp "$(dirname "$0")/config.template.json" "$SKILL_DIR/"

# 创建.env文件
echo "⚙️  创建配置文件..."
cat > "$SKILL_DIR/.env" <<EOF
# 飞书应用配置
FEISHU_APP_ID=$FEISHU_APP_ID
FEISHU_APP_SECRET=$FEISHU_APP_SECRET
FEISHU_DOCUMENT_ID=$FEISHU_DOCUMENT_ID

# 通知配置
SEND_NOTIFICATION=$([ "$SEND_NOTIFICATION" = "y" ] && echo "true" || echo "false")
NOTIFICATION_USER=${NOTIFICATION_USER:-}
EOF

# 创建config.json
cat > "$SKILL_DIR/config.json" <<EOF
{
  "name": "daily-summary",
  "version": "1.0.0",
  "schedule": {
    "enabled": true,
    "cron": "$MINUTE $HOUR * * *",
    "timezone": "Asia/Shanghai"
  },
  "output": {
    "local_backup": true,
    "send_notification": $([ "$SEND_NOTIFICATION" = "y" ] && echo "true" || echo "false")
  }
}
EOF

# 设置权限
echo "🔐 设置权限..."
chmod +x "$SKILL_DIR/scripts/"*.py
chmod +x "$SKILL_DIR/scripts/"*.sh 2>/dev/null || true

# 安装Python依赖
echo "📦 安装Python依赖..."
pip install -q requests python-dateutil 2>/dev/null || pip3 install -q requests python-dateutil

# 创建定时任务
echo "⏰ 创建定时任务..."
(crontab -l 2>/dev/null | grep -v "daily_summary_to_feishu.py"; echo "$MINUTE $HOUR * * * cd $SKILL_DIR && python3 scripts/daily_summary_to_feishu.py >> logs/cron.log 2>&1") | crontab -

echo ""
echo "✅ 安装完成！"
echo "============"
echo ""
echo "📋 配置信息："
echo "   • 飞书文档ID: $FEISHU_DOCUMENT_ID"
echo "   • 定时执行: 每天 $SCHEDULE_TIME"
echo "   • 本地备份: $SKILL_DIR/output/"
echo ""
echo "📖 使用方法："
echo ""
echo "   # 手动运行"
echo "   python3 $SKILL_DIR/scripts/daily_summary_to_feishu.py"
echo ""
echo "   # 查看输出"
echo "   cat $SKILL_DIR/output/\$(date +%Y-%m-%d)_summary_detailed.json"
echo ""
echo "   # 查看飞书文档"
echo "   https://my.feishu.cn/wiki/$FEISHU_DOCUMENT_ID"
echo ""
echo "📝 下一步："
echo "   1. 确保飞书应用有文档写入权限"
echo "   2. 检查定时任务: crontab -l"
echo "   3. 明天 $SCHEDULE_TIME 自动执行第一次复盘"
echo ""
echo "📚 文档: $SKILL_DIR/README.md"
echo ""
