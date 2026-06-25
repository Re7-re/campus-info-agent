"""
智能体功能模块
集成LangGraph智能体，支持自然语言查询成绩、课表、教室、考试等信息
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from .base_feature import BaseFeature
from .langgraph_agent import LangGraphAgent
from utils.memory import ConversationMemory
from utils.knowledge_base import KnowledgeBase
from utils.session_manager import SessionManager
from utils.logger import get_logger
from config import Config


class AgentFeature(BaseFeature):
    """
    智能体功能模块
    基于LangGraph的智能对话系统
    """
    
    def __init__(self):
        super().__init__(
            name="智能助手",
            description="AI智能对话助手，支持自然语言查询"
        )
        
        self.logger = get_logger("agent_feature")
        
        self.memory = ConversationMemory()
        self.knowledge_base = KnowledgeBase()
        
        self.session_manager = SessionManager()
        self.session_manager.create_session("默认会话")
        
        self.langgraph_agent = LangGraphAgent()
        
        self.logger.info("智能体功能模块初始化完成")
    
    def _generate_session_title(self, message: str) -> str:
        """根据用户消息智能生成会话标题"""
        if not message or not isinstance(message, str):
            return ""
        
        message = message.strip()
        
        keywords = [
            ("成绩", "成绩查询"),
            ("分数", "成绩查询"),
            ("课表", "课程表"),
            ("课程", "课程查询"),
            ("教室", "教室查询"),
            ("考试", "考试安排"),
            ("通知", "通知查询"),
            ("作业", "作业查询"),
            ("选课", "选课查询"),
            ("GPA", "GPA计算"),
            ("绩点", "绩点查询"),
            ("老师", "教师查询"),
            ("时间", "时间查询"),
            ("地点", "地点查询"),
            ("安排", "安排查询"),
            ("查询", "信息查询"),
            ("帮助", "帮助中心"),
            ("问题", "问题咨询"),
            ("关于", "关于咨询"),
        ]
        
        for keyword, title in keywords:
            if keyword in message:
                return title
        
        max_length = 20
        if len(message) <= max_length:
            return message
        return message[:max_length] + "..."
    
    def execute(self, message: str, use_memory: bool = True, **kwargs) -> Dict[str, Any]:
        """执行智能体对话"""
        try:
            self.logger.info("收到用户消息: {}".format(message))
            
            history = []
            current_session = self.session_manager.get_current_session()
            if current_session and use_memory:
                history_messages = current_session.get_messages()
                for msg in history_messages:
                    history.append(msg["content"])
            
            response_content = self.langgraph_agent.run(message, history)
            
            self.session_manager.add_message_to_current("user", message)
            self.session_manager.add_message_to_current("assistant", response_content)
            
            if current_session:
                default_titles = ["新会话", "默认会话", "会话 {}".format(datetime.now().strftime('%H:%M:%S'))]
                if current_session.title in default_titles or current_session.title.startswith("会话 "):
                    title = self._generate_session_title(message)
                    if title:
                        current_session.update_title(title)
            
            self.session_manager.save_current_session()
            
            return {
                "success": True,
                "message": response_content,
                "use_memory": use_memory,
                "conversation_length": len(self.memory.conversation_history)
            }
            
        except Exception as e:
            error_msg = "智能体执行出错: {}".format(str(e))
            self.logger.error(error_msg)
            
            self.session_manager.add_message_to_current("user", message)
            self.session_manager.add_message_to_current("assistant", "抱歉，我出错了：{}".format(error_msg))
            self.session_manager.save_current_session()
            
            return {
                "success": False,
                "message": "抱歉，我出错了：{}".format(error_msg),
                "error": str(e)
            }
    
    def list_sessions(self) -> list:
        """列出所有会话"""
        return self.session_manager.list_sessions()
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """获取指定会话"""
        return self.session_manager.get_session(session_id)
    
    def delete_session(self, session_id: str) -> bool:
        """删除指定会话"""
        return self.session_manager.delete_session(session_id)
    
    def clear_memory(self):
        """清空记忆"""
        self.memory.clear()
        self.session_manager.clear_all_sessions()
        self.session_manager.create_session("默认会话")
    
    def get_conversation_history(self) -> list:
        """获取对话历史"""
        return self.memory.conversation_history
    
    def set_model(self, model_name: str):
        """设置模型名称"""
        self.logger.info("设置模型: {}".format(model_name))
        
        model_map = {
            "deepseek-v4-pro": "deepseek-v4-pro",
            "deepseek-chat": "deepseek-chat",
            "zhipu-glm-4": "glm-4",
            "zhipu-glm-4-flash": "glm-4-flash"
        }
        
        actual_model = model_map.get(model_name, model_name)
        self.langgraph_agent = LangGraphAgent(model_name=actual_model)
    
    def switch_session(self, session_id: str):
        """切换会话"""
        self.session_manager.switch_session(session_id)
    
    def get_ui_components(self) -> Dict[str, Any]:
        """获取UI组件配置"""
        return {
            "type": "chat",
            "name": self.name,
            "description": self.description,
            "icon": "🤖",
            "placeholder": "问我关于成绩、课表、教室、考试等问题吧~"
        }
