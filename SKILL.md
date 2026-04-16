# 每日业务复盘 Skill

## 描述
自动分析每日对话内容，生成结构化复盘报告并写入飞书文档。适合需要系统化记录工作内容、提炼业务洞察、追踪学习和成长轨迹的用户。

## 适用场景
- 系统化记录实习/工作期间的成长轨迹
- 从日常对话中提炼业务洞察和方法论
- 生成结构化报告用于周期性总结
- 追踪每日学习和工作进展

## 主要功能
1. **智能分析** - 自动分析memory文件中的实际内容
2. **结构化输出** - 按5大模块生成复盘报告
3. **飞书集成** - 自动写入指定飞书文档，支持团队协作
4. **定时执行** - 每天自动运行，无需手动操作
5. **最新优先** - 新内容插入到文档最前面
6. **本地备份** - 同时保存JSON格式到本地

## 快速开始

### 1. 安装
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/YOUR_USERNAME/daily-summary-skill.git daily-summary
cd daily-summary
bash install.sh
```

### 2. 配置飞书凭证
```bash
# 方法1: 设置环境变量
export FEISHU_APP_ID='your_app_id'
export FEISHU_APP_SECRET='your_app_secret'
export FEISHU_DOCUMENT_ID='your_document_id'

# 方法2: 创建.env文件
cp .env.template .env
# 编辑.env文件填入凭证
```

### 3. 运行测试
```bash
python3 scripts/daily_summary_to_feishu.py
```

## 配置说明

### 飞书应用配置

1. **创建飞书应用**
   - 访问 https://open.feishu.cn/app
   - 创建企业自建应用
   - 获取 App ID 和 App Secret

2. **配置权限**
   - 添加权限：`docx:document`（文档读写权限）
   - 发布应用并审核通过

3. **创建文档**
   - 新建飞书文档
   - 从URL中获取文档ID
   - 例如：`https://my.feishu.cn/wiki/MF2uwx2BziMGBekdIuJcq3Rsnnc` 中的 `MF2uwx2BziMGBekdIuJcq3Rsnnc`

### 定时任务配置

```json
{
  "schedule": {
    "enabled": true,
    "cron": "0 20 * * *",
    "timezone": "Asia/Shanghai"
  }
}
```

## 内容格式

### 复盘结构

每份复盘报告包含5大模块：

```
# YYYY-MM-DD

## 今日工作概览
### 主要完成任务
- 任务1及详情
- 任务2及详情

## 关键业务洞察
### 方法论总结
- 洞察1
- 洞察2

## 今日学习收获
### 技术技能
- 技能1
- 技能2

### 方法论掌握
- 方法1
- 方法2

## 工作流程优化
### 流程改进
- 改进1
- 改进2

## 明日计划
### 重点工作
- 计划1
- 计划2
```

### Memory文件规范

为了让复盘内容更丰富，建议在 `~/.openclaw/workspace/memory/YYYY-MM-DD.md` 中记录：

```markdown
# Memory - YYYY-MM-DD

## 📅 今日关键事件

### 任务1：项目名称
**时间**: 09:00 - 12:00
**工作内容**:
- 完成内容1
- 完成内容2

**关键洞察**:
- 洞察1
- 洞察2

## 💡 今日洞察
- 方法论总结
- 认知突破
```

## 高级功能

### 自定义插入位置

```json
{
  "content": {
    "insert_at_start": true
  }
}
```

- `true` - 最新内容插入到文档开头（推荐）
- `false` - 追加到文档末尾

### 通知配置

```json
{
  "output": {
    "send_notification": true,
    "notification_channel": "infoflow",
    "notification_user": "your_user_id"
  }
}
```

## 故障排查

### 问题：飞书API调用失败

**检查项**：
1. App ID 和 App Secret 是否正确
2. 应用是否有文档写入权限
3. 文档ID是否正确
4. 应用是否已发布

**解决方法**：
```bash
# 验证配置
python3 scripts/daily_summary_to_feishu.py --test
```

### 问题：复盘内容为空

**检查项**：
1. memory文件是否存在
2. memory文件格式是否正确
3. 是否有今日对话记录

**解决方法**：
```bash
# 检查memory文件
cat ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
```

### 问题：定时任务未执行

**检查项**：
```bash
# 查看定时任务
crontab -l

# 查看cron服务
service cron status

# 查看日志
tail -f logs/cron.log
```

## 文件结构

```
daily-summary/
├── SKILL.md                 # 本文档
├── README.md                # 使用说明
├── config.json              # 配置文件
├── config.template.json     # 配置模板
├── .env.template            # 环境变量模板
├── install.sh               # 安装脚本
├── scripts/
│   ├── daily_summary_to_feishu.py  # 主脚本
│   └── create_cron.sh              # 定时任务脚本
├── output/                  # 输出目录
│   └── YYYY-MM-DD_summary_detailed.json
├── templates/               # 模板目录
└── examples/                # 示例目录
```

## 最佳实践

1. **定时执行时间** - 建议设置在每天晚上（20:00-22:00）
2. **Memory记录** - 及时记录重要工作内容到memory文件
3. **定期归档** - 定期备份和归档复盘内容
4. **隐私保护** - 注意不要在memory中记录敏感信息

## 相关技能

- **HEARTBEAT** - 配合heartbeat定期检查复盘状态
- **Memory管理** - 规范化memory文件记录

## 更新日志

### v1.0.0 (2026-04-16)
- ✅ 初始版本发布
- ✅ 支持从memory文件解析内容
- ✅ 支持飞书文档集成
- ✅ 支持最新内容插入到开头
- ✅ 支持定时任务配置

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
