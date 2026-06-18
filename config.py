"""
配置文件
系统配置参数管理
"""

import os
from typing import Optional


class Config:
    """系统配置类"""
    
    # 智谱AI配置
    ZHIPU_API_KEY: str = "7d2cf26ac992484a94fd637e1fedce58.TmRaoswkFI44hMbe"
    MODEL_NAME: str = "glm-4"
    API_BASE: str = "https://open.bigmodel.cn/api/paas/v4/"
    
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
    
    # UI配置
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
            print("警告：智谱API密钥未设置")
            return False
        
        # 创建必要的目录
        for dir_path in [cls.LOG_DIR, cls.DATA_DIR, cls.MEMORY_DIR]:
            os.makedirs(dir_path, exist_ok=True)
        
        return True
    
    @classmethod
    def get_api_config(cls) -> dict:
        """
        获取API配置
        
        Returns:
            API配置字典
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
MODEL_NAME = Config.MODEL_NAME
API_HOST = Config.API_HOST
API_PORT = Config.API_PORT
UI_PORT = Config.UI_PORT
PROJECT_NAME = Config.PROJECT_NAME