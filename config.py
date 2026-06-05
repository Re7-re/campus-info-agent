"""
配置文件
系统配置参数管理
"""

import os
from typing import Optional


class Config:
    """系统配置类"""
    
    # 智谱 AI 配置
    ZHIPU_API_KEY: str = "49f5437b5aa5412ea40de86cae19a85d.57k0Wao6iRLxVXq9"  # 有免费额度的新Key
    ZHIPU_MODEL_NAME: str = "glm-4-air"  # 通用模型，使用按tokens计费的资源包
    ZHIPU_API_BASE: str = "https://open.bigmodel.cn/api/paas/v4/"
    
    # 硅基流动配置 - 免费模型
    SILICONFLOW_API_KEY: str = "sk-ggtcxwwrmbolnpkgstkggqnglzaqqccrtixeqtxnrkjrbnia"
    SILICONFLOW_MODEL_NAME: str = "Qwen/Qwen2.5-1.5B-Instruct"  # 确认可用的免费模型
    SILICONFLOW_API_BASE: str = "https://api.siliconflow.cn/v1/"
    
    # DeepSeek 配置 - 免费模型
    DEEPSEEK_API_KEY: str = "sk-57168e8a2dc4446cba8f47a1e452253b"
    DEEPSEEK_MODEL_NAME: str = "deepseek-chat"
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1/"
    
    # LongChat 配置
    LONGCHAT_API_KEY: str = "ak_27236N7L18go2Q61ju9Jy6PA1rP8M"
    LONGCHAT_MODEL_NAME: str = "longchat-7b-chat"
    LONGCHAT_API_BASE: str = "https://api.longchat.cn/v1/"
    
    # 阿里云百炼配置
    ALIBABA_API_KEY: str = "sk-582ff0386def4eb183eefad02d86c207"
    ALIBABA_MODEL_NAME: str = "qwen-plus"  # 使用 qwen-plus 模型
    ALIBABA_API_BASE: str = "https://dashscope.aliyuncs.com/compatible-mode/v1/"
    
    # 默认使用的 AI 服务 - 切换到智谱免费模型
    DEFAULT_AI_SERVICE: str = "zhipu"  # 可选值：zhipu, siliconflow, deepseek, longchat, alibaba
    
    # 服务配置
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    UI_PORT: int = 7860
    
    # 项目配置
    PROJECT_NAME: str = "校园信息智能查询系统"
    VERSION: str = "2.0.0"
    
    # 功能配置
    ENABLE_MEMORY: bool = True
    MAX_MEMORY_SIZE: int = 50
    ENABLE_KNOWLEDGE_BASE: bool = True
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FILE: Optional[str] = None
    
    # 数据配置
    DATA_DIR: str = "data"
    MEMORY_DIR: str = "memory"
    
    # UI 配置
    UI_THEME: str = "Soft"
    UI_TITLE: str = "校园信息智能查询系统"
    
    @classmethod
    def validate(cls) -> bool:
        """
        验证配置有效性
        
        Returns:
            配置是否有效
        """
        if not cls.ZHIPU_API_KEY:
            print("警告：智谱 API 密钥未设置")
            return False
        
        # 创建必要的目录
        for dir_path in [cls.LOG_DIR, cls.DATA_DIR, cls.MEMORY_DIR]:
            os.makedirs(dir_path, exist_ok=True)
        
        return True
    
    @classmethod
    def get_api_config(cls) -> dict:
        """
        获取 API 配置
        
        Returns:
            API 配置字典
        """
        return {
            "api_key": cls.ZHIPU_API_KEY,
            "model": cls.MODEL_NAME,
            "base_url": cls.API_BASE
        }
    
    @classmethod
    def get_server_config(cls) -> dict:
        """
        获取服务器配置
        
        Returns:
            服务器配置字典
        """
        return {
            "host": cls.API_HOST,
            "port": cls.API_PORT,
            "ui_port": cls.UI_PORT
        }


# 兼容旧的全局变量
ZHIPU_API_KEY = Config.ZHIPU_API_KEY
MODEL_NAME = Config.ZHIPU_MODEL_NAME  # 保持向后兼容
API_HOST = Config.API_HOST
API_PORT = Config.API_PORT
UI_PORT = Config.UI_PORT
PROJECT_NAME = Config.PROJECT_NAME
