"""
主评估脚本
提供命令行接口进行手术步骤质控评估
"""

import argparse
import sys
import os
from typing import Dict, Any

# 添加src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .openai_client import call_openai_api
    from .prompt import build_evaluation_messages, validate_surgery_steps, SURGERY_TYPES
    from .utils import read_file_content, format_json_output, load_env_config
except ImportError:
    from openai_client import call_openai_api
    from prompt import build_evaluation_messages, validate_surgery_steps, SURGERY_TYPES
    from utils import read_file_content, format_json_output, load_env_config


def evaluate_surgery_steps(surgery_steps: str, surgery_type: str = "general") -> Dict[str, Any]:
    """
    评估手术步骤
    
    Args:
        surgery_steps: 手术步骤描述
        surgery_type: 手术类型
        
    Returns:
        Dict[str, Any]: 评估结果
    """
    # 验证输入
    if not validate_surgery_steps(surgery_steps):
        raise ValueError("手术步骤描述无效")
    
    if surgery_type not in SURGERY_TYPES:
        print(f"警告: 未知手术类型 '{surgery_type}'，使用通用评估")
        surgery_type = "general"
    
    # 构建评估消息
    messages = build_evaluation_messages(surgery_steps, surgery_type)
    
    # 调用API进行评估
    try:
        result = call_openai_api(messages)
        return result
    except Exception as e:
        raise Exception(f"评估失败: {e}")


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(
        description="医院手术质控Agent - 手术步骤评估工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python evaluate.py --file data/appendectomy_01.txt --type appendectomy
  python evaluate.py --text "手术步骤..." --type cholecystectomy
  
支持的手术类型:
  appendectomy      - 阑尾切除术
  cholecystectomy   - 胆囊切除术  
  gastric_perforation - 胃穿孔修补术
  general           - 一般手术（默认）
        """
    )
    
    # 输入参数组（互斥）
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument(
        "--file", "-f",
        type=str,
        help="包含手术步骤的文本文件路径"
    )
    input_group.add_argument(
        "--text", "-t", 
        type=str,
        help="直接输入的手术步骤文本"
    )
    
    # 其他参数
    parser.add_argument(
        "--type", "-T",
        type=str,
        default="general",
        choices=list(SURGERY_TYPES.keys()),
        help="手术类型 (默认: general)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="输出结果到文件（可选）"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细信息"
    )
    
    parser.add_argument(
        "--config-check",
        action="store_true", 
        help="检查配置并退出"
    )
    
    args = parser.parse_args()
    
    # 配置检查模式
    if args.config_check:
        print("检查配置...")
        config = load_env_config()
        
        if config.get('OPENAI_API_KEY'):
            if config['OPENAI_API_KEY'].startswith('sk-'):
                print("✓ OPENAI_API_KEY: 已设置且格式正确")
            else:
                print("✗ OPENAI_API_KEY: 格式不正确")
                return 1
        else:
            print("✗ OPENAI_API_KEY: 未设置")
            return 1
            
        print(f"✓ OPENAI_MODEL: {config['OPENAI_MODEL']}")
        print(f"✓ OPENAI_BASE_URL: {config['OPENAI_BASE_URL']}")
        print("配置检查完成")
        return 0
    
    # 检查是否提供了输入参数
    if not args.file and not args.text:
        parser.error("必须提供 --file 或 --text 参数")
    
    try:
        # 获取手术步骤文本
        if args.file:
            if args.verbose:
                print(f"从文件读取手术步骤: {args.file}")
            surgery_steps = read_file_content(args.file)
        else:
            surgery_steps = args.text
        
        if args.verbose:
            print(f"手术类型: {SURGERY_TYPES[args.type]}")
            print(f"步骤长度: {len(surgery_steps)} 字符")
            print("开始评估...")
        
        # 执行评估
        result = evaluate_surgery_steps(surgery_steps, args.type)
        
        # 格式化输出
        formatted_result = format_json_output(result)
        
        # 输出结果
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(formatted_result)
            print(f"评估结果已保存到: {args.output}")
        else:
            print("\n=== 评估结果 ===")
            print(formatted_result)
        
        # 详细信息
        if args.verbose:
            print(f"\n=== 评估摘要 ===")
            print(f"总分: {result['total_score']}")
            print(f"风险等级: {result['risk_level']}")
            print(f"识别风险: {len(result['risks'])} 个")
            print(f"改进建议: {len(result['suggestions'])} 条")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"错误: {e}")
        return 1
    except ValueError as e:
        print(f"输入错误: {e}")
        return 1
    except Exception as e:
        print(f"评估失败: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 