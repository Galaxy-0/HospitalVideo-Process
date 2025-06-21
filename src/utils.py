"""
工具函数模块
提供项目中常用的辅助功能
"""

import os
from typing import Dict, Any


def load_env_config() -> Dict[str, str]:
    """
    加载环境变量配置
    
    Returns:
        Dict[str, str]: 配置字典
    """
    config = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
        'OPENAI_MODEL': os.getenv('OPENAI_MODEL', 'deepseek-chat'),
        'OPENAI_BASE_URL': os.getenv('OPENAI_BASE_URL', 'https://api.deepseek.com'),
        'DEBUG': os.getenv('DEBUG', 'false').lower() == 'true'
    }
    return config


def validate_config(config: Dict[str, str]) -> bool:
    """
    验证配置是否有效
    
    Args:
        config: 配置字典
        
    Returns:
        bool: 配置是否有效
    """
    if not config.get('OPENAI_API_KEY'):
        print("错误: OPENAI_API_KEY 未设置")
        return False
    
    if not config.get('OPENAI_API_KEY').startswith('sk-'):
        print("错误: OPENAI_API_KEY 格式不正确")
        return False
    
    return True


def read_file_content(file_path: str) -> str:
    """
    读取文件内容
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件内容
        
    Raises:
        FileNotFoundError: 文件不存在
        IOError: 文件读取错误
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"文件未找到: {file_path}")
    except Exception as e:
        raise IOError(f"文件读取错误: {e}")


def format_json_output(data: Dict[str, Any], indent: int = 2) -> str:
    """
    格式化JSON输出
    
    Args:
        data: 要格式化的数据
        indent: 缩进空格数
        
    Returns:
        str: 格式化后的JSON字符串
    """
    import json
    return json.dumps(data, ensure_ascii=False, indent=indent) 