# 每日业务复盘 Skill

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

自动分析每日对话内容，生成结构化复盘报告并写入飞书文档的OpenClaw技能。

## ✨ 功能特性

- 📊 **智能分析** - 自动分析memory文件中的实际内容
- 📋 **结构化输出** - 按5大模块生成标准复盘报告
- 📄 **飞书集成** - 自动写入飞书文档，支持团队协作
- ⏰ **定时执行** - 每天自动运行，无需手动操作
- 🔄 **最新优先** - 新内容插入到文档最前面
- 💾 **本地备份** - 同时保存JSON格式到本地

## 🚀 快速开始

### 1. 安装

```bash
# 克隆仓库
cd ~/.openclaw/workspace/skills
git clone https://github.com/YOUR_USERNAME/daily-summary-skill.git daily-summary
cd daily-summary

# 运行安装脚本
bash install.sh
```

### 2. 配置飞书凭证

```bash
# 创建.env文件
cp .env.template .env

# 编辑.env文件，填入你的飞书凭证
nano .env
```

`.env` 文件内容：
```bash
# 飞书应用配置
FEISHU_APP_ID=cli_xxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxx
FEISHU_DOCUMENT_ID=xxxxxxxxxxxxxxxxxxxx

# 可选：通知配置
SEND_NOTIFICATION=false
NOTIFICATION_USER=your_user_id
```

### 3. 验证安装

```bash
# 手动运行测试
python3 scripts/daily_summary_to_feishu.py
```

## 📋 复盘内容结构

每份复盘报告包含：

1. **今日工作概览** - 主要完成任务
2. **关键业务洞察** - 方法论和认知突破  
3. **今日学习收获** - 技术技能和方法论掌握
4. **工作流程优化** - 流程改进建议
5. **明日计划** - 跟进工作和重点任务

## ⚙️ 配置说明

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
   - 从URL获取文档ID
   - 例如：`https://my.feishu.cn/wiki/MF2uwx2BziMGBekdIuJcq3Rsnnc` → `MF2uwx2BziMGBekdIuJcq3Rsnnc`

### 定时任务配置

默认每天20:00执行，可在安装时自定义：

```bash
# 安装时指定时间
bash install.sh
# 提示：执行时间 (默认 20:00, 格式: HH:MM): 21:00
```

## 📖 使用方法

### 手动运行

```bash
# 运行今日复盘
python3 scripts/daily_summary_to_feishu.py

# 查看输出
cat output/$(date +%Y-%m-%d)_summary_detailed.json
```

### 查看结果

- **飞书文档**: https://my.feishu.cn/wiki/YOUR_DOCUMENT_ID
- **本地备份**: `output/YYYY-MM-DD_summary_detailed.json`

### Memory文件规范

为了让复盘内容更丰富，建议在 `~/.openclaw/workspace/memory/YYYY-MM-DD.md` 中记录：

```markdown
# Memory - YYYY-MM-DD

## 📅 今日关键事件

### 任务1：项目名称
**时间**: 09:00 - 12:00
**工作内容**:
- 完成了XXX功能开发
- 解决了XXX问题

**关键洞察**:
- 洞察1
- 洞察2

## 💡 今日洞察
- 方法论总结
- 认知突破
```

## 🔧 故障排查

### 常见问题

1. **飞书API调用失败**
   ```
   检查项：
   - App ID 和 App Secret 是否正确
   - 应用是否有文档写入权限
   - 文档ID是否正确
   - 应用是否已发布
   ```

2. **定时任务未执行**
   ```bash
   # 检查cron服务
   service cron status
   
   # 检查任务列表
   crontab -l
   
   # 查看日志
   tail -f logs/cron.log
   ```

3. **复盘内容为空**
   ```
   检查项：
   - memory文件是否存在
   - memory文件格式是否正确
   - 是否有今日对话记录
   ```

## 📚 相关资源

- [OpenClaw 文档](https://docs.openclaw.ai)
- [飞书开放平台](https://open.feishu.cn)
- [Cron 表达式指南](https://crontab.guru)

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目基于 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

感谢所有为这个技能做出贡献的开发者！

---

**如果这个技能对你有帮助，请点个⭐️支持一下！**
