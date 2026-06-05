# 🏫 校园信息智能查询系统

> 基于LangGraph和智谱大模型的多功能模块化校园服务平台

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-orange.svg)](https://github.com)

## ✨ 项目简介

本项目是一个基于LangGraph构建的校园信息智能查询系统，采用**多功能模块化设计**，面向学生、教师与管理员提供一站式校园服务。系统通过智谱大模型API实现自然语言意图识别，自动调用封装的查询工具，支持成绩、课表、选课、空教室、考试安排、校园通知等高频查询功能。

### 🎯 核心特性

- **🤖 AI智能助手**：基于LangGraph和智谱大模型的智能对话系统
- **🧠 对话记忆**：支持多轮对话上下文记忆，提升交互体验
- **📚 知识库支持**：内置校园知识库，提供常见问题快速解答
- **🎨 现代化UI**：基于Gradio的响应式网页界面，左侧侧边栏导航
- **🔧 模块化设计**：各功能模块独立开发，易于扩展和维护
- **📊 多功能集成**：成绩、课表、教室、考试、通知六大功能模块

## 🏗️ 项目架构

```
campus-info-agent/
├── agent/                  # 智能体核心模块（已废弃，功能已迁移到features/）
├── features/              # 功能模块目录
│   ├── __init__.py
│   ├── base_feature.py    # 功能模块基类
│   ├── agent_feature.py   # AI智能助手功能
│   ├── grade_feature.py   # 成绩查询功能
│   ├── schedule_feature.py # 课表查询功能
│   ├── classroom_feature.py # 教室查询功能
│   ├── exam_feature.py    # 考试查询功能
│   └── notice_feature.py  # 通知查询功能
├── utils/                 # 工具模块目录
│   ├── __init__.py
│   ├── logger.py          # 日志记录工具
│   ├── memory.py          # 对话记忆工具
│   └── knowledge_base.py  # 知识库管理工具
├── ui/                    # 用户界面模块
│   ├── __init__.py
│   └── gradio_ui.py       # Gradio界面实现
├── data/                  # 数据模块
│   └── mock_data.py       # 模拟校园数据
├── api/                   # API接口模块（预留）
├── logs/                  # 日志文件目录
├── memory/                # 对话记忆存储目录
├── config.py              # 配置文件
├── main.py                # 主程序入口
├── requirements.txt       # 依赖包列表
└── README.md             # 项目说明文档
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置系统

编辑 `config.py` 文件，设置智谱AI API密钥：

```python
class Config:
    ZHIPU_API_KEY = "your_api_key_here"  # 替换为你的API密钥
    MODEL_NAME = "glm-4"
    # ... 其他配置
```

### 启动系统

```bash
python main.py
```

系统启动后，会自动在浏览器中打开界面，默认访问地址：`http://127.0.0.1:7860`

## 📖 功能说明

### 🤖 AI智能助手

- **自然语言交互**：支持用自然语言提问，系统自动识别意图
- **对话记忆**：记住对话上下文，支持多轮对话
- **知识库搜索**：自动搜索相关知识库内容
- **工具调用**：自动调用相应的查询工具

**示例对话**：
```
用户：我的成绩怎么样？
助手：我来帮您查询成绩信息...
用户：那我的课表呢？
助手：根据上下文，我为您查询课表信息...
```

### 📊 成绩查询

- 按学期查询成绩
- 查看全部成绩
- 自动计算GPA
- 成绩统计分析

### 📅 课表查询

- 按星期查询课表
- 查看完整周课表
- 今日课表快速查看
- 空闲时间段查询

### 🏫 教室查询

- 查询当前可用空教室
- 教室搜索功能
- 教室状态查询

### 📝 考试查询

- 查询考试安排
- 按科目筛选
- 即将到来的考试提醒
- 考试摘要统计

### 📢 通知查询

- 查询最新校园通知
- 通知数量自定义
- 重要通知筛选
- 通知分类查看

## 🔧 技术栈

- **后端框架**：LangGraph + LangChain
- **大模型**：智谱AI GLM-4
- **前端界面**：Gradio
- **数据存储**：JSON文件（模拟数据）
- **日志系统**：Python logging
- **对话记忆**：自定义内存管理

## 📝 开发指南

### 添加新功能模块

1. 继承 `BaseFeature` 类：

```python
from features.base_feature import BaseFeature

class NewFeature(BaseFeature):
    def __init__(self):
        super().__init__(
            name="新功能",
            description="功能描述"
        )
    
    def execute(self, **kwargs):
        # 实现功能逻辑
        return {"success": True, "message": "执行结果"}
    
    def get_ui_components(self):
        # 返回UI组件配置
        return {}
```

2. 在 `features/__init__.py` 中注册新功能

3. 在 `ui/gradio_ui.py` 中添加对应的UI创建方法

### 扩展知识库

```python
from utils.knowledge_base import KnowledgeBase

kb = KnowledgeBase()
kb.add_knowledge(
    question="如何申请图书馆？",
    answer="图书馆申请需要...",
    category="图书馆",
    keywords=["图书馆", "申请", "借书"]
)
```

## 🐛 常见问题

### 1. API密钥错误

确保在 `config.py` 中正确设置了智谱AI的API密钥。

### 2. 依赖包安装失败

尝试使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 端口被占用

修改 `config.py` 中的端口配置：
```python
UI_PORT = 7861  # 修改为其他端口
```

## 🔄 版本历史

### v2.0.0 (2026-06-04)

- 🎉 重大重构：采用多功能模块化设计
- ✨ 新增对话记忆功能
- ✨ 新增知识库支持
- 🎨 全新UI设计：左侧侧边栏导航
- 🔧 代码规范化：添加类型提示和完整注释
- 📝 完善日志系统和异常处理

### v1.0.0 (初始版本)

- 基础的智能体功能
- 简单的Gradio界面
- 基本的查询工具

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

蔡华兵 - 校园信息智能查询系统开发

## 🙏 致谢

- [智谱AI](https://open.bigmodel.cn/) - 提供大模型API支持
- [LangChain](https://github.com/langchain-ai/langchain) - 强大的LLM开发框架
- [Gradio](https://gradio.app/) - 优秀的机器学习界面框架

---

**注意**：本项目当前使用模拟数据，实际部署时需要对接真实的校园信息系统。
