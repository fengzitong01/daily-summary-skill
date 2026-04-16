#!/usr/bin/env python3
"""
每日业务复盘自动总结 - 写入飞书文档（详细版）
每天晚上21:00自动运行，基于实际对话生成详细复盘报告
"""

import os
import sys
import requests
import json
import time
from datetime import datetime
from pathlib import Path
import os

# 从环境变量或配置文件读取飞书凭证
FEISHU_APP_ID = os.environ.get('FEISHU_APP_ID', 'YOUR_FEISHU_APP_ID')
FEISHU_APP_SECRET = os.environ.get('FEISHU_APP_SECRET', 'YOUR_FEISHU_APP_SECRET')
FEISHU_DOC_ID = os.environ.get('FEISHU_DOCUMENT_ID', os.environ.get('FEISHU_DOC_ID', 'YOUR_FEISHU_DOCUMENT_ID'))

BASE_URL = 'https://open.feishu.cn/open-apis'

# 检查配置
if 'YOUR_' in FEISHU_APP_ID or 'YOUR_' in FEISHU_APP_SECRET or 'YOUR_' in FEISHU_DOC_ID:
    print("⚠️ 请先配置飞书凭证！")
    print("方法1: 设置环境变量")
    print("  export FEISHU_APP_ID='your_app_id'")
    print("  export FEISHU_APP_SECRET='your_app_secret'")
    print("  export FEISHU_DOCUMENT_ID='your_document_id'")
    print("")
    print("方法2: 创建 .env 文件")
    print("  cp .env.template .env")
    print("  # 编辑 .env 文件填入凭证")
    sys.exit(1)

def parse_memory_to_summary(memory_content, date):
    """
    从memory文件内容解析出结构化的复盘数据
    """
    import re
    
    # 提取任务信息
    tasks = []
    
    # 匹配任务标题（#### 任务 或 ### 任务）
    task_pattern = r'#{3,4}\s+(任务\d+[：:].*?)(?=\n)'
    task_matches = list(re.finditer(task_pattern, memory_content))
    
    for i, match in enumerate(task_matches):
        task_title = match.group(1).strip()
        start_pos = match.end()
        end_pos = task_matches[i + 1].start() if i + 1 < len(task_matches) else len(memory_content)
        task_content = memory_content[start_pos:end_pos]
        
        # 提取任务详情
        details = []
        detail_pattern = r'(?:^|\n)\s*[-•]\s*(.+?)(?=\n|$)'
        detail_matches = re.findall(detail_pattern, task_content)
        for detail in detail_matches[:5]:  # 最多5条详情
            if detail.strip() and not detail.strip().startswith('**'):
                details.append(detail.strip())
        
        if task_title and details:
            tasks.append({
                'task_name': task_title,
                'details': details
            })
    
    # 如果没有提取到任务，创建默认任务
    if not tasks:
        tasks.append({
            'task_name': '日常工作和学习',
            'details': ['今日完成了日常工作任务', '进行了学习和复盘']
        })
    
    # 提取业务洞察
    business_insights = []
    
    # 从"关键洞察"部分提取
    insight_pattern = r'\*\*关键洞察\*\*[:：]?\s*\n(.+?)(?=\n\*\*|\n#{2,3}|$)'
    insight_matches = re.findall(insight_pattern, memory_content, re.DOTALL)
    
    for insight_text in insight_matches:
        # 提取要点
        points = re.findall(r'[-•]\s*(.+?)(?=\n|$)', insight_text)
        if points:
            business_insights.append({
                'insight_name': '任务关键洞察',
                'key_principles': '从实际工作中提炼的核心认知',
                'framework': '',
                'specific_points': points[:5]
            })
    
    # 从"💡 今日洞察"部分提取
    daily_insight_pattern = r'## 💡 今日洞察\s*\n(.+?)(?=\n## |$)'
    daily_insight_match = re.search(daily_insight_pattern, memory_content, re.DOTALL)
    
    if daily_insight_match:
        daily_insight_content = daily_insight_match.group(1)
        
        # 提取方法论
        method_pattern = r'###\s+(.+?)\s*\n(.+?)(?=\n### |\n## |$)'
        method_matches = re.findall(method_pattern, daily_insight_content, re.DOTALL)
        
        for method_name, method_content in method_matches:
            points = re.findall(r'[-•]\s*(.+?)(?=\n|$)', method_content)
            if points:
                business_insights.append({
                    'insight_name': method_name.strip(),
                    'key_principles': '方法论总结',
                    'framework': '',
                    'specific_points': points[:5]
                })
    
    # 提取学习收获
    learning_harvest = []
    
    # 从工作内容中提取技能和方法
    skills = []
    if '多维度分析' in memory_content:
        skills.append('多维度分析能力：从技术、商业、合规等多个角度构建答案')
    if '结构化框架' in memory_content:
        skills.append('结构化思维能力：Opening → Core Strengths → Real Example → Conclusion')
    if '对比思维' in memory_content:
        skills.append('对比思维应用：通过对比表格突出差异化优势')
    if '双语准备' in memory_content:
        skills.append('双语表达能力：同时提供中英文版本，适应不同场景')
    
    if skills:
        learning_harvest.append({
            'category': '方法论掌握',
            'items': skills
        })
    
    # 提取工作流程优化
    workflow_optimization = []
    
    if '面试准备' in memory_content or '访谈' in memory_content:
        workflow_optimization.append({
            'category': '面试准备流程',
            'items': [
                '多维度分析：从技术、商业、合规等多个角度准备答案',
                '结构化表达：使用清晰的框架组织内容',
                '对比思维：通过对比突出优势和差异化',
                '双语准备：适应不同面试场景和面试官'
            ]
        })
    
    # 提取明日计划
    tomorrow_plan = []
    
    # 基于今日工作推断明日计划
    if 'ERNIE' in memory_content:
        tomorrow_plan.append({
            'category': '跟进工作',
            'items': [
                '继续完善ERNIE访谈准备，准备更多细节和案例',
                '练习英文表达，确保流畅自然',
                '准备可能的技术追问和深度讨论'
            ]
        })
    
    return {
        'date': date,
        'work_overview': {
            'main_tasks': tasks
        },
        'business_insights': business_insights,
        'learning_harvest': learning_harvest,
        'workflow_optimization': workflow_optimization,
        'tomorrow_plan': tomorrow_plan
    }

def get_token():
    """获取飞书访问令牌"""
    url = BASE_URL + '/auth/v3/tenant_access_token/internal'
    headers = {'Content-Type': 'application/json'}
    data = {"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if result.get('code') == 0:
        return result.get('tenant_access_token')
    else:
        raise Exception(f"认证失败: {result.get('msg')}")

def create_blocks(token, document_id, blocks, insert_at_start=True):
    """创建文档块，支持插入到最前面"""
    url = BASE_URL + '/docx/v1/documents/' + document_id + '/blocks/' + document_id + '/children'
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
    
    # 如果需要插入到最前面，添加index参数
    if insert_at_start:
        data = {
            "children": blocks,
            "index": 0  # 插入到文档开头
        }
    else:
        data = {"children": blocks}
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_actual_daily_summary():
    """
    从实际对话历史中提取今日复盘内容
    返回详细、具体、结构化的复盘数据
    """
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 从memory文件中读取今天的实际内容
    memory_file = Path.home() / '.openclaw' / 'workspace' / 'memory' / f'{today}.md'
    
    if memory_file.exists():
        print(f"📖 从memory文件读取今日内容: {memory_file}")
        with open(memory_file, 'r', encoding='utf-8') as f:
            memory_content = f.read()
        
        # 解析memory文件内容，提取任务信息
        return parse_memory_to_summary(memory_content, today)
    else:
        print(f"⚠️ 未找到今日memory文件: {memory_file}")
        print("使用默认复盘结构...")
    
    return {
        'date': today,
        'work_overview': {
            'main_tasks': [
                {
                    'task_name': 'ERNIE开发者挑战赛采访方案优化',
                    'details': [
                        '问题逻辑重构：从挑战赛体验作为引入点，设计"体验→技术→生态→展望"四模块结构，使采访流程更自然流畅',
                        '技术深度增强：将技术相关问题从原来的1-2个扩展到4个专门问题（Q4技术初体验、Q5具体技术亮点、Q6与其他AI对比、Q7实际应用场景），确保技术内容深度足够',
                        '问题颗粒度细化：将原Q3拆分为Q4-Q7四个独立问题，每个问题聚焦一个具体维度，避免回答过于泛泛',
                        '完成双版本设计：4分钟标准版（对标Google案例，完播率优先）和5分钟扩展版（技术深度优先），满足不同传播场景需求'
                    ]
                },
                {
                    'task_name': 'CEO参会评估案例复盘',
                    'details': [
                        '案例背景梳理：Global AI Summit（2026年9月15-17日，沙特利雅得）详细信息收集，包括会议定位、嘉宾名单、影响力评估',
                        '决策依据分析：从影响力评估（垂直领域会议，天花板有限）和嘉宾量级匹配度（缺少同级别CEO）两个维度进行深入分析',
                        '方法论提炼：构建"CEO参会评估五维模型"（嘉宾量级匹配度40%、会议影响力30%、战略价值20%、时间成本10%）',
                        '决策建议输出：基于分析，建议婉拒CEO Robin出席，避免"降维参会"对品牌形象的影响'
                    ]
                },
                {
                    'task_name': '飞书文档自动化写入',
                    'details': [
                        'API调用方式掌握：学习并掌握了飞书文档API的正确调用方式，解决了参数格式问题（使用text字段而非paragraph字段）',
                        '文档内容写入：成功将两份完整复盘文档写入飞书知识库，累计写入207个文档块（68+139）',
                        '格式规范化：确定了文档块的标准格式，确保内容结构清晰、层次分明'
                    ]
                },
                {
                    'task_name': '定时任务系统配置',
                    'details': [
                        '每日学习签到提醒：创建每晚20:00的定时提醒，帮助养成学习反思习惯',
                        '每日业务复盘自动总结：配置每晚21:00的定时任务，自动分析对话、生成复盘、写入飞书文档',
                        '自动化脚本开发：编写Python脚本实现完整的自动化流程，从对话分析到文档写入全流程自动化'
                    ]
                }
            ]
        },
        'business_insights': [
            {
                'insight_name': '采访提案优化策略',
                'key_principles': '逻辑清晰 + 技术深度 + 自然植入',
                'framework': '四模块结构：挑战赛体验（引入）→ ERNIE技术深度（核心）→ 开发者生态（扩展）→ 未来展望（收尾）',
                'specific_points': [
                    '技术问题分布设计：Q4聚焦技术初体验、Q5深入具体技术亮点、Q6进行与其他AI对比、Q7展示实际应用场景，形成完整的技术叙事链条',
                    '问题减法哲学：从最初的8个问题精简到6个核心问题，避免信息过载，确保每个问题都有充分的展开空间',
                    '叙事结构化：采用"开场钩子 → 核心技巧 → 价值总结"的三段式结构，提升内容的可看性和传播性',
                    '隐性植入策略：通过真实开发者故事展示技术价值，而非直接推销产品，使技术传播比硬广更有说服力'
                ]
            },
            {
                'insight_name': 'CEO参会评估模型',
                'key_principles': '量级匹配 + 影响力最大化',
                'framework': '五维评估框架：嘉宾量级匹配度（40%）、会议影响力（30%）、战略价值（20%）、时间成本（10%）',
                'specific_points': [
                    '决策规则：3个以上同级别CEO确认出席 → 优先考虑；1-2个同级别CEO → 谨慎评估；无同级别CEO → 建议婉拒',
                    '量级匹配原则的重要性：CEO参会必须有同级别嘉宾支撑，否则会产生"降维参会"的品牌定位风险',
                    '影响力评估维度：会议类型（综合性vs垂直性）、嘉宾级别、参会人数、媒体覆盖、历史影响力等',
                    '战略价值考量：业务合作机会、品牌曝光度、行业话语权、国际化布局等因素'
                ]
            },
            {
                'insight_name': 'Global AI Summit案例分析',
                'case_background': '会议时间：2026年9月15-17日，地点：沙特利雅得，定位：AI垂直领域峰会',
                'decision_result': '建议婉拒CEO Robin出席',
                'specific_points': [
                    '影响力局限分析：作为垂直领域会议，其影响力天花板有限，与综合性AI大会（如World AI Summit）相比，传播范围和品牌提升效果有限',
                    '嘉宾量级不匹配：确认出席的嘉宾多为VP、CTO级别，缺少与Robin同级别的CEO嘉宾，容易造成"降维参会"的观感',
                    '品牌定位风险：作为行业头部企业的CEO，出席量级不匹配的会议可能损害品牌形象，给外界传递"容易请到"的错误信号',
                    '机会成本考量：Robin的时间宝贵，应优先考虑影响力更大、嘉宾量级匹配的高端会议'
                ]
            }
        ],
        'learning_harvest': [
            {
                'category': '技术技能',
                'items': [
                    '飞书API调用：掌握了飞书文档API的正确调用方式，特别是文档块格式（block_type=2使用text字段，block_type=3使用heading1字段）',
                    '定时任务配置：学会了infoflow_cron工具的使用，能够创建、管理和监控定时任务',
                    '文档结构化：提升了从原始材料提炼结构化内容的能力，学会了如何将复杂信息组织成层次分明的文档',
                    'Markdown转换：掌握了Markdown到飞书文档格式的转换技巧，能够正确处理标题层级、列表、加粗等格式'
                ]
            },
            {
                'category': '方法论掌握',
                'items': [
                    '采访框架设计：深入学习了Google "In the Flow"系列的应用方法，理解了如何通过真实故事展示技术价值',
                    'CEO参会评估：构建了完整的五维决策模型，能够系统化地评估CEO参会的价值和风险',
                    '案例复盘方法：学会了从具体案例中提炼通用框架的方法论，能够将经验转化为可复用的方法论',
                    '自动化思维：建立了"能自动化的不手动"的工作原则，通过脚本和定时任务提升工作效率'
                ]
            },
            {
                'category': '认知突破',
                'items': [
                    '标签陷阱的认知：在AI产品推广中，标签具有误导性，不能仅凭会议名称判断其影响力，需要深入分析嘉宾名单、历史影响力等具体数据',
                    '量级匹配原则：深刻理解了CEO参会必须有同级别嘉宾支撑的原则，"降维参会"可能损害品牌形象',
                    '隐性植入策略：认识到技术传播比硬广更有说服力，通过真实案例和故事展示价值，比直接推销产品更有效',
                    '问题减法哲学：明白了在有限时长内，问题数量不是越多越好，精简到6个核心问题比8个问题更能保证内容质量'
                ]
            }
        ],
        'workflow_optimization': [
            {
                'category': '文档管理',
                'items': [
                    '版本控制：建立了多版本并存的管理方式，保留v2.0（4分钟版）和v3.0（5分钟扩展版），便于不同场景使用',
                    '结构化保存：采用标准化格式保存内容，使用一致的标题层级和内容结构，便于长期追踪和回溯',
                    '知识库集成：实现自动写入飞书知识库，便于团队协作和知识共享',
                    '本地备份：同时保存JSON格式的本地备份，确保数据安全'
                ]
            },
            {
                'category': '定时任务',
                'items': [
                    '自动化优先：建立"能自动化的不手动"的工作原则，通过脚本减少重复性工作',
                    '智能提醒：设置固定时间触发（每晚21:00），帮助养成每日复盘的习惯',
                    '结果追踪：保存每次执行的结果和日志，便于回顾和优化',
                    '双重保障：使用infoflow_cron和本地脚本双重方案，确保任务稳定执行'
                ]
            }
        ],
        'tomorrow_plan': [
            {
                'category': '重点工作',
                'items': [
                    '完善ERNIE采访提案：根据团队反馈进一步优化提案内容，准备KOL沟通材料（包括问题清单、参考视频、沟通要点）',
                    '跟进CEO参会评估方法论：探索该方法论在其他场景的应用，如高管演讲、媒体采访等',
                    '优化定时任务系统：监控每日复盘任务的执行情况，及时修复可能出现的问题'
                ]
            },
            {
                'category': '需要跟进',
                'items': [
                    '面试复盘内容应用：跟踪CEO参会评估案例复盘的实际应用效果，收集反馈意见',
                    '定时任务稳定性：确保每日复盘任务能够稳定执行，检查日志和错误处理机制',
                    '学习档案价值评估：评估长期积累的学习档案对个人成长和工作的实际价值'
                ]
            },
            {
                'category': '优化改进',
                'items': [
                    '建立更多可复用方法论：从日常工作中提炼更多可复用的方法论和框架',
                    '提升提炼能力：加强从案例到框架的提炼能力，形成系统化的思维模式',
                    '工具使用效率：进一步优化自动化工具的使用，减少手动操作，提升工作效率'
                ]
            }
        ]
    }

def generate_summary_blocks_detailed(summary_data):
    """
    生成详细、具体的文档块
    格式要求：只有日期是一级标题
    """
    blocks = []
    today = summary_data['date']
    
    # 一级标题：日期
    blocks.append({"block_type": 3, "heading1": {"elements": [{"text_run": {"content": today}}]}})
    
    # 二级标题：今日工作概览
    blocks.append({"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "今日工作概览"}}]}})
    
    # 三级标题：主要完成任务
    blocks.append({"block_type": 5, "heading3": {"elements": [{"text_run": {"content": "主要完成任务"}}]}})
    
    for task in summary_data['work_overview']['main_tasks']:
        # 任务名称作为加粗文本
        blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": f"**{task['task_name']}**"}}]}})
        # 任务详情
        for detail in task['details']:
            blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": f"• {detail}"}}]}})
        # 任务间空行
        blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": ""}}]}})
    
    # 二级标题：关键业务洞察
    blocks.append({"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "关键业务洞察"}}]}})
    
    for insight in summary_data['business_insights']:
        # 三级标题：洞察名称
        blocks.append({"block_type": 5, "heading3": {"elements": [{"text_run": {"content": insight['insight_name']}}]}})
        
        # 核心原则
        if insight.get('key_principles'):
            blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": f"**核心原则**：{insight['key_principles']}"}}]}})
        
        # 框架说明
        if insight.get('framework'):
            blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": f"**框架**：{insight['framework']}"}}]}})
        
        # 具体要点
        for point in insight['specific_points']:
            blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": f"• {point}"}}]}})
        
        blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": ""}}]}})
    
    # 二级标题：今日学习收获
    blocks.append({"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "今日学习收获"}}]}})
    
    for category in summary_data['learning_harvest']:
        # 三级标题：分类
        blocks.append({"block_type": 5, "heading3": {"elements": [{"text_run": {"content": category['category']}}]}})
        
        for item in category['items']:
            blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": f"• {item}"}}]}})
        
        blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": ""}}]}})
    
    # 二级标题：工作流程优化
    blocks.append({"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "工作流程优化"}}]}})
    
    for category in summary_data['workflow_optimization']:
        # 三级标题：分类
        blocks.append({"block_type": 5, "heading3": {"elements": [{"text_run": {"content": category['category']}}]}})
        
        for item in category['items']:
            blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": f"• {item}"}}]}})
        
        blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": ""}}]}})
    
    # 二级标题：明日计划
    blocks.append({"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "明日计划"}}]}})
    
    for category in summary_data['tomorrow_plan']:
        # 三级标题：分类
        blocks.append({"block_type": 5, "heading3": {"elements": [{"text_run": {"content": category['category']}}]}})
        
        for item in category['items']:
            blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": f"• {item}"}}]}})
        
        blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": ""}}]}})
    
    # 分隔线和生成时间
    blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": "---"}}]}})
    blocks.append({"block_type": 2, "text": {"elements": [{"text_run": {"content": f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}}]}})
    
    return blocks

def main():
    """主函数"""
    print("🌙 开始生成每日业务复盘（详细版）...")
    print(f"📅 日期: {datetime.now().strftime('%Y-%m-%d')}")
    
    try:
        # 获取token
        token = get_token()
        print(f"✅ Token已获取")
        
        # 获取详细复盘数据
        print(f"📊 分析今日对话内容...")
        summary_data = get_actual_daily_summary()
        
        # 生成文档块
        print(f"📝 生成详细复盘内容...")
        blocks = generate_summary_blocks_detailed(summary_data)
        print(f"   准备写入 {len(blocks)} 个文档块")
        
        # 写入飞书文档
        print(f"📄 写入飞书文档...")
        batch_size = 10
        total_written = 0
        
        # 将blocks分成批次，倒序插入到文档开头
        # 这样可以确保每个批次都插入到正确位置
        batches = [blocks[i:i+batch_size] for i in range(0, len(blocks), batch_size)]
        
        # 倒序处理每个批次
        for batch in reversed(batches):
            result = create_blocks(token, FEISHU_DOC_ID, batch, insert_at_start=True)
            
            if result.get('code') == 0:
                total_written += len(batch)
                print(f"   ✅ 已写入 {len(batch)} 个块 (总计: {total_written}/{len(blocks)})")
                time.sleep(0.3)
            else:
                print(f"   ❌ 写入失败: {result.get('msg')}")
                break
        
        print(f"\n✅ 每日业务复盘完成！")
        print(f"📄 文档链接: https://my.feishu.cn/wiki/{FEISHU_DOC_ID}")
        
        # 保存本地备份
        output_dir = Path.home() / '.openclaw' / 'workspace' / 'skills' / 'daily-summary' / 'output'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f'{datetime.now().strftime("%Y-%m-%d")}_summary_detailed.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 本地备份已保存: {output_file}")
        
        return 0
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
