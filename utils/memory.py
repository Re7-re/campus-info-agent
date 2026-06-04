"""
对话记忆模块
提供对话历史记录和检索功能
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os


class ConversationMemory:
    """
    对话记忆类，用于存储和检索对话历史
    """
    
    def __init__(self, max_history: int = 50, save_dir: str = "memory"):
        """
        初始化对话记忆
        
        Args:
            max_history: 最大保存的对话历史数量
            save_dir: 对话历史保存目录
        """
        self.max_history = max_history
        self.save_dir = save_dir
        self.conversation_history: List[Dict[str, Any]] = []
        self.session_id = self._generate_session_id()
        
        # 确保保存目录存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        添加消息到对话历史
        
        Args:
            role: 消息角色 (user/assistant/system)
            content: 消息内容
            metadata: 额外的元数据
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversation_history.append(message)
        
        # 限制历史记录数量
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]
    
    def get_history(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        获取对话历史
        
        Args:
            last_n: 获取最近n条记录，如果为None则返回全部
        
        Returns:
            对话历史列表
        """
        if last_n is None:
            return self.conversation_history.copy()
        return self.conversation_history[-last_n:]
    
    def get_last_user_message(self) -> Optional[str]:
        """获取最后一条用户消息"""
        for msg in reversed(self.conversation_history):
            if msg["role"] == "user":
                return msg["content"]
        return None
    
    def get_last_assistant_message(self) -> Optional[str]:
        """获取最后一条助手消息"""
        for msg in reversed(self.conversation_history):
            if msg["role"] == "assistant":
                return msg["content"]
        return None
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
    
    def save_to_file(self, filename: Optional[str] = None):
        """
        保存对话历史到文件
        
        Args:
            filename: 文件名，如果为None则使用会话ID
        """
        if filename is None:
            filename = f"conversation_{self.session_id}.json"
        
        filepath = os.path.join(self.save_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "conversation_history": self.conversation_history,
                "saved_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filename: str):
        """
        从文件加载对话历史
        
        Args:
            filename: 文件名
        """
        filepath = os.path.join(self.save_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.session_id = data.get("session_id", self._generate_session_id())
                self.conversation_history = data.get("conversation_history", [])
    
    def get_context_summary(self, max_tokens: int = 500) -> str:
        """
        获取对话历史的摘要
        
        Args:
            max_tokens: 最大token数
        
        Returns:
            对话摘要
        """
        if not self.conversation_history:
            return "暂无对话历史"
        
        summary_parts = []
        current_length = 0
        
        # 从最近的对话开始构建摘要
        for msg in reversed(self.conversation_history):
            msg_text = f"{msg['role']}: {msg['content']}"
            
            if current_length + len(msg_text) > max_tokens:
                break
            
            summary_parts.insert(0, msg_text)
            current_length += len(msg_text)
        
        return "\n".join(summary_parts)