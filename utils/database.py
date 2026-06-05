"""
数据库管理模块
提供数据库连接、表创建和数据操作功能
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from utils.logger import get_logger


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "data/campus_info.db"):
        """
        初始化数据库管理器
        
        Args:
            db_path: 数据库文件路径
        """
        self.logger = get_logger("database_manager")
        self.db_path = db_path
        
        # 确保目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        self.logger.info("数据库管理器初始化完成")
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_database(self):
        """初始化数据库表结构"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 用户表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        phone TEXT UNIQUE NOT NULL,
                        nickname TEXT,
                        role TEXT DEFAULT 'student',
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                # 成绩表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS grades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        course_name TEXT NOT NULL,
                        course_code TEXT,
                        term TEXT NOT NULL,
                        credit REAL NOT NULL,
                        score REAL NOT NULL,
                        gpa REAL,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                
                # 课表表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS schedules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        course_name TEXT NOT NULL,
                        course_code TEXT,
                        day_of_week TEXT NOT NULL,
                        start_time TEXT NOT NULL,
                        end_time TEXT NOT NULL,
                        location TEXT,
                        teacher TEXT,
                        term TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                
                # 教室表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS classrooms (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        building TEXT NOT NULL,
                        room_number TEXT NOT NULL,
                        capacity INTEGER,
                        has_projector BOOLEAN DEFAULT 0,
                        has_computer BOOLEAN DEFAULT 0,
                        has_air_conditioner BOOLEAN DEFAULT 0,
                        status TEXT DEFAULT 'available',
                        created_at TEXT NOT NULL
                    )
                """)
                
                # 考试表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS exams (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        course_name TEXT NOT NULL,
                        course_code TEXT,
                        exam_date TEXT NOT NULL,
                        start_time TEXT NOT NULL,
                        end_time TEXT NOT NULL,
                        location TEXT,
                        seat_number TEXT,
                        term TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                
                # 通知表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS notices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category TEXT,
                        priority TEXT DEFAULT 'normal',
                        publish_date TEXT NOT NULL,
                        publisher TEXT,
                        is_important BOOLEAN DEFAULT 0,
                        created_at TEXT NOT NULL
                    )
                """)
                
                # 会话表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE NOT NULL,
                        user_id INTEGER,
                        title TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        metadata TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                
                # 会话消息表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS session_messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        FOREIGN KEY (session_id) REFERENCES sessions(session_id)
                    )
                """)
                
                # 知识库表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS knowledge_base (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        category TEXT,
                        keywords TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL
                    )
                """)
                
                conn.commit()
                self.logger.info("数据库表结构初始化完成")
                
        except Exception as e:
            self.logger.error(f"数据库初始化失败: {str(e)}")
            raise
    
    # 用户相关操作
    def add_user(self, user_data: Dict[str, Any]) -> bool:
        """
        添加用户
        
        Args:
            user_data: 用户数据字典
        
        Returns:
            是否添加成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, password, email, phone, nickname, role, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_data['username'],
                    user_data['password'],
                    user_data['email'],
                    user_data['phone'],
                    user_data.get('nickname', user_data['username']),
                    user_data.get('role', 'student'),
                    user_data['created_at'],
                    user_data['created_at']
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"添加用户失败: {str(e)}")
            return False
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        根据用户名获取用户
        
        Args:
            username: 用户名
        
        Returns:
            用户数据字典，不存在返回None
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            self.logger.error(f"获取用户失败: {str(e)}")
            return None
    
    def update_user(self, username: str, update_data: Dict[str, Any]) -> bool:
        """
        更新用户信息
        
        Args:
            username: 用户名
            update_data: 更新数据字典
        
        Returns:
            是否更新成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # 构建更新语句
                update_fields = []
                update_values = []
                
                for key, value in update_data.items():
                    if key in ['email', 'phone', 'nickname', 'role']:
                        update_fields.append(f"{key} = ?")
                        update_values.append(value)
                
                if update_fields:
                    update_fields.append("updated_at = ?")
                    update_values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    update_values.append(username)
                    
                    sql = f"UPDATE users SET {', '.join(update_fields)} WHERE username = ?"
                    cursor.execute(sql, update_values)
                    conn.commit()
                    return True
                return False
        except Exception as e:
            self.logger.error(f"更新用户失败: {str(e)}")
            return False
    
    # 成绩相关操作
    def add_grade(self, user_id: int, grade_data: Dict[str, Any]) -> bool:
        """
        添加成绩记录
        
        Args:
            user_id: 用户ID
            grade_data: 成绩数据字典
        
        Returns:
            是否添加成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO grades (user_id, course_name, course_code, term, credit, score, gpa, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    grade_data['course_name'],
                    grade_data.get('course_code', ''),
                    grade_data['term'],
                    grade_data['credit'],
                    grade_data['score'],
                    grade_data.get('gpa', 0.0),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"添加成绩失败: {str(e)}")
            return False
    
    def get_grades_by_user(self, user_id: int, term: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取用户成绩
        
        Args:
            user_id: 用户ID
            term: 学期筛选，None表示全部
        
        Returns:
            成绩列表
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if term:
                    cursor.execute("""
                        SELECT * FROM grades WHERE user_id = ? AND term = ?
                        ORDER BY term DESC, course_name
                    """, (user_id, term))
                else:
                    cursor.execute("""
                        SELECT * FROM grades WHERE user_id = ?
                        ORDER BY term DESC, course_name
                    """, (user_id,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"获取成绩失败: {str(e)}")
            return []
    
    # 课表相关操作
    def add_schedule(self, user_id: int, schedule_data: Dict[str, Any]) -> bool:
        """
        添加课表记录
        
        Args:
            user_id: 用户ID
            schedule_data: 课表数据字典
        
        Returns:
            是否添加成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO schedules (user_id, course_name, course_code, day_of_week, start_time, end_time, location, teacher, term, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    schedule_data['course_name'],
                    schedule_data.get('course_code', ''),
                    schedule_data['day_of_week'],
                    schedule_data['start_time'],
                    schedule_data['end_time'],
                    schedule_data.get('location', ''),
                    schedule_data.get('teacher', ''),
                    schedule_data['term'],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"添加课表失败: {str(e)}")
            return False
    
    def get_schedules_by_user(self, user_id: int, day: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取用户课表
        
        Args:
            user_id: 用户ID
            day: 星期筛选，None表示全部
        
        Returns:
            课表列表
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if day:
                    cursor.execute("""
                        SELECT * FROM schedules WHERE user_id = ? AND day_of_week = ?
                        ORDER BY day_of_week, start_time
                    """, (user_id, day))
                else:
                    cursor.execute("""
                        SELECT * FROM schedules WHERE user_id = ?
                        ORDER BY day_of_week, start_time
                    """, (user_id,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"获取课表失败: {str(e)}")
            return []
    
    # 教室相关操作
    def add_classroom(self, classroom_data: Dict[str, Any]) -> bool:
        """
        添加教室记录
        
        Args:
            classroom_data: 教室数据字典
        
        Returns:
            是否添加成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO classrooms (building, room_number, capacity, has_projector, has_computer, has_air_conditioner, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    classroom_data['building'],
                    classroom_data['room_number'],
                    classroom_data.get('capacity', 0),
                    classroom_data.get('has_projector', False),
                    classroom_data.get('has_computer', False),
                    classroom_data.get('has_air_conditioner', False),
                    classroom_data.get('status', 'available'),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"添加教室失败: {str(e)}")
            return False
    
    def get_available_classrooms(self) -> List[Dict[str, Any]]:
        """
        获取可用教室
        
        Returns:
            教室列表
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM classrooms WHERE status = 'available'
                    ORDER BY building, room_number
                """)
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"获取教室失败: {str(e)}")
            return []
    
    # 考试相关操作
    def add_exam(self, user_id: int, exam_data: Dict[str, Any]) -> bool:
        """
        添加考试记录
        
        Args:
            user_id: 用户ID
            exam_data: 考试数据字典
        
        Returns:
            是否添加成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO exams (user_id, course_name, course_code, exam_date, start_time, end_time, location, seat_number, term, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    exam_data['course_name'],
                    exam_data.get('course_code', ''),
                    exam_data['exam_date'],
                    exam_data['start_time'],
                    exam_data['end_time'],
                    exam_data.get('location', ''),
                    exam_data.get('seat_number', ''),
                    exam_data['term'],
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"添加考试失败: {str(e)}")
            return False
    
    def get_exams_by_user(self, user_id: int, subject: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取用户考试
        
        Args:
            user_id: 用户ID
            subject: 科目筛选，None表示全部
        
        Returns:
            考试列表
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if subject:
                    cursor.execute("""
                        SELECT * FROM exams WHERE user_id = ? AND course_name = ?
                        ORDER BY exam_date
                    """, (user_id, subject))
                else:
                    cursor.execute("""
                        SELECT * FROM exams WHERE user_id = ?
                        ORDER BY exam_date
                    """, (user_id,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"获取考试失败: {str(e)}")
            return []
    
    # 通知相关操作
    def add_notice(self, notice_data: Dict[str, Any]) -> bool:
        """
        添加通知记录
        
        Args:
            notice_data: 通知数据字典
        
        Returns:
            是否添加成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO notices (title, content, category, priority, publish_date, publisher, is_important, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    notice_data['title'],
                    notice_data['content'],
                    notice_data.get('category', 'general'),
                    notice_data.get('priority', 'normal'),
                    notice_data['publish_date'],
                    notice_data.get('publisher', '系统'),
                    notice_data.get('is_important', False),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"添加通知失败: {str(e)}")
            return False
    
    def get_notices(self, limit: int = 10, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取通知列表
        
        Args:
            limit: 返回数量限制
            category: 分类筛选，None表示全部
        
        Returns:
            通知列表
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if category:
                    cursor.execute("""
                        SELECT * FROM notices WHERE category = ?
                        ORDER BY publish_date DESC, is_important DESC
                        LIMIT ?
                    """, (category, limit))
                else:
                    cursor.execute("""
                        SELECT * FROM notices
                        ORDER BY publish_date DESC, is_important DESC
                        LIMIT ?
                    """, (limit,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"获取通知失败: {str(e)}")
            return []
    
    # 会话相关操作
    def add_session(self, session_data: Dict[str, Any]) -> bool:
        """
        添加会话记录
        
        Args:
            session_data: 会话数据字典
        
        Returns:
            是否添加成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO sessions (session_id, user_id, title, created_at, updated_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    session_data['session_id'],
                    session_data.get('user_id'),
                    session_data['title'],
                    session_data['created_at'],
                    session_data['updated_at'],
                    json.dumps(session_data.get('metadata', {}))
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"添加会话失败: {str(e)}")
            return False
    
    def add_session_message(self, session_id: str, role: str, content: str, timestamp: str) -> bool:
        """
        添加会话消息
        
        Args:
            session_id: 会话ID
            role: 消息角色
            content: 消息内容
            timestamp: 时间戳
        
        Returns:
            是否添加成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO session_messages (session_id, role, content, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (session_id, role, content, timestamp))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"添加会话消息失败: {str(e)}")
            return False
    
    def get_sessions_by_user(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        获取会话列表
        
        Args:
            user_id: 用户ID筛选，None表示全部
        
        Returns:
            会话列表
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                if user_id:
                    cursor.execute("""
                        SELECT * FROM sessions WHERE user_id = ?
                        ORDER BY updated_at DESC
                    """, (user_id,))
                else:
                    cursor.execute("""
                        SELECT * FROM sessions
                        ORDER BY updated_at DESC
                    """)
                
                sessions = []
                for row in cursor.fetchall():
                    session_data = dict(row)
                    # 解析metadata
                    if session_data.get('metadata'):
                        try:
                            session_data['metadata'] = json.loads(session_data['metadata'])
                        except:
                            session_data['metadata'] = {}
                    sessions.append(session_data)
                
                return sessions
        except Exception as e:
            self.logger.error(f"获取会话列表失败: {str(e)}")
            return []
    
    def get_session_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """
        获取会话消息
        
        Args:
            session_id: 会话ID
        
        Returns:
            消息列表
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM session_messages WHERE session_id = ?
                    ORDER BY timestamp ASC
                """, (session_id,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            self.logger.error(f"获取会话消息失败: {str(e)}")
            return []
    
    # 知识库相关操作
    def add_knowledge(self, knowledge_data: Dict[str, Any]) -> bool:
        """
        添加知识条目
        
        Args:
            knowledge_data: 知识数据字典
        
        Returns:
            是否添加成功
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO knowledge_base (question, answer, category, keywords, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    knowledge_data['question'],
                    knowledge_data['answer'],
                    knowledge_data.get('category', 'general'),
                    json.dumps(knowledge_data.get('keywords', [])),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                return True
        except Exception as e:
            self.logger.error(f"添加知识失败: {str(e)}")
            return False
    
    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        搜索知识库
        
        Args:
            query: 查询关键词
            limit: 返回数量限制
        
        Returns:
            知识条目列表
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # 简单的模糊搜索
                cursor.execute("""
                    SELECT * FROM knowledge_base
                    WHERE question LIKE ? OR answer LIKE ? OR keywords LIKE ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", f"%{query}%", limit))
                
                results = []
                for row in cursor.fetchall():
                    knowledge_data = dict(row)
                    # 解析keywords
                    if knowledge_data.get('keywords'):
                        try:
                            knowledge_data['keywords'] = json.loads(knowledge_data['keywords'])
                        except:
                            knowledge_data['keywords'] = []
                    results.append(knowledge_data)
                
                return results
        except Exception as e:
            self.logger.error(f"搜索知识库失败: {str(e)}")
            return []
    
    def get_database_stats(self) -> Dict[str, int]:
        """
        获取数据库统计信息
        
        Returns:
            统计信息字典
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # 统计各表的记录数
                tables = ['users', 'grades', 'schedules', 'classrooms', 'exams', 'notices', 'sessions', 'session_messages', 'knowledge_base']
                
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    stats[table] = count
                
                return stats
        except Exception as e:
            self.logger.error(f"获取数据库统计失败: {str(e)}")
            return {}