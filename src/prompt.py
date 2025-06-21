"""
Prompt模板管理模块
提供手术质控评估的Prompt模板和拼装功能
"""

from typing import List, Dict, Any


# 系统Prompt模板
SYSTEM_PROMPT = """你是一名资深的手术质控专家，拥有丰富的临床经验和质控评估能力。

你的任务是对提供的手术操作步骤进行专业评估，从以下维度进行分析：
1. 操作合理性：手术步骤是否符合标准流程
2. 安全风险：识别潜在的手术风险点
3. 改进建议：提出具体的改进措施

评估标准：
- 100-90分：操作规范，无明显风险
- 89-75分：操作基本规范，有轻微改进空间
- 74-60分：操作存在问题，需要改进
- 59-0分：操作严重不规范，存在重大风险

请严格按照以下JSON格式输出结果，必须是有效的JSON，不要包含任何其他文字说明：

```json
{
  "total_score": 85,
  "risks": ["风险点1", "风险点2"],
  "suggestions": ["改进建议1", "改进建议2"],
  "risk_level": "Medium"
}
```

重要要求：
1. 只输出JSON格式的内容，不要有其他解释文字
2. risk_level的值只能是：Low（低风险）、Medium（中风险）、High（高风险）
3. total_score必须是0-100之间的数字"""


# 用户Prompt模板
USER_PROMPT_TEMPLATE = """请评估以下{surgery_type}手术的操作步骤：

手术类型：{surgery_type}
手术步骤：
{surgery_steps}

请根据医学标准和安全规范，对上述手术步骤进行全面评估。"""


# 手术类型映射
SURGERY_TYPES = {
    "appendectomy": "阑尾切除术",
    "cholecystectomy": "胆囊切除术", 
    "gastric_perforation": "胃穿孔修补术",
    "general": "一般手术"
}


def build_evaluation_messages(surgery_steps: str, surgery_type: str = "general") -> List[Dict[str, str]]:
    """
    构建用于评估的消息列表
    
    Args:
        surgery_steps: 手术步骤描述
        surgery_type: 手术类型（appendectomy/cholecystectomy/gastric_perforation/general）
        
    Returns:
        List[Dict[str, str]]: 格式化的消息列表
    """
    # 标准化手术类型
    surgery_type_cn = SURGERY_TYPES.get(surgery_type, "一般手术")
    
    # 构建用户消息
    user_content = USER_PROMPT_TEMPLATE.format(
        surgery_type=surgery_type_cn,
        surgery_steps=surgery_steps.strip()
    )
    
    # 返回消息列表
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user", 
            "content": user_content
        }
    ]
    
    return messages


def get_surgery_specific_guidance(surgery_type: str) -> str:
    """
    获取手术类型特定的评估指导
    
    Args:
        surgery_type: 手术类型
        
    Returns:
        str: 特定指导内容
    """
    guidance = {
        "appendectomy": """
阑尾切除术评估要点：
- 切口选择是否合适（McBurney点切口或腹腔镜）
- 阑尾动脉处理是否得当
- 阑尾根部结扎是否牢固
- 腹腔冲洗是否充分
- 是否有感染预防措施
        """,
        
        "cholecystectomy": """
胆囊切除术评估要点：
- Calot三角解剖是否清晰
- 胆囊动脉和胆囊管识别是否准确
- 电凝止血是否充分
- 胆囊床渗血处理是否妥当
- 腹腔镜操作是否规范
        """,
        
        "gastric_perforation": """
胃穿孔修补术评估要点：
- 穿孔部位探查是否充分
- 缝合方式是否合适（单层或双层）
- 大网膜覆盖是否到位
- 腹腔冲洗引流是否充分
- 术后并发症预防措施
        """,
        
        "general": """
一般手术评估要点：
- 手术指征是否明确
- 操作步骤是否规范
- 无菌原则是否遵守
- 止血是否充分
- 组织处理是否轻柔
        """
    }
    
    return guidance.get(surgery_type, guidance["general"])


def validate_surgery_steps(surgery_steps: str) -> bool:
    """
    验证手术步骤描述是否有效
    
    Args:
        surgery_steps: 手术步骤描述
        
    Returns:
        bool: 是否有效
    """
    if not surgery_steps or not surgery_steps.strip():
        return False
        
    # 基本长度检查
    if len(surgery_steps.strip()) < 50:
        print("警告: 手术步骤描述过短，可能影响评估质量")
        
    if len(surgery_steps.strip()) > 2000:
        print("警告: 手术步骤描述过长，可能超出模型处理能力")
        
    return True


def format_evaluation_prompt(surgery_steps: str, surgery_type: str = "general") -> str:
    """
    格式化完整的评估Prompt（用于调试）
    
    Args:
        surgery_steps: 手术步骤
        surgery_type: 手术类型
        
    Returns:
        str: 完整的Prompt文本
    """
    messages = build_evaluation_messages(surgery_steps, surgery_type)
    
    formatted_prompt = f"=== 系统提示 ===\n{messages[0]['content']}\n\n"
    formatted_prompt += f"=== 用户输入 ===\n{messages[1]['content']}\n\n"
    formatted_prompt += f"=== 手术特定指导 ===\n{get_surgery_specific_guidance(surgery_type)}"
    
    return formatted_prompt


if __name__ == "__main__":
    # 测试Prompt构建
    test_steps = """
    1. 患者全麻后取仰卧位
    2. 常规消毒铺巾
    3. 在McBurney点作斜切口
    4. 逐层切开至腹膜
    5. 探查阑尾位置和炎症程度
    6. 分离阑尾周围粘连
    7. 结扎阑尾动脉
    8. 在阑尾根部用丝线结扎
    9. 切除阑尾
    10. 检查止血情况
    11. 生理盐水冲洗腹腔
    12. 逐层缝合切口
    """
    
    messages = build_evaluation_messages(test_steps, "appendectomy")
    print("构建的消息列表:")
    for i, msg in enumerate(messages):
        print(f"{i+1}. {msg['role']}: {msg['content'][:100]}...")
        
    print(f"\n手术类型指导:\n{get_surgery_specific_guidance('appendectomy')}") 