#!/usr/bin/env python3
"""
每日业务总结脚本
自动分析当天对话，生成结构化业务思考总结
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import argparse

# 添加路径
script_dir = Path(__file__).parent
template_dir = script_dir.parent / "templates"
output_dir = os.environ.get('DAILY_SUMMARY_OUTPUT_DIR', str(script_dir.parent / "output"))

class DailySummaryGenerator:
    """每日总结生成器"""
    
    def __init__(self, date: str = None, output_dir: str = None):
        self.date_str = date or datetime.now().strftime('%Y-%m-%d')
        self.output_dir = Path(output_dir) if output_dir else Path(script_dir.parent / "output")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 读取模板
        template_file = template_dir / "summary_template.md"
        with open(template_file, 'r', encoding='utf-8') as f:
            self.template = f.read()
    
    def analyze_conversations(self) -> Dict[str, Any]:
        """分析当天对话内容（模拟实现）"""
        # TODO: 实际实现需要从 OpenClaw 获取当天对话历史
        # 这里返回模拟数据用于演示
        
        return {
            'total_messages': 15,
            'question_types': '业务问题(6) + 技术实现(5) + 学习需求(4)',
            'tasks_completed': 8,
            'business_questions': [
                '1. 采访提案优化：4分钟版 vs 5分钟版选择',
                '2. KOL pitching 策略制定',
                '3. 技术植入方式优化（隐性 vs 硬广）',
                '4. 传播渠道选择和时间规划',
                '5. 采访问题数量精简（6个问题）',
                '6. 目标受众定位（全球开发者社区）'
            ],
            'technical_requests': [
                '1. 知识库文档操作（读取、编辑、发布）',
                '2. Markdown 转 JSON 格式转换',
                '3. 采访提纲结构化整理',
                '4. 视频时间分配计算',
                '5. 多版本内容管理'
            ],
            'communication_tasks': [
                '1. 联系 Zack Williams 邮件准备',
                '2. KOL 沟通要点整理',
                '3. 团队协作任务分配',
                '4. 文档版本管理'
            ],
            'learning_needs': [
                '1. Google "In the Flow" 系列框架学习',
                '2. 技术植入叙事技巧',
                '3. 视频制作流程了解',
                '4. KOL pitching 最佳实践'
            ],
            'challenges_and_solutions': [
                '挑战1: 如何在有限时长内平衡技术深度和完播率？\n  解决方案: 采用"问题驱动三段式"叙事，聚焦核心技巧',
                '挑战2: 技术植入如何避免硬广感？\n  解决方案: 采用场景化、对比化、体验化叙事，通过真实案例展示价值',
                '挑战3: 如何设计既有深度又吸引人的问题？\n  解决方案: 每个问题自带叙事方向，引导受访者自然讲述'
            ],
            'technical_decisions': [
                '1. 选择 v2.0 (4分钟版) 作为主推版本，完播率优先',
                '2. 技术植入集中在 Q4，占比 60%，自然度 ⭐⭐⭐⭐',
                '3. 使用知识库 API 进行文档管理，便于团队协作',
                '4. 采用 Markdown 格式便于版本控制和内容复用'
            ],
            'best_practices': [
                '1. 技巧命名化: "Relief Generation Pipeline" 易记易传播',
                '2. 问题减法哲学: 从8个精简到6个，避免信息过载',
                '3. 叙事结构化: 开场钩子 → 核心技巧 → 价值总结',
                '4. 视觉丰富: 采访画面 + B-Roll 穿插，提升观看体验'
            ],
            'business_logic': [
                '1. 核心价值主张: 通过真实开发者故事展示 ERNIE OCR 技术价值',
                '2. 目标受众: 全球技术社区，特别是 AI/ML 开发者',
                '3. 传播目标: 提升开发者对百度技术的认知和好感，引导 API 试用',
                '4. 竞争优势: 真实案例背书比官方演示更有说服力'
            ],
            'user_needs_mapping': [
                '1. 需要结构化的采访提案，而非零散的想法',
                '2. 需要可执行的 KOL 沟通方案',
                '3. 需要明确的版本选择建议',
                '4. 需要完整的执行时间线和 KPI 指标'
            ],
            'value_proposition': [
                '1. 专业框架: 基于 Google "In the Flow" 深度优化',
                '2. 技术隐性植入: 避免硬广，提升可信度',
                '3. 双版本适配: 满足不同平台和时长需求',
                '4. 可执行性强: 包含分镜脚本、B-Roll 清单、时间线'
            ],
            'risk_management': [
                '风险1: KOL 时间协调困难\n  应对: 提前2周沟通，提供灵活时间选项',
                '风险2: 技术植入过于生硬\n  应对: 提供参考回答框架，鼓励真实体验表达',
                '风险3: 视频完播率不达标\n  应对: 优化内容节奏，增加视觉变化，设置吸引点'
            ],
            'short_term_actions': [
                '1. 完成 Zack Williams 邮件草稿，包含问题清单和参考视频',
                '2. 整理 Q4 技术植入要点，准备沟通材料',
                '3. 设计拍摄场地和视觉效果方案',
                '4. 创建 B-Roll 素材清单和制作计划'
            ],
            'mid_term_optimizations': [
                '1. 联系 2-3 位备选 KOL，建立合作关系',
                '2. 准备多套采访方案，适应不同技术背景的受访者',
                '3. 建立 "Powered by ERNIE" 系列内容库',
                '4. 设计传播渠道测试方案，优化投放策略'
            ],
            'long_term_directions': [
                '1. 打造 "Powered by ERNIE" 技术创作者系列品牌',
                '2. 建立开发者社区运营机制，持续产出优质内容',
                '3. 探索更多技术领域（如 NLP、CV、推荐系统）的案例',
                '4. 形成标准化的 KOL 合作流程和内容生产体系'
            ],
            'new_skills': [
                '1. 掌握 Google "In the Flow" 采访框架的核心要素',
                '2. 学会"问题驱动三段式"叙事结构设计',
                '3. 掌握技术隐性植入的叙事技巧（场景化、对比化、体验化）',
                '4. 学会技巧命名化方法，提升内容传播力'
            ],
            'improvement_points': [
                '1. 业务分析能力: 能够从零散需求中提炼结构化方案',
                '2. 技术理解能力: 快速掌握 ERNIE OCR 技术价值点',
                '3. 沟通协调能力: 设计 KOL 沟通方案，平衡各方需求',
                '4. 项目管理能力: 制定完整的执行时间线和 KPI 体系'
            ],
            'cognitive_breakthroughs': [
                '1. 认识到"隐性植入"比"硬广推销"更有说服力',
                '2. 理解"技巧命名化"对内容传播的重要性',
                '3. 明确"问题驱动叙事"比"功能堆砌"更有效',
                '4. 发现"真实案例背书"是技术传播的核心资产'
            ],
            'methodologies_mastered': [
                '1. "In the Flow" 系列框架应用方法',
                '2. 技术植入叙事设计方法论',
                '3. KOL pitching 沟通策略',
                '4. 结构化提案撰写方法'
            ],
            'resource_links': [
                '- 采访提案文档: https://ku.baidu-int.com/d/izW8auLSHl_gq4',
                '- Google "In the Flow" 系列: [参考视频链接]',
                '- ERNIE API 文档: https://cloud.baidu.com/ernie',
                '- NisabaRelief 项目: https://huggingface.co/boatbomber/NisabaRelief'
            ],
            'reflections': [
                '1. 今天最大的收获是理解了如何通过真实故事展示技术价值，而非直接推销产品。',
                '2. 发现"问题驱动三段式"叙事框架非常实用，可以应用到其他内容创作中。',
                '3. 意识到 KOL 沟通需要平衡"商业目标"和"创作者体验"，提供真实价值。',
                '4. 学会在有限约束下（如5分钟时长）最大化信息传递效率，这是重要的内容设计能力。'
            ]
        }
    
    def generate_summary(self, analysis: Dict[str, Any]) -> str:
        """生成总结文档"""
        # 填充模板
        content = self.template
        
        # 基本信息
        content = content.replace('{{date}}', self.date_str)
        content = content.replace('{{username}}', os.environ.get('SANDBOX_USERNAME', 'user'))
        content = content.replace('{{total_messages}}', str(analysis['total_messages']))
        content = content.replace('{{question_types}}', analysis['question_types'])
        content = content.replace('{{tasks_completed}}', str(analysis['tasks_completed']))
        
        # 业务问题
        content = content.replace('{{business_questions}}', 
            '\n'.join([f'- {q}' for q in analysis['business_questions']]))
        content = content.replace('{{technical_requests}}',
            '\n'.join([f'- {q}' for q in analysis['technical_requests']]))
        content = content.replace('{{communication_tasks}}',
            '\n'.join([f'- {q}' for q in analysis['communication_tasks']]))
        content = content.replace('{{learning_needs}}',
            '\n'.join([f'- {q}' for q in analysis['learning_needs']]))
        
        # 技术洞察
        content = content.replace('{{challenges_and_solutions}}',
            '\n\n'.join([f'**{q}**' for q in analysis['challenges_and_solutions']]))
        content = content.replace('{{technical_decisions}}',
            '\n'.join([f'- {q}' for q in analysis['technical_decisions']]))
        content = content.replace('{{best_practices}}',
            '\n'.join([f'- {q}' for q in analysis['best_practices']]))
        
        # 业务思考
        content = content.replace('{{business_logic}}',
            '\n'.join([f'- {q}' for q in analysis['business_logic']]))
        content = content.replace('{{user_needs_mapping}}',
            '\n'.join([f'- {q}' for q in analysis['user_needs_mapping']]))
        content = content.replace('{{value_proposition}}',
            '\n'.join([f'- {q}' for q in analysis['value_proposition']]))
        content = content.replace('{{risk_management}}',
            '\n\n'.join([f'**{q}**' for q in analysis['risk_management']]))
        
        # 下一步建议
        content = content.replace('{{short_term_actions}}',
            '\n'.join([f'- {q}' for q in analysis['short_term_actions']]))
        content = content.replace('{{mid_term_optimizations}}',
            '\n'.join([f'- {q}' for q in analysis['mid_term_optimizations']]))
        content = content.replace('{{long_term_directions}}',
            '\n'.join([f'- {q}' for q in analysis['long_term_directions']]))
        
        # 学习收获
        content = content.replace('{{new_skills}}',
            '\n'.join([f'- {q}' for q in analysis['new_skills']]))
        content = content.replace('{{improvement_points}}',
            '\n'.join([f'- {q}' for q in analysis['improvement_points']]))
        content = content.replace('{{cognitive_breakthroughs}}',
            '\n'.join([f'- {q}' for q in analysis['cognitive_breakthroughs']]))
        content = content.replace('{{methodologies_mastered}}',
            '\n'.join([f'- {q}' for q in analysis['methodologies_mastered']]))
        
        # 资源和反思
        content = content.replace('{{resource_links}}',
            '\n'.join(analysis['resource_links']))
        content = content.replace('{{reflections}}',
            '\n'.join([f'- {q}' for q in analysis['reflections']]))
        
        # 元信息
        content = content.replace('{{generated_time}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        return content
    
    def save_summary(self, content: str) -> Path:
        """保存总结文档"""
        filename = f"{self.date_str}_summary.md"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='每日业务总结生成器')
    parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)，默认为今天')
    parser.add_argument('--output', help='指定输出目录')
    parser.add_argument('--send-infoflow', action='store_true', help='发送摘要到如流')
    parser.add_argument('--verbose', action='store_true', help='详细输出模式')
    
    args = parser.parse_args()
    
    # 初始化生成器
    generator = DailySummaryGenerator(date=args.date, output_dir=args.output)
    
    if args.verbose:
        print(f"📅 日期: {generator.date_str}")
        print(f"📁 输出目录: {generator.output_dir}")
        print(f"🔧 分析对话内容...")
    
    # 分析对话
    analysis = generator.analyze_conversations()
    
    if args.verbose:
        print(f"✅ 分析完成:")
        print(f"   - 对话总数: {analysis['total_messages']}")
        print(f"   - 任务完成: {analysis['tasks_completed']}")
        print(f"   - 业务问题: {len(analysis['business_questions'])}")
    
    # 生成总结
    summary_content = generator.generate_summary(analysis)
    
    if args.verbose:
        print(f"📝 生成总结文档...")
    
    # 保存总结
    filepath = generator.save_summary(summary_content)
    
    print(f"✅ 每日总结已生成:")
    print(f"📄 文件路径: {filepath}")
    print(f"📊 统计:")
    print(f"   - 对话总数: {analysis['total_messages']}")
    print(f"   - 任务完成: {analysis['tasks_completed']}")
    print(f"   - 业务问题: {len(analysis['business_questions'])}")
    print(f"   - 技术洞察: {len(analysis['challenges_and_solutions'])}")
    print(f"   - 行动建议: {len(analysis['short_term_actions'])}")
    
    # TODO: 如果需要发送到如流，这里可以调用 infoflow_send
    # if args.send_infoflow:
    #     send_to_infoflow(summary_content)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
