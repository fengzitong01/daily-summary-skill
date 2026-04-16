#!/bin/bash
# 每日业务复盘定时任务调度器
# Daily Business Summary Scheduler

SCRIPT_PATH="/home/gem/.openclaw/workspace/skills/daily-summary/scripts/daily_summary_to_feishu.py"
LOG_FILE="/tmp/daily_summary_scheduler.log"
PID_FILE="/tmp/daily_summary_scheduler.pid"

# 记录日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查是否已经在运行
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        log "调度器已在运行 (PID: $OLD_PID)"
        exit 1
    else
        rm -f "$PID_FILE"
    fi
fi

# 保存PID
echo $$ > "$PID_FILE"

log "调度器启动 (PID: $$)"

# 主循环
while true; do
    # 获取当前时间
    CURRENT_HOUR=$(date '+%H')
    CURRENT_MINUTE=$(date '+%M')
    
    # 检查是否是20:00
    if [ "$CURRENT_HOUR" = "20" ] && [ "$CURRENT_MINUTE" = "00" ]; then
        log "执行每日业务复盘..."
        /usr/bin/python3 "$SCRIPT_PATH" >> "$LOG_FILE" 2>&1
        log "复盘完成"
        
        # 执行后等待1分钟，避免重复执行
        sleep 60
    fi
    
    # 每分钟检查一次
    sleep 60
done
