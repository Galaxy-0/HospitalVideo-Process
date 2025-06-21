# 医院手术质控Agent MVP

基于大模型的手术步骤质控评估系统，使用OpenAI API对手术操作流程进行智能分析和评分。

## 🎯 项目目标

- **输入**: 手术文字步骤（300-800字）+ 手术类型标签
- **输出**: 结构化JSON评分（总分、风险点、改进建议）
- **支持手术**: 阑尾切除、胆囊切除、胃穿孔修补
- **成功标准**: ≥70%的输出被医生评为"有实用价值"

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd HospitalVideo-Process

# 创建虚拟环境
uv venv
source .venv/bin/activate  # Linux/Mac

# 配置环境变量
cp env.example .env
# 编辑 .env 文件，设置你的 DeepSeek API 密钥
```

### 2. API配置

系统默认使用DeepSeek API，在 `.env` 文件中配置：

```bash
# DeepSeek API配置
OPENAI_API_KEY=sk-your-deepseek-api-key-here
OPENAI_MODEL=deepseek-chat
OPENAI_BASE_URL=https://api.deepseek.com
```

如果要使用OpenAI API，修改为：
```bash
# OpenAI API配置
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. 配置检查

```bash
# 检查配置是否正确
python src/evaluate.py --config-check
```

### 4. 运行评估

```bash
# 评估示例手术步骤
python src/evaluate.py --file data/samples/appendectomy_01.txt --type appendectomy --verbose

# 直接输入文本评估
python src/evaluate.py --text "手术步骤内容..." --type cholecystectomy

# 保存结果到文件
python src/evaluate.py --file data/samples/gastric_perforation_01.txt --type gastric_perforation --output results.json
```

## 📋 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--file, -f` | 手术步骤文件路径 | `--file data/samples/appendectomy_01.txt` |
| `--text, -t` | 直接输入手术步骤 | `--text "1. 患者全麻..."` |
| `--type, -T` | 手术类型 | `--type appendectomy` |
| `--output, -o` | 输出文件路径 | `--output result.json` |
| `--verbose, -v` | 显示详细信息 | `--verbose` |
| `--config-check` | 检查配置 | `--config-check` |

### 支持的手术类型

- `appendectomy` - 阑尾切除术
- `cholecystectomy` - 胆囊切除术
- `gastric_perforation` - 胃穿孔修补术
- `general` - 一般手术（默认）

## 📊 输出格式

```json
{
  "total_score": 85.0,
  "risks": [
    "术中出血风险",
    "感染风险"
  ],
  "suggestions": [
    "建议加强止血措施",
    "术后密切观察"
  ],
  "risk_level": "Medium"
}
```

## 🧪 测试功能

```bash
# 运行功能测试
python test_api_call.py

# 测试所有模块
python src/prompt.py
python src/utils.py
```

## 📁 项目结构

```
HospitalVideo-Process/
├── src/                    # 核心代码
│   ├── evaluate.py        # 主评估脚本
│   ├── openai_client.py   # OpenAI API调用
│   ├── prompt.py          # Prompt模板管理
│   └── utils.py           # 工具函数
├── data/                  # 示例数据
│   └── samples/           # 手术步骤示例
├── .env                   # 环境变量配置
├── pyproject.toml         # 项目配置
└── README.md              # 说明文档
```

## ⚙️ 技术实现

- **API调用**: 使用Python标准库`urllib.request`，无第三方依赖
- **支持模型**: DeepSeek Chat (默认) / OpenAI GPT-4o
- **输出格式**: 结构化JSON，包含评分、风险点、建议
- **错误处理**: 完整的异常处理和配置验证
- **兼容性**: 支持OpenAI兼容的API接口

## 🔧 开发说明

### 核心模块

1. **openai_client.py**: 
   - HTTP请求构造和发送
   - JSON响应解析和验证
   - 错误处理和异常管理

2. **prompt.py**:
   - 系统和用户Prompt模板
   - 手术类型特定的评估指导
   - 消息格式化和拼装

3. **evaluate.py**:
   - 命令行接口
   - 文件处理和输出格式化
   - 主要业务逻辑

4. **utils.py**:
   - 配置管理
   - 文件操作
   - 通用工具函数

### 设计原则

- **极简化**: 避免过度工程，专注核心价值验证
- **无依赖**: 仅使用Python标准库
- **可扩展**: 模块化设计，便于后续扩展
- **易测试**: 清晰的接口和错误处理

## 📈 下一步计划

1. **数据扩充**: 增加更多手术类型和示例
2. **批量处理**: 实现批量评估脚本
3. **结果分析**: 添加统计分析功能
4. **医生评审**: 收集专业医生反馈
5. **性能优化**: 优化API调用和响应时间

## 🐛 已知限制

- 需要有效的OpenAI API密钥
- 单次评估，无批量处理
- 基础错误处理，无重试机制
- 示例数据有限

## 📞 支持

如有问题或建议，请查看：
- [TASK_COMPLEXITY_ANALYSIS.md](TASK_COMPLEXITY_ANALYSIS.md) - 任务复杂度分析
- [WORK_TODO.md](WORK_TODO.md) - 开发计划
- [CHANGELOG.md](CHANGELOG.md) - 变更记录

---

*最后更新: 2024-01-XX*
