"""
配置文件
系统配置参数管理
"""

import os
from typing import Optional


class  Config:
    """系统配置类"""
    
    # 智谱 AI 配置
    ZHIPU_API_KEY: str = "49f5437b5aa5412ea40de86cae19a85d.57k0Wao6iRLxVXq9"  # 有免费额度的新Key
    ZHIPU_MODEL_NAME: str = "glm-4-flash"  # 智谱免费模型
    ZHIPU_API_BASE: str = "https://open.bigmodel.cn/api/paas/v4/"
    
    # 硅基流动配置 - 免费模型
    SILICONFLOW_API_KEY: str = "sk-ggtcxwwrmbolnpkgstkggqnglzaqqccrtixeqtxnrkjrbnia"
    SILICONFLOW_MODEL_NAME: str = "Qwen/Qwen2-1.5B-Instruct"  # 确认可用的免费模型
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
    DEFAULT_AI_SERVICE: str = "zhipu"  # 优先使用智谱免费模型
    
    # API 连接配置
    API_TIMEOUT: int = 30  # 连接超时时间（秒）
    API_RETRY_COUNT: int = 2  # 重试次数
    API_RETRY_DELAY: int = 2  # 重试延迟（秒）
    
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
    ENABLE_FALLBACK: bool = True  # 启用降级到本地规则引擎
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FILE: Optional[str] = None
    
    # 数据配置
    DATA_DIR: str = "data"
    MEMORY_DIR: str = "memory"
    
    # 教务系统配置
    ENABLE_CUIT_SPIDER: bool = True  # 是否启用成都信息工程大学教务爬虫
    CUIT_USERNAME: str = "2023132060"  # 学号
    CUIT_PASSWORD: str = "C18328526643x."  # 密码
    CUIT_AUTO_UPDATE: bool = True  # 是否自动更新数据
    CUIT_UPDATE_INTERVAL: int = 24  # 更新间隔（小时）
    
    # 教务系统Cookie配置（登录后获取，只保留关键3条）
    CUIT_COOKIES: dict = {
        "GSSESSIONID": "DDCAF4CB441F55D9ED1FB2372B4D8676",
        "JSESSIONID": "DDCAF4CB441F55D9ED1FB2372B4D8676",
        "semester.id": "1006",
        "WVTSESSIONID": "90bec63b-134a-4b12-4b80-b412-ad0c6cc3434"
    }
    
    # 教务系统URL配置（使用eams老平台）
    CUIT_JWGL_URL: str = "http://jwgl.cuit.edu.cn/eams"  # eams老教务平台
    CUIT_JWC_URL: str = "https://jwc.cuit.edu.cn"        # 教务处官网
    CUIT_CAS_URL: str = "https://cas.cuit.edu.cn"        # CAS登录
    
    # 数据来源配置
    DATA_SOURCE: str = "manual"  # 可选值: mock(模拟数据), cuit(真实数据), manual(手动导入)
    # 注意：cuit模式需要配置正确的教务系统登录信息，且教务系统可能有验证码等安全措施
    # manual模式需要在 data/manual_data.json 文件中手动填写数据
    
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
