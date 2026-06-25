"""
对话记忆模块 - 双层记忆架构
短期上下文窗口 + 长期持久记忆
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os
import sqlite3
from config import Config


class SessionMetadata:
    """
    会话元数据存储 - SQLite持久化
    """
    
    def __init__(self, db_path: str = "data/campus_info.db"):
        self.db_path = db_path
        self._init_table()
    
    def _init_table(self):
        """初始化会话元数据表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session_metadata (
                session_id TEXT PRIMARY KEY,
                user_id TEXT DEFAULT 'admin',
                created_at TEXT,
                updated_at TEXT,
                message_count INTEGER DEFAULT 0,
                token_usage INTEGER DEFAULT 0,
                model_used TEXT DEFAULT '',
                feature_distribution TEXT DEFAULT '{}',
                data_source TEXT DEFAULT 'manual'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_session(self, session_id: str, user_id: str = 'admin', **kwargs):
        """保存会话元数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT OR REPLACE INTO session_metadata 
            (session_id, user_id, created_at, updated_at, message_count, 
             token_usage, model_used, feature_distribution, data_source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_id,
            user_id,
            kwargs.get('created_at', now),
            now,
            kwargs.get('message_count', 0),
            kwargs.get('token_usage', 0),
            kwargs.get('model_used', ''),
            kwargs.get('feature_distribution', '{}'),
            kwargs.get('data_source', 'manual')
        ))
        
        conn.commit()
        conn.close()
    
    def update_session(self, session_id: str, **kwargs):
        """更新会话元数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        update_fields = []
        params = []
        
        if 'message_count' in kwargs:
            update_fields.append('message_count = message_count + ?')
            params.append(kwargs['message_count'])
        if 'token_usage' in kwargs:
            update_fields.append('token_usage = token_usage + ?')
            params.append(kwargs['token_usage'])
        if 'model_used' in kwargs:
            update_fields.append('model_used = ?')
            params.append(kwargs['model_used'])
        if 'feature_distribution' in kwargs:
            update_fields.append('feature_distribution = ?')
            params.append(kwargs['feature_distribution'])
        
        params.append(session_id)
        
        cursor.execute(f'''
            UPDATE session_metadata 
            SET updated_at = ?, {', '.join(update_fields)}
            WHERE session_id = ?
        ''', (datetime.now().isoformat(), *params))
        
        conn.commit()
        conn.close()
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """获取会话元数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM session_metadata WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'session_id': row[0],
                'user_id': row[1],
                'created_at': row[2],
                'updated_at': row[3],
                'message_count': row[4],
                'token_usage': row[5],
                'model_used': row[6],
                'feature_distribution': json.loads(row[7]),
                'data_source': row[8]
            }
        return None
    
    def get_all_sessions(self, user_id: str = None) -> List[Dict]:
        """获取所有会话列表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('SELECT * FROM session_metadata WHERE user_id = ? ORDER BY updated_at DESC', (user_id,))
        else:
            cursor.execute('SELECT * FROM session_metadata ORDER BY updated_at DESC')
        
        rows = cursor.fetchall()
        conn.close()
        
        sessions = []
        for row in rows:
            sessions.append({
                'session_id': row[0],
                'user_id': row[1],
                'created_at': row[2],
                'updated_at': row[3],
                'message_count': row[4],
                'token_usage': row[5],
                'model_used': row[6],
                'feature_distribution': json.loads(row[7]),
                'data_source': row[8]
            })
        return sessions


class DualMemory:
    """
    双层记忆架构
    - 短期上下文窗口：20轮原始对话，超过自动生成全局摘要
    - 长期持久记忆：SQLite存储元数据 + JSON完整存档
    """
    
    SHORT_TERM_WINDOW = 20  # 短期上下文窗口大小
    
    def __init__(self, user_id: str = 'admin', session_id: str = None):
        """
        初始化双层记忆
        
        Args:
            user_id: 用户ID
            session_id: 会话ID（可选，不传则自动生成）
        """
        self.user_id = user_id
        self.session_id = session_id or self._generate_session_id()
        self.save_dir = Config.MEMORY_DIR
        
        # 短期记忆：原始对话
        self.short_term_history: List[Dict[str, Any]] = []
        
        # 全局摘要
        self.global_summary = ""
        
        # 长期记忆：元数据存储
        self.metadata_store = SessionMetadata()
        
        # 确保保存目录存在
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # 初始化会话元数据
        self._init_session()
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _init_session(self):
        """初始化会话元数据"""
        existing = self.metadata_store.get_session(self.session_id)
        if not existing:
            self.metadata_store.save_session(
                session_id=self.session_id,
                user_id=self.user_id,
                created_at=datetime.now().isoformat(),
                message_count=0,
                token_usage=0
            )
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        添加消息到双层记忆
        
        Args:
            role: 消息角色 (user/assistant/system/tool)
            content: 消息内容
            metadata: 额外的元数据（token消耗、模型类型、功能调用等）
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        # 添加到短期记忆
        self.short_term_history.append(message)
        
        # 更新元数据
        self.metadata_store.update_session(
            session_id=self.session_id,
            message_count=1
        )
        
        if metadata:
            if 'token_usage' in metadata:
                self.metadata_store.update_session(
                    session_id=self.session_id,
                    token_usage=metadata['token_usage']
                )
            if 'model_used' in metadata:
                self.metadata_store.update_session(
                    session_id=self.session_id,
                    model_used=metadata['model_used']
                )
            if 'feature_used' in metadata:
                self._update_feature_distribution(metadata['feature_used'])
        
        # 检查是否需要生成摘要
        if len(self.short_term_history) >= self.SHORT_TERM_WINDOW:
            self._generate_global_summary()
    
    def _update_feature_distribution(self, feature_name: str):
        """更新功能使用分布"""
        session = self.metadata_store.get_session(self.session_id)
        if session:
            dist = session.get('feature_distribution', {})
            dist[feature_name] = dist.get(feature_name, 0) + 1
            self.metadata_store.update_session(
                session_id=self.session_id,
                feature_distribution=json.dumps(dist)
            )
    
    def _generate_global_summary(self):
        """生成全局摘要，压缩长期对话历史"""
        if len(self.short_term_history) < 10:
            return
        
        # 取最近10轮对话生成摘要
        recent_messages = self.short_term_history[-10:]
        
        summary_lines = []
        for msg in recent_messages:
            role_label = "用户" if msg["role"] == "user" else "助手"
            summary_lines.append(f"{role_label}: {msg['content'][:100]}")
        
        self.global_summary = "\n".join(summary_lines)
        
        # 压缩短期记忆，只保留最近20轮
        self.short_term_history = self.short_term_history[-self.SHORT_TERM_WINDOW:]
    
    def get_context_for_llm(self) -> List[Dict[str, str]]:
        """
        获取送入大模型的上下文
        
        Returns:
            上下文消息列表（系统摘要 + 最近对话）
        """
        messages = []
        
        # 添加全局摘要（如果存在）
        if self.global_summary:
            messages.append({
                "role": "system",
                "content": f"对话历史摘要：\n{self.global_summary}\n\n请根据以上摘要理解对话上下文。"
            })
        
        # 添加最近10轮原始对话
        recent_history = self.short_term_history[-10:]
        for msg in recent_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return messages
    
    def get_visualization_data(self) -> Dict[str, Any]:
        """
        获取前端可视化面板数据
        
        Returns:
            可视化数据字典
        """
        session = self.metadata_store.get_session(self.session_id)
        
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "global_summary": self.global_summary[:500] if self.global_summary else "暂无摘要",
            "recent_messages": self.short_term_history[-10:],
            "message_count": len(self.short_term_history),
            "metadata": session or {}
        }
    
    def get_history(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取对话历史"""
        if last_n is None:
            return self.short_term_history.copy()
        return self.short_term_history[-last_n:]
    
    def get_last_user_message(self) -> Optional[str]:
        """获取最后一条用户消息"""
        for msg in reversed(self.short_term_history):
            if msg["role"] == "user":
                return msg["content"]
        return None
    
    def clear_history(self):
        """清空对话历史"""
        self.short_term_history = []
        self.global_summary = ""
    
    def save_to_file(self, filename: Optional[str] = None):
        """保存对话历史到文件"""
        if filename is None:
            filename = f"conversation_{self.session_id}.json"
        
        filepath = os.path.join(self.save_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "user_id": self.user_id,
                "global_summary": self.global_summary,
                "conversation_history": self.short_term_history,
                "saved_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, filename: str):
        """从文件加载对话历史"""
        filepath = os.path.join(self.save_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.session_id = data.get("session_id", self._generate_session_id())
                self.user_id = data.get("user_id", 'admin')
                self.global_summary = data.get("global_summary", "")
                self.short_term_history = data.get("conversation_history", [])


# 兼容旧接口
class ConversationMemory(DualMemory):
    """兼容旧版对话记忆类"""
    
    def __init__(self, user_id: str = 'admin', session_id: str = None):
        super().__init__(user_id, session_id)
        self.max_history = 100
    
    @property
    def conversation_history(self):
        """获取对话历史（兼容旧接口）"""
        return self.short_term_history
    
    def get_context_summary(self, max_tokens: int = 300):
        """获取对话上下文摘要（兼容旧接口）"""
        if not self.short_term_history:
            return "暂无对话历史"
        
        summary_lines = []
        for msg in self.short_term_history[-5:]:
            role_label = "用户" if msg["role"] == "user" else "助手"
            content = msg["content"][:50] if len(msg["content"]) > 50 else msg["content"]
            summary_lines.append(f"{role_label}: {content}")
        
        return "\n".join(summary_lines)