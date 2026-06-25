# 校园信息智能查询系统

> 基于 Flask + LangGraph 的多功能模块化校园服务平台，支持自然语言查询成绩、课表、教室、考试、通知等信息

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Flask](https://img.shields.io/badge/Flask-3.0+-orange.svg)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-red.svg)](https://www.langchain.com/)

## 项目简介

本项目是一个基于 Flask + LangGraph 构建的校园信息智能查询系统，采用**多功能模块化设计**，面向学生、教师与管理员提供一站式校园服务。

系统通过大模型 API（如智谱 GLM-4、DeepSeek 等）实现自然语言意图识别，自动调用封装的查询工具，支持以下功能：

- 📊 成绩查询（GPA 计算、学期成绩统计）
- 📅 课表查询（今日课表、周课表、课程详情）
- 🏫 教室查询（空教室搜索、教室状态）
- 📝 考试查询（考试安排、时间地点）
- 📢 通知查询（校园公告、分类筛选）
- 🎓 选课查询（选课状态、选课指南）

### 核心特性

- 🤖 **AI 智能助手**：基于 LangGraph 和大模型的智能对话系统
- 💬 **多轮对话**：支持对话上下文记忆，智能关联上下文
- 🎨 **现代化 UI**：基于 Bootstrap 5 的响应式网页界面
- 🔧 **模块化设计**：各功能模块独立，易于扩展和维护
- 📱 **会话管理**：支持多会话切换、历史记录保存
- 🔄 **多模型支持**：支持智谱 GLM-4、DeepSeek 等多种大模型

## 项目结构

```
campus-info-agent/
├── app.py                 # Flask 应用主入口
├── config.py              # 系统配置文件
├── requirements.txt       # Python 依赖包
├── Dockerfile              # Docker 部署配置
│
├── features/              # 功能模块目录
│   ├── __init__.py
│   ├── base_feature.py    # 功能模块基类
│   ├── agent_feature.py   # AI 智能助手
│   ├── grade_feature.py   # 成绩查询
│   ├── schedule_feature.py # 课表查询
│   ├── classroom_feature.py # 教室查询
│   ├── exam_feature.py    # 考试查询
│   ├── notice_feature.py  # 通知查询
│   ├── selection_feature.py # 选课查询
│   └── langgraph_agent.py # LangGraph 智能体
│
├── utils/                 # 工具模块目录
│   ├── __init__.py
│   ├── logger.py          # 日志记录
│   ├── memory.py          # 对话记忆
│   ├── knowledge_base.py  # 知识库管理
│   ├── data_loader.py     # 数据加载器
│   ├── database.py        # 数据库工具
│   └── session_manager.py # 会话管理
│
├── templates/             # HTML 模板
│   ├── login.html         # 登录页面
│   ├── dashboard.html     # 主页面
│   └── settings.html      # 设置页面
│
├── data/                  # 数据目录
│   ├── mock_data.py       # 模拟数据
│   ├── manual_data.json   # 手动导入数据
│   ├── knowledge_base.json # 知识库
│   ├── selections.json     # 选课数据
│   ├── user_data.py       # 用户数据
│   ├── users.json         # 用户账户
│   ├── sessions/          # 会话记录（不提交）
│   ├── 成绩/              # 真实成绩数据
│   ├── 考试安排/          # 真实考试数据
│   └── 课程/              # 真实课程数据
│
├── scripts/               # 脚本目录
│   └── export_data.py     # 数据导出脚本
│
└── logs/                  # 日志目录（不提交）
```

## 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/campus-info-agent.git
cd campus-info-agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或使用国内镜像：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 配置 API 密钥

复制配置文件并填写你的 API 密钥：

```bash
cp config_example.py config.py
```

编辑 `config.py` 文件：

```python
# 智谱 AI 配置
ZHIPU_API_KEY = "your_api_key_here"

# 或 DeepSeek 配置
DEEPSEEK_API_KEY = "your_api_key_here"

# 设置默认 AI 服务
DEFAULT_AI_SERVICE = "zhipu"  # 可选: zhipu, deepseek, siliconflow, alibaba
```

> 💡 获取 API 密钥：
> - 智谱 AI：https://open.bigmodel.cn/
> - DeepSeek：https://platform.deepseek.com/

### 4. 启动系统

```bash
python app.py
```

启动后访问 `http://127.0.0.1:5000`，使用测试账号登录：

- **管理员账号**：用户名 `admin` / 密码 `admin123`
- **学生账号**：用户名 `student` / 密码 `student123`

### 5. Docker 部署（可选）

```bash
docker build -t campus-info-agent .
docker run -p 5000:5000 campus-info-agent
```

## 功能演示

### AI 智能助手对话

```
用户：查询我的成绩
助手：好的，我来帮你查询成绩信息...
      📊 2025-2026学年第1学期成绩
      - Spark大数据技术：93分（优秀）
      - 离散数学：94分（优秀）
      - ...

用户：那我的课表呢？
助手：根据上下文，为你查询本周课表...
      📅 周一课表
      - 第1-2节：习近平新时代中国特色社会主义思想概论
      - 第3-4节：Web前端编程
      ...
```

### 功能模块

| 模块 | 功能 | 说明 |
|------|------|------|
| 成绩查询 | 按学期/课程查询、GPA 计算 | 支持成绩统计和分析 |
| 课表查询 | 今日/周课表、课程详情 | 显示上课时间地点 |
| 教室查询 | 空教室搜索、状态查询 | 教学楼/楼层筛选 |
| 考试查询 | 考试安排、时间地点 | 支持按课程筛选 |
| 通知查询 | 校园公告、分类筛选 | 重要通知提醒 |
| 选课查询 | 选课状态、选课指南 | 查看已选课程 |

## 技术栈

| 分类 | 技术 | 说明 |
|------|------|------|
| 后端框架 | Flask 3.0+ | Web 框架 |
| AI 框架 | LangChain + LangGraph | 大模型应用开发 |
| 大模型 | 智谱 GLM-4 / DeepSeek | 自然语言处理 |
| 前端 | Bootstrap 5 + HTML/CSS/JS | 响应式界面 |
| 数据存储 | JSON 文件 | 本地数据存储 |
| 日志系统 | Python logging | 运行日志记录 |

## 配置说明

### 数据源配置

系统支持三种数据源模式，修改 `config.py` 中的 `DATA_SOURCE`：

```python
DATA_SOURCE = "manual"  # 可选值:

# mock - 使用内置模拟数据（默认，适合测试）
# manual - 使用 data/manual_data.json 中的数据
# cuit - 对接成都信息工程大学教务系统（需要配置账号密码）
```

### 多模型配置

系统支持配置多个 AI 服务，按优先级自动切换：

```python
# 模型降级策略
MODEL_TIER_ORDER = ["online", "local", "rules"]

# 当在线模型失败次数超过阈值时，自动降级
MAX_FAILURES_BEFORE_SWITCH = 5
```

### 功能开关

```python
ENABLE_MEMORY = True           # 启用对话记忆
ENABLE_KNOWLEDGE_BASE = True   # 启用知识库
ENABLE_FALLBACK = True         # 启用本地规则降级
```

## 开发指南

### 添加新功能模块

1. 继承 `BaseFeature` 类创建新模块：

```python
# features/new_feature.py
from .base_feature import BaseFeature

class NewFeature(BaseFeature):
    def __init__(self):
        super().__init__(
            name="新功能",
            description="功能描述"
        )
    
    def execute(self, **kwargs):
        # 实现功能逻辑
        return {"success": True, "message": "执行结果"}
```

2. 在 `features/__init__.py` 中注册

3. 在 `app.py` 的 `features` 字典中添加实例

### 扩展知识库

编辑 `data/knowledge_base.json` 添加新知识：

```json
{
  "knowledge_items": [
    {
      "question": "常见问题？",
      "answer": "这里是回答内容...",
      "category": "分类",
      "keywords": ["关键词1", "关键词2"]
    }
  ]
}
```

## 常见问题

### Q: API 密钥错误或失效？

确保在 `config.py` 中正确设置了有效的 API 密钥，且账户有足够的 API 调用配额。

### Q: 依赖包安装失败？

```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或升级 pip
pip install --upgrade pip
```

### Q: 端口被占用？

修改 `app.py` 中的端口：

```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Q: 如何获取真实成绩数据？

1. 将 Excel 成绩文件放入 `data/成绩/` 目录
2. 将考试安排文件放入 `data/考试安排/` 目录
3. 将课程表文件放入 `data/课程/` 目录
4. 修改 `config.py` 中 `DATA_SOURCE = "manual"`

## 版本历史

### v3.0.0 (2026-06-25)

- 🎉 重构为 Flask Web 应用
- ✨ 新增会话管理功能
- 🎨 全新 Bootstrap 5 界面
- 🔧 优化模块化架构
- 📝 完善文档和注释

### v2.0.0

- 🤖 基于 LangGraph 的智能体
- 💬 多轮对话记忆
- 📚 知识库支持

### v1.0.0

- 初始版本
- 基础查询功能

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 致谢

- [智谱 AI](https://open.bigmodel.cn/) - 提供 GLM-4 大模型 API
- [DeepSeek](https://platform.deepseek.com/) - 提供 DeepSeek 大模型
- [LangChain](https://github.com/langchain-ai/langchain) - LLM 应用开发框架
- [Bootstrap](https://getbootstrap.com/) - 前端 UI 框架

---

**注意**：本项目默认使用模拟数据。部署时建议：
1. 使用模拟数据进行开发和测试
2. 替换 `config.py` 中的 API 密钥为你的密钥
3. 如需真实数据，按照上述说明导入 Excel 文件
