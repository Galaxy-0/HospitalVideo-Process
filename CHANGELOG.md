# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 初始项目结构和PRD文档
- 基于uv的Python项目配置
- Git版本管理初始化

## [0.1.0] - 2024-01-XX

### Added
- 🎯 **核心功能实现**
  - 实现基于OpenAI API的手术质控评估系统
  - 支持阑尾切除、胆囊切除、胃穿孔修补三种手术类型
  - 结构化JSON输出（总分、风险点、改进建议）
  
- 🔧 **技术架构**
  - `src/openai_client.py`: OpenAI API调用模块，使用urllib.request实现HTTP调用
  - `src/prompt.py`: Prompt模板管理，包含系统提示和手术特定指导
  - `src/evaluate.py`: 主评估脚本，提供完整的命令行接口
  - `src/utils.py`: 工具函数模块，配置管理和文件操作
  
- 📋 **命令行接口**
  - 支持文件输入和直接文本输入
  - 多种手术类型选择
  - 详细输出和配置检查功能
  - 结果保存到文件
  
- 📊 **示例数据**
  - 阑尾切除术标准操作步骤示例
  - 腹腔镜胆囊切除术操作步骤示例  
  - 胃穿孔修补术操作步骤示例
  
- 🧪 **测试工具**
  - 功能测试脚本 `test_api_call.py`
  - 模拟API响应测试
  - 配置验证功能

### Technical Features  
- **零依赖**: 仅使用Python标准库，无第三方依赖
- **模块化**: 清晰的模块分离，便于维护和扩展
- **错误处理**: 完整的异常处理和用户友好的错误信息
- **配置管理**: 基于环境变量的配置系统
- **可扩展**: 支持新增手术类型和评估维度

### Development Environment
- Python 3.13.2 (兼容3.11+)
- uv包管理器
- OpenAI GPT-4o模型 