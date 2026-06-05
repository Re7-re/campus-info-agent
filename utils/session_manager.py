"""
会话管理模块
提供会话创建、保存、加载、历史记录等功能
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from utils.logger import get_logger


class Session:
    """会话类"""
    
    def __init__(self, session_id: str, title: str = "新会话"):
        """
        初始化会话
        
        Args:
            session_id: 会话ID
            title: 会话标题
        """
        self.session_id = session_id
        self.title = title
        self.messages: List[Dict[str, str]] = []
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at
        self.metadata: Dict[str, Any] = {}
    
    def add_message(self, role: str, content: str):
        """
        添加消息到会话
        
        Args:
            role: 消息角色 (user/assistant)
            content: 消息内容
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_messages(self) -> List[Dict[str, str]]:
        """获取会话所有消息"""
        return self.messages
    
    def get_last_messages(self, count: int = 5) -> List[Dict[str, str]]:
        """获取最后几条消息"""
        return self.messages[-count:] if self.messages else []
    
    def update_title(self, title: str):
        """更新会话标题"""
        self.title = title
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "session_id": self.session_id,
            "title": self.title,
            "messages": self.messages,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        """从字典创建会话"""
        session = cls(data["session_id"], data["title"])
        session.messages = data["messages"]
        session.created_at = data["created_at"]
        session.updated_at = data["updated_at"]
        session.metadata = data.get("metadata", {})
        return session


class SessionManager:
    """会话管理器"""
    
    def __init__(self, sessions_dir: str = "data/sessions"):
        """
        初始化会话管理器
        
        Args:
            sessions_dir: 会话存储目录
        """
        self.logger = get_logger("session_manager")
        self.sessions_dir = sessions_dir
        self.current_session: Optional[Session] = None
        self.session_history: Dict[str, Session] = {}
        
        # 确保目录存在
        os.makedirs(sessions_dir, exist_ok=True)
        
        # 加载历史会话
        self._load_sessions()
        
        self.logger.info("会话管理器初始化完成")
    
    def _load_sessions(self):
        """加载历史会话"""
        try:
            if os.path.exists(self.sessions_dir):
                for filename in os.listdir(self.sessions_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(self.sessions_dir, filename)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            session = Session.from_dict(data)
                            self.session_history[session.session_id] = session
                self.logger.info(f"加载了 {len(self.session_history)} 个历史会话")
        except Exception as e:
            self.logger.error(f"加载历史会话失败: {str(e)}")
    
    def _save_session(self, session: Session):
        """保存会话到文件"""
        try:
            filepath = os.path.join(self.sessions_dir, f"{session.session_id}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(session.to_dict(), f, ensure_ascii=False, indent=2)
            self.logger.info(f"会话 {session.session_id} 保存成功")
        except Exception as e:
            self.logger.error(f"保存会话失败: {str(e)}")
    
    def create_session(self, title: str = "新会话") -> Session:
        """
        创建新会话
        
        Args:
            title: 会话标题
        
        Returns:
            新创建的会话
        """
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        session = Session(session_id, title)
        self.session_history[session_id] = session
        self.current_session = session
        
        self.logger.info(f"创建新会话: {session_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """
        获取指定会话
        
        Args:
            session_id: 会话ID
        
        Returns:
            会话对象，不存在返回None
        """
        return self.session_history.get(session_id)
    
    def switch_session(self, session_id: str) -> bool:
        """
        切换到指定会话
        
        Args:
            session_id: 会话ID
        
        Returns:
            是否切换成功
        """
        session = self.get_session(session_id)
        if session:
            self.current_session = session
            self.logger.info(f"切换到会话: {session_id}")
            return True
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        删除指定会话
        
        Args:
            session_id: 会话ID
        
        Returns:
            是否删除成功
        """
        if session_id in self.session_history:
            del self.session_history[session_id]
            
            # 删除文件
            filepath = os.path.join(self.sessions_dir, f"{session_id}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
            
            # 如果删除的是当前会话，清空当前会话
            if self.current_session and self.current_session.session_id == session_id:
                self.current_session = None
            
            self.logger.info(f"删除会话: {session_id}")
            return True
        return False
    
    def save_current_session(self) -> bool:
        """
        保存当前会话
        
        Returns:
            是否保存成功
        """
        if self.current_session:
            self._save_session(self.current_session)
            return True
        return False
    
    def get_session_list(self) -> List[Dict[str, Any]]:
        """
        获取会话列表
        
        Returns:
            会话信息列表
        """
        sessions = []
        for session in self.session_history.values():
            sessions.append({
                "session_id": session.session_id,
                "title": session.title,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
                "message_count": len(session.messages),
                "is_current": session.session_id == (self.current_session.session_id if self.current_session else None)
            })
        
        # 按更新时间排序
        sessions.sort(key=lambda x: x["updated_at"], reverse=True)
        return sessions
    
    def get_current_session(self) -> Optional[Session]:
        """获取当前会话"""
        return self.current_session
    
    def add_message_to_current(self, role: str, content: str):
        """
        向当前会话添加消息
        
        Args:
            role: 消息角色
            content: 消息内容
        """
        if self.current_session:
            self.current_session.add_message(role, content)
    
    def update_current_title(self, title: str):
        """
        更新当前会话标题
        
        Args:
            title: 新标题
        """
        if self.current_session:
            self.current_session.update_title(title)
    
    def search_sessions(self, keyword: str) -> List[Dict[str, Any]]:
        """
        搜索会话
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的会话列表
        """
        results = []
        keyword = keyword.lower()
        
        for session in self.session_history.values():
            # 搜索标题
            if keyword in session.title.lower():
                results.append({
                    "session_id": session.session_id,
                    "title": session.title,
                    "created_at": session.created_at,
                    "updated_at": session.updated_at,
                    "message_count": len(session.messages),
                    "match_type": "标题"
                })
                continue
            
            # 搜索消息内容
            for msg in session.messages:
                if keyword in msg["content"].lower():
                    results.append({
                        "session_id": session.session_id,
                        "title": session.title,
                        "created_at": session.created_at,
                        "updated_at": session.updated_at,
                        "message_count": len(session.messages),
                        "match_type": "内容"
                    })
                    break
        
        return results
    
    def export_session(self, session_id: str, format: str = "json") -> Optional[str]:
        """
        导出会话
        
        Args:
            session_id: 会话ID
            format: 导出格式 (json/txt)
        
        Returns:
            导出的内容，失败返回None
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        if format == "json":
            return json.dumps(session.to_dict(), ensure_ascii=False, indent=2)
        elif format == "txt":
            content = f"会话ID: {session.session_id}\n"
            content += f"标题: {session.title}\n"
            content += f"创建时间: {session.created_at}\n"
            content += f"更新时间: {session.updated_at}\n"
            content += "-" * 50 + "\n\n"
            
            for msg in session.messages:
                role_name = "用户" if msg["role"] == "user" else "助手"
                content += f"[{msg['timestamp']}] {role_name}:\n{msg['content']}\n\n"
            
            return content
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取会话统计信息
        
        Returns:
            统计信息字典
        """
        total_sessions = len(self.session_history)
        total_messages = sum(len(session.messages) for session in self.session_history.values())
        
        if self.current_session:
            current_messages = len(self.current_session.messages)
        else:
            current_messages = 0
        
        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "current_session_id": self.current_session.session_id if self.current_session else None,
            "current_messages": current_messages,
            "sessions_dir": self.sessions_dir
        }