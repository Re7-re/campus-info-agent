"""
智能体功能模块
集成LangGraph和大模型，支持对话记忆和知识库
支持本地规则引擎作为降级方案
"""

from typing import Dict, Any, Optional, List
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools import tool

from .base_feature import BaseFeature
from utils.memory import ConversationMemory
from utils.knowledge_base import KnowledgeBase
from utils.session_manager import SessionManager
from utils.logger import get_logger
from config import Config
from agent.local_engine import query_local_engine


class AgentFeature(BaseFeature):
    """
    智能体功能模块
    基于LangGraph和智谱大模型的智能对话系统
    """
    
    def __init__(self):
        super().__init__(
            name=" 智能助手",
            description="AI智能对话助手，支持自然语言查询"
        )
        
        # 初始化日志
        self.logger = get_logger("agent_feature")
        
        # 初始化记忆和知识库
        self.memory = ConversationMemory()
        self.knowledge_base = KnowledgeBase()
        
        # 初始化会话管理器
        self.session_manager = SessionManager()
        # 创建默认会话
        self.session_manager.create_session("默认会话")
        
        # 初始化大模型（根据配置选择AI服务）
        service = Config.DEFAULT_AI_SERVICE
        if service == "zhipu":
            self.llm = ChatOpenAI(
                api_key=Config.ZHIPU_API_KEY,
                model=Config.ZHIPU_MODEL_NAME,
                base_url=Config.ZHIPU_API_BASE,
                temperature=0.7
            )
        elif service == "siliconflow":
            self.llm = ChatOpenAI(
                api_key=Config.SILICONFLOW_API_KEY,
                model=Config.SILICONFLOW_MODEL_NAME,
                base_url=Config.SILICONFLOW_API_BASE,
                temperature=0.7
            )
        elif service == "deepseek":
            self.llm = ChatOpenAI(
                api_key=Config.DEEPSEEK_API_KEY,
                model=Config.DEEPSEEK_MODEL_NAME,
                base_url=Config.DEEPSEEK_API_BASE,
                temperature=0.7
            )
        elif service == "longchat":
            self.llm = ChatOpenAI(
                api_key=Config.LONGCHAT_API_KEY,
                model=Config.LONGCHAT_MODEL_NAME,
                base_url=Config.LONGCHAT_API_BASE,
                temperature=0.7
            )
        elif service == "alibaba":
            self.llm = ChatOpenAI(
                api_key=Config.ALIBABA_API_KEY,
                model=Config.ALIBABA_MODEL_NAME,
                base_url=Config.ALIBABA_API_BASE,
                temperature=0.7,
                request_timeout=60  # 设置 60 秒超时
            )
        else:
            # 默认使用阿里云百炼
            self.llm = ChatOpenAI(
                api_key=Config.ALIBABA_API_KEY,
                model=Config.ALIBABA_MODEL_NAME,
                base_url=Config.ALIBABA_API_BASE,
                temperature=0.7,
                request_timeout=30  # 设置 30 秒超时
            )
        
        # 创建工具
        self.tools = self._create_tools()
        
        # 绑定工具
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # 构建LangGraph流程
        self.agent = self._build_agent()
        
        self.logger.info("智能体功能模块初始化完成")
    
    def _create_tools(self) -> List:
        """创建智能体工具"""
        from features.grade_feature import GradeFeature
        from features.schedule_feature import ScheduleFeature
        from features.classroom_feature import ClassroomFeature
        from features.exam_feature import ExamFeature
        from features.notice_feature import NoticeFeature
        
        # 初始化各功能模块
        grade_feature = GradeFeature()
        schedule_feature = ScheduleFeature()
        classroom_feature = ClassroomFeature()
        exam_feature = ExamFeature()
        notice_feature = NoticeFeature()
        
        @tool
        def query_grade(term: str = None):
            """查询学生成绩，支持按学期查询，不传参数返回全部成绩"""
            result = grade_feature.execute(term=term)
            return result.get("message", "查询失败")
        
        @tool
        def query_schedule(day: str = None):
            """查询课表，支持按星期查询，不传参数返回全部课表"""
            result = schedule_feature.execute(day=day)
            return result.get("message", "查询失败")
        
        @tool
        def query_classroom():
            """查询当前可用的空教室"""
            result = classroom_feature.execute()
            return result.get("message", "查询失败")
        
        @tool
        def query_exam(subject: str = None):
            """查询期末考试安排，可以指定科目"""
            result = exam_feature.execute(subject=subject)
            return result.get("message", "查询失败")
        
        @tool
        def query_notice(count: int = 5):
            """查询最新校园通知，可以指定返回数量"""
            result = notice_feature.execute(count=count)
            return result.get("message", "查询失败")
        
        @tool
        def search_knowledge(query: str):
            """搜索知识库中的相关信息"""
            results = self.knowledge_base.search(query, top_k=3)
            if results:
                knowledge_text = "\n".join([f"Q: {item.question}\nA: {item.answer}" for item in results])
                return f"相关知识库信息：\n{knowledge_text}"
            return "未找到相关知识库信息"
        
        return [
            query_grade,
            query_schedule,
            query_classroom,
            query_exam,
            query_notice,
            search_knowledge
        ]
    
    def _build_agent(self):
        """构建LangGraph智能体，支持实时思考反馈"""
        # 定义节点
        def agent_node(state: MessagesState):
            try:
                # 添加对话历史上下文
                messages = state["messages"]
                
                # 获取对话历史摘要
                context_summary = self.memory.get_context_summary(max_tokens=300)
                if context_summary and "暂无对话历史" not in context_summary:
                    # 在消息前添加上下文
                    context_message = f"以下是对话历史摘要，可以帮助你更好地理解用户意图：\n{context_summary}\n\n当前用户问题："
                    if messages:
                        messages = [HumanMessage(content=context_message + messages[-1].content)]
                
                # 添加思考提示
                system_prompt = """你是一个专业的校园信息智能助手。在回答问题时，请按照以下步骤进行思考：

1. **理解用户意图**：分析用户想要查询什么信息
2. **选择合适工具**：根据用户需求选择合适的查询工具
3. **执行查询操作**：调用相应的工具获取信息
4. **整理结果**：将查询结果整理成用户友好的格式
5. **提供补充建议**：根据查询结果提供相关建议

请在回答中展示你的思考过程，使用以下格式：
- 🤔 **思考过程**：[你的思考内容]
- 🔧 **执行操作**：[你选择的操作]
- 📊 **查询结果**：[查询结果]
- 💡 **建议**：[相关建议]

如果查询失败，请说明原因并提供替代方案。"""
                
                # 添加系统提示
                messages = [AIMessage(content=system_prompt)] + messages
                
                response = self.llm_with_tools.invoke(messages)
                self.logger.info(f"智能体响应: {response.content[:100]}...")
                return {"messages": [response]}
            except Exception as e:
                self.logger.error(f"智能体节点执行错误: {str(e)}")
                # 重新抛出异常，让外层execute方法可以捕获并降级到本地规则引擎
                raise
        
        # 创建工具节点
        tool_node = ToolNode(self.tools)
        
        # 构建流程
        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", agent_node)
        workflow.add_node("tools", tool_node)
        
        # 判断是否调用工具
        def should_continue(state):
            last_message = state["messages"][-1]
            if last_message.tool_calls:
                return "tools"
            return "__end__"
        
        # 添加边
        workflow.add_conditional_edges("agent", should_continue)
        workflow.add_edge("tools", "agent")
        workflow.set_entry_point("agent")
        
        # 编译
        return workflow.compile()
    
    def execute(self, message: str, use_memory: bool = True, **kwargs) -> Dict[str, Any]:
        """
        执行智能体对话
        
        Args:
            message: 用户消息
            use_memory: 是否使用对话记忆
            **kwargs: 其他参数
        
        Returns:
            响应结果字典
        """
        try:
            self.logger.info(f"收到用户消息: {message}")
            
            # 添加用户消息到记忆
            if use_memory:
                self.memory.add_message("user", message)
            
            # 构建消息列表
            messages = [HumanMessage(content=message)]
            
            # 调用智能体（带降级处理）
            try:
                result = self.agent.invoke({"messages": messages})
                response_content = result["messages"][-1].content
                self.logger.info("使用云API响应")
            except Exception as cloud_error:
                # 云API调用失败，使用本地规则引擎降级
                self.logger.warning(f"云API调用失败，使用本地规则引擎: {str(cloud_error)}")
                response_content = query_local_engine(message)
            
            # 添加助手响应到记忆
            if use_memory:
                self.memory.add_message("assistant", response_content)
            
            # 添加到会话管理
            self.session_manager.add_message_to_current("user", message)
            self.session_manager.add_message_to_current("assistant", response_content)
            
            self.logger.info(f"智能体响应完成: {response_content[:100]}...")
            
            return {
                "success": True,
                "message": response_content,
                "use_memory": use_memory,
                "conversation_length": len(self.memory.conversation_history)
            }
            
        except Exception as e:
            error_msg = f"智能体执行出错: {str(e)}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "error": str(e),
                "message": error_msg
            }
    
    def get_ui_components(self) -> Dict[str, Any]:
        """
        获取UI组件配置
        
        Returns:
            UI组件配置字典
        """
        return {
            "type": "agent_chat",
            "title": "智能助手",
            "description": "AI智能对话助手，支持自然语言查询校园信息",
            "components": [
                {
                    "type": "chatbot",
                    "label": "对话窗口",
                    "key": "chatbot",
                    "height": 550
                },
                {
                    "type": "textbox",
                    "label": "输入消息",
                    "key": "message",
                    "placeholder": "请输入你的问题..."
                },
                {
                    "type": "checkbox",
                    "label": "启用对话记忆",
                    "key": "use_memory",
                    "default": True
                },
                {
                    "type": "button",
                    "label": "发送",
                    "action": "send_message"
                },
                {
                    "type": "button",
                    "label": "清空对话",
                    "action": "clear_chat"
                }
            ]
        }
    
    def clear_memory(self):
        """清空对话记忆"""
        self.memory.clear_history()
        self.logger.info("对话记忆已清空")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """获取对话历史"""
        return self.memory.get_history()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计信息"""
        return {
            "total_messages": len(self.memory.conversation_history),
            "session_id": self.memory.session_id,
            "max_history": self.memory.max_history
        }
    
    def add_knowledge(
        self,
        question: str,
        answer: str,
        category: str,
        keywords: List[str]
    ):
        """
        添加知识到知识库
        
        Args:
            question: 问题
            answer: 答案
            category: 分类
            keywords: 关键词列表
        """
        self.knowledge_base.add_knowledge(question, answer, category, keywords)
        self.logger.info(f"添加知识: {question}")
    
    def search_knowledge(self, query: str, top_k: int = 3) -> List:
        """
        搜索知识库
        
        Args:
            query: 查询文本
            top_k: 返回前k个结果
        
        Returns:
            匹配的知识条目列表
        """
        return self.knowledge_base.search(query, top_k)
    
    # 会话管理方法
    def create_new_session(self, title: str = "新会话") -> Dict[str, Any]:
        """
        创建新会话
        
        Args:
            title: 会话标题
        
        Returns:
            操作结果
        """
        try:
            session = self.session_manager.create_session(title)
            # 清空当前记忆
            self.memory.clear_history()
            
            return {
                "success": True,
                "message": f"新会话 '{title}' 创建成功",
                "session_id": session.session_id
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"创建会话失败: {str(e)}"
            }
    
    def get_session_list(self) -> Dict[str, Any]:
        """
        获取会话列表
        
        Returns:
            会话列表信息
        """
        try:
            sessions = self.session_manager.get_session_list()
            return {
                "success": True,
                "message": f"共找到 {len(sessions)} 个会话",
                "sessions": sessions
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"获取会话列表失败: {str(e)}"
            }
    
    def switch_session(self, session_id: str) -> Dict[str, Any]:
        """
        切换会话
        
        Args:
            session_id: 会话ID
        
        Returns:
            操作结果
        """
        try:
            success = self.session_manager.switch_session(session_id)
            if success:
                session = self.session_manager.get_current_session()
                # 加载会话消息到记忆
                self.memory.clear_history()
                for msg in session.get_messages():
                    self.memory.add_message(msg["role"], msg["content"])
                
                return {
                    "success": True,
                    "message": f"切换到会话 '{session.title}'",
                    "session_id": session_id
                }
            else:
                return {
                    "success": False,
                    "message": "会话不存在"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"切换会话失败: {str(e)}"
            }
    
    def save_current_session(self) -> Dict[str, Any]:
        """
        保存当前会话
        
        Returns:
            操作结果
        """
        try:
            success = self.session_manager.save_current_session()
            if success:
                return {
                    "success": True,
                    "message": "会话保存成功"
                }
            else:
                return {
                    "success": False,
                    "message": "没有当前会话"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"保存会话失败: {str(e)}"
            }
    
    def delete_session(self, session_id: str) -> Dict[str, Any]:
        """
        删除会话
        
        Args:
            session_id: 会话ID
        
        Returns:
            操作结果
        """
        try:
            success = self.session_manager.delete_session(session_id)
            if success:
                return {
                    "success": True,
                    "message": "会话删除成功"
                }
            else:
                return {
                    "success": False,
                    "message": "会话不存在"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"删除会话失败: {str(e)}"
            }
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """
        获取会话统计信息
        
        Returns:
            统计信息
        """
        try:
            stats = self.session_manager.get_statistics()
            return {
                "success": True,
                "message": "统计信息获取成功",
                "statistics": stats
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"获取统计信息失败: {str(e)}"
            }