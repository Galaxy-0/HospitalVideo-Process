"""
OpenAI API调用模块
使用urllib.request实现HTTP调用，避免第三方依赖
"""

import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

try:
    from .utils import load_env_config, validate_config
except ImportError:
    from utils import load_env_config, validate_config


def call_openai_api(messages: List[Dict[str, str]], model: str = "gpt-4o") -> Dict[str, Any]:
    """
    调用OpenAI Chat Completions API
    
    Args:
        messages: 消息列表，格式为 [{"role": "system", "content": "..."}, ...]
        model: 使用的模型名称
        
    Returns:
        Dict[str, Any]: 解析后的响应数据
        
    Raises:
        Exception: API调用失败或响应解析错误
    """
    # 2.2.4: 配置管理
    config = load_env_config()
    if not validate_config(config):
        raise ValueError("配置验证失败")
    
    # 2.2.1: 基础HTTP调用实现
    api_key = config['OPENAI_API_KEY']
    base_url = config['OPENAI_BASE_URL']
    url = f"{base_url}/chat/completions"
    
    # 构造请求数据
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 1000,
        "response_format": {"type": "json_object"}
    }
    
    # 构造HTTP请求
    json_data = json.dumps(data).encode('utf-8')
    
    request = urllib.request.Request(
        url,
        data=json_data,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'HospitalAgent/0.1.0'
        },
        method='POST'
    )
    
    try:
        # 2.2.1c: 执行HTTP调用并获取响应
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status != 200:
                raise Exception(f"HTTP错误: {response.status}")
            
            response_data = response.read().decode('utf-8')
            
        # 2.2.2: JSON处理与解析
        return _parse_openai_response(response_data)
        
    except urllib.error.HTTPError as e:
        # 2.2.3a: HTTP错误处理
        error_body = e.read().decode('utf-8') if e.fp else "无错误详情"
        raise Exception(f"OpenAI API HTTP错误 {e.code}: {error_body}")
        
    except urllib.error.URLError as e:
        # 2.2.3a: 网络错误处理
        raise Exception(f"网络连接错误: {e.reason}")
        
    except Exception as e:
        # 2.2.3b: 其他错误处理
        raise Exception(f"API调用失败: {str(e)}")


def _parse_openai_response(response_data: str) -> Dict[str, Any]:
    """
    解析OpenAI API响应
    
    Args:
        response_data: 原始响应字符串
        
    Returns:
        Dict[str, Any]: 解析后的评分数据
    """
    try:
        # 2.2.2a: 响应JSON解析
        raw_response = json.loads(response_data)
        
        # 提取消息内容
        if 'choices' not in raw_response or not raw_response['choices']:
            raise ValueError("响应中没有choices字段")
            
        message_content = raw_response['choices'][0]['message']['content']
        
        # 解析LLM返回的JSON内容
        evaluation_result = json.loads(message_content)
        
        # 2.2.2b: 输出格式验证
        return _validate_evaluation_result(evaluation_result)
        
    except json.JSONDecodeError as e:
        # 2.2.3b: JSON解析错误处理
        raise Exception(f"JSON解析错误: {e}")
    except KeyError as e:
        # 2.2.3b: 缺少必需字段
        raise Exception(f"响应格式错误，缺少字段: {e}")
    except Exception as e:
        # 2.2.3b: 其他解析错误
        raise Exception(f"响应解析失败: {e}")


def _validate_evaluation_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证评估结果格式
    
    Args:
        result: 待验证的结果字典
        
    Returns:
        Dict[str, Any]: 验证并标准化后的结果
    """
    # 检查必需字段
    required_fields = ['total_score', 'risks', 'suggestions']
    for field in required_fields:
        if field not in result:
            raise ValueError(f"缺少必需字段: {field}")
    
    # 基础数据类型验证
    if not isinstance(result['total_score'], (int, float)):
        raise ValueError("total_score必须是数字")
        
    if not isinstance(result['risks'], list):
        raise ValueError("risks必须是列表")
        
    if not isinstance(result['suggestions'], list):
        raise ValueError("suggestions必须是列表")
    
    # 标准化输出格式
    standardized_result = {
        'total_score': float(result['total_score']),
        'risks': [str(risk) for risk in result['risks']],
        'suggestions': [str(suggestion) for suggestion in result['suggestions']],
        'risk_level': result.get('risk_level', 'Unknown')
    }
    
    # 分数范围验证
    if not (0 <= standardized_result['total_score'] <= 100):
        print(f"警告: 分数超出范围 [0-100]: {standardized_result['total_score']}")
    
    return standardized_result


def test_api_connection() -> bool:
    """
    测试API连接是否正常
    
    Returns:
        bool: 连接是否成功
    """
    try:
        test_messages = [
            {"role": "system", "content": "你是一个测试助手，请返回JSON格式: {\"status\": \"ok\"}"},
            {"role": "user", "content": "测试连接"}
        ]
        
        result = call_openai_api(test_messages)
        print("API连接测试成功")
        print(f"测试结果: {result}")
        return True
        
    except Exception as e:
        print(f"API连接测试失败: {e}")
        return False


if __name__ == "__main__":
    # 2.2.5: 简单测试验证
    print("开始测试OpenAI API连接...")
    test_api_connection() 