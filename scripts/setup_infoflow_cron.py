#!/usr/bin/env python3
"""
使用 OpenClaw infoflow_cron 设置每日总结定时任务
这种方式比系统 cron 更适合与如流集成
"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.expanduser("~/.openclaw/skills/daily-summary/scripts"))

def setup_infoflow_cron():
    """设置 infoflow 定时任务"""
    
    print("📝 设置每日业务总结定时任务（通过 infoflow_cron）")
    print("=" * 60)
    
    # 方案1: 每天 20:00 运行
    print("\n📅 推荐方案：")
    print("   执行时间: 每天 20:00")
    print("   执行命令: python3 ~/.openclaw/workspace/skills/daily-summary/scripts/daily_summary.py --verbose")
    print("")
    
    # 生成定时任务配置
    cron_config = {
        "name": "每日业务总结",
        "cron": "0 20 * * *",  # 每天 20:00
        "message": "📊 每日业务总结提醒\n\n请查看今天的业务总结报告：\n- 问题分析\n- 技术洞察\n- 行动建议\n\n运行命令查看详细报告：\n```bash\npython3 ~/.openclaw/workspace/skills/daily-summary/scripts/daily_summary.py\n```",
        "tz": "Asia/Shanghai"
    }
    
    print("💡 提示：")
    print("   由于当前环境支持 infoflow_cron 工具，")
    print("   您可以直接在对话中说：")
    print("")
    print("   '每天晚上8点提醒我做每日总结'")
    print("   或")
    print("   '创建定时任务，每天20:00运行 daily_summary.py'")
    print("")
    
    # 生成命令
    print("🔧 手动设置命令：")
    print("   在对话中告诉 AI：")
    print("   '创建定时任务：每天20:00运行以下命令：'")
    print(f"   python3 {os.path.expanduser('~/.openclaw/workspace/skills/daily-summary/scripts/daily_summary.py')}")
    print("")
    
    print("✅ 或者使用 OpenClaw CLI：")
    print(f"   openclaw cron create --name '每日总结' --cron '0 20 * * *' --command 'python3 {os.path.expanduser('~/.openclaw/workspace/skills/daily-summary/scripts/daily_summary.py')}'")
    print("")
    
    return 0

if __name__ == "__main__":
    sys.exit(setup_infoflow_cron())
