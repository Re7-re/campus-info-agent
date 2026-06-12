"""
用户数据管理模块
提供用户注册、登录、数据存储等功能
"""

import json
import os
import hashlib
from typing import Dict, Any, Optional, List


class  UserData:
    """
    用户数据管理类
    提供用户注册、登录、数据存储等功能
    """
    
    def __init__(self, data_file: str = "data/users.json"):
        """
        初始化用户数据管理
        
        Args:
            data_file: 用户数据文件路径
        """
        self.data_file = data_file
        self.users: Dict[str, Dict[str, Any]] = {}
        self._load_users()
    
    def _load_users(self):
        """从文件加载用户数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            except Exception as e:
                print(f"加载用户数据失败: {e}")
                self._init_default_users()
        else:
            self._init_default_users()
    
    def _init_default_users(self):
        """初始化默认用户"""
        # 创建默认测试用户
        default_users = {
            "admin": {
                "username": "admin",
                "password": self._hash_password("admin123"),
                "email": "admin@example.com",
                "phone": "13800138000",
                "nickname": "管理员",
                "role": "admin",
                "created_at": "2026-06-01 00:00:00"
            },
            "student": {
                "username": "student",
                "password": self._hash_password("student123"),
                "email": "student@example.com",
                "phone": "13900139000",
                "nickname": "学生用户",
                "role": "student",
                "created_at": "2026-06-02 00:00:00"
            }
        }
        self.users = default_users
        self._save_users()
    
    def _save_users(self):
        """保存用户数据到文件"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """
        密码哈希函数
        
        Args:
            password: 原始密码
        
        Returns:
            哈希后的密码
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def validate_username(self, username: str) -> Dict[str, Any]:
        """
        验证用户名
        
        Args:
            username: 用户名
        
        Returns:
            验证结果字典
        """
        if not username:
            return {"valid": False, "message": "用户名不能为空"}
        
        if len(username) < 3 or len(username) > 20:
            return {"valid": False, "message": "用户名长度必须在3-20个字符之间"}
        
        if not username.isalnum():
            return {"valid": False, "message": "用户名只能包含字母和数字"}
        
        return {"valid": True, "message": "用户名有效"}
    
    def validate_password(self, password: str) -> Dict[str, Any]:
        """
        验证密码
        
        Args:
            password: 密码
        
        Returns:
            验证结果字典
        """
        if not password:
            return {"valid": False, "message": "密码不能为空"}
        
        if len(password) < 6:
            return {"valid": False, "message": "密码长度至少6位"}
        
        # 检查是否包含数字和字母
        has_number = any(char.isdigit() for char in password)
        has_letter = any(char.isalpha() for char in password)
        
        if not has_number or not has_letter:
            return {"valid": False, "message": "密码必须包含字母和数字"}
        
        return {"valid": True, "message": "密码有效"}
    
    def validate_email(self, email: str) -> Dict[str, Any]:
        """
        验证邮箱格式
        
        Args:
            email: 邮箱地址
        
        Returns:
            验证结果字典
        """
        if not email:
            return {"valid": False, "message": "邮箱不能为空"}
        
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return {"valid": False, "message": "邮箱格式不正确"}
        
        return {"valid": True, "message": "邮箱格式有效"}
    
    def validate_phone(self, phone: str) -> Dict[str, Any]:
        """
        验证手机号格式
        
        Args:
            phone: 手机号码
        
        Returns:
            验证结果字典
        """
        if not phone:
            return {"valid": False, "message": "手机号不能为空"}
        
        import re
        pattern = r'^1[3-9]\d{9}$'
        if not re.match(pattern, phone):
            return {"valid": False, "message": "手机号格式不正确"}
        
        return {"valid": True, "message": "手机号格式有效"}
    
    def register(
        self,
        username: str,
        password: str,
        confirm_password: str,
        email: str,
        phone: str,
        nickname: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        用户注册
        
        Args:
            username: 用户名
            password: 密码
            confirm_password: 确认密码
            email: 邮箱
            phone: 手机号
            nickname: 昵称（可选）
        
        Returns:
            注册结果字典
        """
        # 验证用户名
        username_result = self.validate_username(username)
        if not username_result["valid"]:
            return {"success": False, "message": username_result["message"]}
        
        # 检查用户名是否已存在
        if username in self.users:
            return {"success": False, "message": "用户名已存在"}
        
        # 验证密码
        password_result = self.validate_password(password)
        if not password_result["valid"]:
            return {"success": False, "message": password_result["message"]}
        
        # 验证确认密码
        if password != confirm_password:
            return {"success": False, "message": "两次输入的密码不一致"}
        
        # 验证邮箱
        email_result = self.validate_email(email)
        if not email_result["valid"]:
            return {"success": False, "message": email_result["message"]}
        
        # 验证手机号
        phone_result = self.validate_phone(phone)
        if not phone_result["valid"]:
            return {"success": False, "message": phone_result["message"]}
        
        # 检查邮箱是否已被使用
        for user in self.users.values():
            if user["email"] == email:
                return {"success": False, "message": "该邮箱已被注册"}
            if user["phone"] == phone:
                return {"success": False, "message": "该手机号已被注册"}
        
        # 创建用户
        from datetime import datetime
        new_user = {
            "username": username,
            "password": self._hash_password(password),
            "email": email,
            "phone": phone,
            "nickname": nickname or username,
            "role": "student",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.users[username] = new_user
        self._save_users()
        
        return {
            "success": True,
            "message": "注册成功！",
            "user": {
                "username": username,
                "nickname": nickname or username,
                "email": email,
                "phone": phone
            }
        }
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        用户登录
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            登录结果字典
        """
        # 检查用户是否存在
        if username not in self.users:
            return {"success": False, "message": "用户名不存在"}
        
        # 验证密码
        user = self.users[username]
        if user["password"] != self._hash_password(password):
            return {"success": False, "message": "密码错误"}
        
        return {
            "success": True,
            "message": "登录成功！",
            "user": {
                "username": user["username"],
                "nickname": user["nickname"],
                "email": user["email"],
                "phone": user["phone"],
                "role": user["role"],
                "created_at": user["created_at"]
            }
        }
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """
        获取用户信息
        
        Args:
            username: 用户名
        
        Returns:
            用户信息字典，如果不存在返回None
        """
        if username in self.users:
            user = self.users[username].copy()
            # 不返回密码
            user.pop("password", None)
            return user
        return None
    
    def update_user(
        self,
        username: str,
        nickname: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        更新用户信息
        
        Args:
            username: 用户名
            nickname: 昵称
            email: 邮箱
            phone: 手机号
        
        Returns:
            更新结果字典
        """
        if username not in self.users:
            return {"success": False, "message": "用户不存在"}
        
        user = self.users[username]
        
        if nickname:
            user["nickname"] = nickname
        
        if email:
            email_result = self.validate_email(email)
            if not email_result["valid"]:
                return {"success": False, "message": email_result["message"]}
            # 检查邮箱是否被其他用户使用
            for u in self.users.values():
                if u["email"] == email and u["username"] != username:
                    return {"success": False, "message": "该邮箱已被使用"}
            user["email"] = email
        
        if phone:
            phone_result = self.validate_phone(phone)
            if not phone_result["valid"]:
                return {"success": False, "message": phone_result["message"]}
            # 检查手机号是否被其他用户使用
            for u in self.users.values():
                if u["phone"] == phone and u["username"] != username:
                    return {"success": False, "message": "该手机号已被使用"}
            user["phone"] = phone
        
        self._save_users()
        
        return {"success": True, "message": "更新成功！", "user": self.get_user(username)}
    
    def change_password(self, username: str, old_password: str, new_password: str) -> Dict[str, Any]:
        """
        修改密码
        
        Args:
            username: 用户名
            old_password: 旧密码
            new_password: 新密码
        
        Returns:
            修改结果字典
        """
        if username not in self.users:
            return {"success": False, "message": "用户不存在"}
        
        user = self.users[username]
        
        # 验证旧密码
        if user["password"] != self._hash_password(old_password):
            return {"success": False, "message": "旧密码错误"}
        
        # 验证新密码
        password_result = self.validate_password(new_password)
        if not password_result["valid"]:
            return {"success": False, "message": password_result["message"]}
        
        # 更新密码
        user["password"] = self._hash_password(new_password)
        self._save_users()
        
        return {"success": True, "message": "密码修改成功！"}
    
    def delete_user(self, username: str) -> Dict[str, Any]:
        """
        删除用户
        
        Args:
            username: 用户名
        
        Returns:
            删除结果字典
        """
        if username not in self.users:
            return {"success": False, "message": "用户不存在"}
        
        del self.users[username]
        self._save_users()
        
        return {"success": True, "message": "删除成功！"}
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        获取所有用户列表（不含密码）
        
        Returns:
            用户列表
        """
        users = []
        for user in self.users.values():
            u = user.copy()
            u.pop("password", None)
            users.append(u)
        return users
    
    def get_user_count(self) -> int:
        """获取用户数量"""
        return len(self.users)