#!/usr/bin/env python3
"""
医院手术质控Agent - 演示脚本
展示系统的主要功能和使用方法
"""

import os
import sys

def print_header():
    """打印演示标题"""
    print("=" * 60)
    print("🏥 医院手术质控Agent MVP - 功能演示")
    print("=" * 60)
    print()

def print_section(title):
    """打印章节标题"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_config_check():
    """演示配置检查功能"""
    print_section("1. 配置检查")
    print("命令: python src/evaluate.py --config-check")
    print()
    os.system("python src/evaluate.py --config-check")

def demo_help():
    """演示帮助信息"""
    print_section("2. 帮助信息")
    print("命令: python src/evaluate.py --help")
    print()
    os.system("python src/evaluate.py --help")

def demo_file_structure():
    """展示项目结构"""
    print_section("3. 项目结构")
    print("核心文件:")
    files = [
        "src/evaluate.py      # 主评估脚本",
        "src/openai_client.py # OpenAI API调用",
        "src/prompt.py        # Prompt模板管理", 
        "src/utils.py         # 工具函数",
        "data/samples/        # 示例数据",
        ".env                 # 环境配置",
        "README.md            # 使用说明"
    ]
    
    for file in files:
        print(f"  {file}")

def demo_sample_data():
    """展示示例数据"""
    print_section("4. 示例数据")
    
    samples = [
        ("阑尾切除术", "data/samples/appendectomy_01.txt"),
        ("胆囊切除术", "data/samples/cholecystectomy_01.txt"),
        ("胃穿孔修补术", "data/samples/gastric_perforation_01.txt")
    ]
    
    for name, file in samples:
        print(f"\n🔸 {name} ({file}):")
        try:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()[:200] + "..." if len(f.read()) > 200 else f.read()
                print(f"  {content[:100]}...")
        except FileNotFoundError:
            print(f"  文件未找到: {file}")

def demo_commands():
    """展示命令示例"""
    print_section("5. 使用示例")
    
    commands = [
        ("配置检查", "python src/evaluate.py --config-check"),
        ("评估阑尾切除术", "python src/evaluate.py --file data/samples/appendectomy_01.txt --type appendectomy --verbose"),
        ("评估胆囊切除术", "python src/evaluate.py --file data/samples/cholecystectomy_01.txt --type cholecystectomy"),
        ("直接文本输入", 'python src/evaluate.py --text "手术步骤..." --type general'),
        ("保存结果", "python src/evaluate.py --file data/samples/gastric_perforation_01.txt --type gastric_perforation --output result.json")
    ]
    
    for desc, cmd in commands:
        print(f"\n🔸 {desc}:")
        print(f"  {cmd}")

def demo_output_format():
    """展示输出格式"""
    print_section("6. 输出格式")
    
    sample_output = '''{
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
}'''
    
    print("评估结果JSON格式:")
    print(sample_output)

def demo_next_steps():
    """展示下一步操作"""
    print_section("7. 下一步操作")
    
    steps = [
        "1. 设置OpenAI API密钥到 .env 文件",
        "2. 运行配置检查: python src/evaluate.py --config-check", 
        "3. 测试示例评估: python src/evaluate.py --file data/samples/appendectomy_01.txt --type appendectomy --verbose",
        "4. 查看详细文档: README.md",
        "5. 查看开发计划: WORK_TODO.md"
    ]
    
    for step in steps:
        print(f"  {step}")

def main():
    """主演示函数"""
    print_header()
    
    # 检查是否在项目根目录
    if not os.path.exists("src/evaluate.py"):
        print("❌ 错误: 请在项目根目录运行此演示脚本")
        sys.exit(1)
    
    try:
        demo_config_check()
        demo_help()
        demo_file_structure()
        demo_sample_data()
        demo_commands()
        demo_output_format()
        demo_next_steps()
        
        print("\n" + "=" * 60)
        print("🎉 演示完成！系统已准备就绪。")
        print("💡 提示: 设置API密钥后即可开始使用手术质控评估功能。")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n演示被用户中断。")
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")

if __name__ == "__main__":
    main() 