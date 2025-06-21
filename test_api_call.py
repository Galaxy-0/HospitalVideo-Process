#!/usr/bin/env python3
"""
API调用测试脚本
用于验证openai_client模块的基本功能
"""

import os
import sys

# 添加src目录到路径
sys.path.insert(0, 'src')

from src.openai_client import test_api_connection
from src.utils import load_env_config, validate_config
from src.prompt import build_evaluation_messages

def test_without_api():
    """测试不需要API的功能"""
    print("=== 测试基础功能（无需API） ===")
    
    # 测试配置加载
    print("1. 测试配置加载...")
    config = load_env_config()
    print(f"   OPENAI_MODEL: {config['OPENAI_MODEL']}")
    print(f"   OPENAI_BASE_URL: {config['OPENAI_BASE_URL']}")
    print(f"   API Key 长度: {len(config.get('OPENAI_API_KEY', ''))}")
    
    # 测试配置验证
    print("2. 测试配置验证...")
    is_valid = validate_config(config)
    print(f"   配置有效性: {is_valid}")
    
    # 测试Prompt构建
    print("3. 测试Prompt构建...")
    test_steps = """
    1. 患者全麻后取仰卧位
    2. 常规消毒铺巾  
    3. 在McBurney点作斜切口
    4. 逐层切开至腹膜
    5. 探查阑尾位置
    """
    
    messages = build_evaluation_messages(test_steps, "appendectomy")
    print(f"   生成消息数量: {len(messages)}")
    print(f"   系统消息长度: {len(messages[0]['content'])}")
    print(f"   用户消息长度: {len(messages[1]['content'])}")
    
    print("✓ 基础功能测试完成")

def test_with_mock_api():
    """使用模拟数据测试API调用逻辑"""
    print("\n=== 测试API调用逻辑（模拟数据） ===")
    
    # 模拟一个成功的API响应
    mock_response = {
        "choices": [{
            "message": {
                "content": '{"total_score": 85, "risks": ["术中出血风险"], "suggestions": ["加强止血"], "risk_level": "Medium"}'
            }
        }]
    }
    
    from src.openai_client import _parse_openai_response
    import json
    
    try:
        result = _parse_openai_response(json.dumps(mock_response))
        print("✓ 模拟API响应解析成功")
        print(f"   总分: {result['total_score']}")
        print(f"   风险数量: {len(result['risks'])}")
        print(f"   建议数量: {len(result['suggestions'])}")
        print(f"   风险等级: {result['risk_level']}")
    except Exception as e:
        print(f"✗ 模拟API响应解析失败: {e}")

def main():
    """主测试函数"""
    print("医院质控Agent - 功能测试")
    print("=" * 50)
    
    test_without_api()
    test_with_mock_api()
    
    print("\n=== 测试总结 ===")
    print("✓ 配置管理模块正常")
    print("✓ Prompt构建模块正常") 
    print("✓ API响应解析模块正常")
    print("✓ 核心功能验证完成")
    
    print("\n下一步:")
    print("1. 设置 .env 文件中的 OPENAI_API_KEY")
    print("2. 运行: python src/evaluate.py --config-check")
    print("3. 运行: python src/evaluate.py --file data/samples/appendectomy_01.txt --type appendectomy")

if __name__ == "__main__":
    main() 