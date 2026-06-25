"""
配置文件
系统配置参数管理
"""

import os
from typing import Optional


class Config:
    """系统配置类"""
    
    # =============================================================================
    # API 配置 - 请填写你的 API 密钥
    # 提示：从 https://open.bigmodel.cn/ 或 https://platform.deepseek.com/ 获取
    # =============================================================================

    # 智谱 AI 配置
    ZHIPU_API_KEY: str = "your_zhipu_api_key_here"
    ZHIPU_MODEL_NAME: str = "glm-4"
    ZHIPU_API_BASE: str = "https://open.bigmodel.cn/api/paas/v4/"

    # 硅基流动配置
    SILICONFLOW_API_KEY: str = "your_siliconflow_api_key_here"
    SILICONFLOW_MODEL_NAME: str = "Qwen/Qwen2-1.5B-Instruct"
    SILICONFLOW_API_BASE: str = "https://api.siliconflow.cn/v1/"

    # DeepSeek 配置
    DEEPSEEK_API_KEY: str = "your_deepseek_api_key_here"
    DEEPSEEK_MODEL_NAME: str = "deepseek-v4-pro"
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1/"

    # LongChat 配置
    LONGCHAT_API_KEY: str = "your_longchat_api_key_here"
    LONGCHAT_MODEL_NAME: str = "longchat-7b-chat"
    LONGCHAT_API_BASE: str = "https://api.longchat.cn/v1/"

    # 阿里云百炼配置
    ALIBABA_API_KEY: str = "your_alibaba_api_key_here"
    ALIBABA_MODEL_NAME: str = "qwen-plus"
    ALIBABA_API_BASE: str = "https://dashscope.aliyuncs.com/compatible-mode/v1/"
    
    # 默认使用的 AI 服务
    DEFAULT_AI_SERVICE: str = "zhipu"
    
    # API 连接配置
    API_TIMEOUT: int = 8  # 超时时间（秒）
    API_RETRY_COUNT: int = 3  # 重试次数
    API_RETRY_DELAY: int = 1  # 初始重试延迟（秒）
    
    # 本地模型配置
    ENABLE_LOCAL_MODEL: bool = False  # 是否启用本地量化模型
    LOCAL_MODEL_NAME: str = "Qwen-1.8B-Chat"
    LOCAL_MODEL_PATH: str = "models"
    LOCAL_MODEL_MAX_TOKENS: int = 2048
    
    # 模型降级策略
    MODEL_TIER_ORDER: list = ["online", "local", "rules"]
    MAX_FAILURES_BEFORE_SWITCH: int = 5
    
    # 服务配置
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    UI_PORT: int = 7860
    
    # 项目配置
    PROJECT_NAME: str = "校园信息智能查询系统"
    VERSION: str = "3.0.0"
    
    # 功能配置
    ENABLE_MEMORY: bool = True
    SHORT_TERM_WINDOW: int = 20  # 短期上下文窗口大小
    ENABLE_KNOWLEDGE_BASE: bool = True
    ENABLE_FALLBACK: bool = True  # 启用降级到本地规则引擎
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "logs"
    LOG_FILE: Optional[str] = None
    
    # 数据配置
    DATA_DIR: str = "data"
    MEMORY_DIR: str = "memory"
    CACHE_DIR: str = "data"
    
    # 增量导入配置
    ENABLE_INCREMENTAL_IMPORT: bool = True
    CACHE_VALID_DURATION: int = 86400  # 缓存有效时长（秒）
    
    # GPA计算配置
    DEFAULT_GPA_MODE: str = "weighted"  # simple 或 weighted
    
    # 中文数字映射表（课表解析规则）
    CHINESE_NUM_MAP: dict = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
        '七': 7, '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12
    }
    
    # =============================================================================
    # 教务系统配置（仅当 DATA_SOURCE = "cuit" 时使用）
    # =============================================================================
    ENABLE_CUIT_SPIDER: bool = False  # 是否启用教务爬虫
    CUIT_USERNAME: str = "your_student_id"  # 学号
    CUIT_PASSWORD: str = "your_password"  # 密码
    CUIT_AUTO_UPDATE: bool = True  # 是否自动更新数据
    CUIT_UPDATE_INTERVAL: int = 24  # 更新间隔（小时）

    # 教务系统Cookie配置（登录后获取）
    CUIT_COOKIES: dict = {}

    # 教务系统URL配置
    CUIT_JWGL_URL: str = "http://jwgl.cuit.edu.cn/eams"
    CUIT_JWC_URL: str = "https://jwc.cuit.edu.cn"
    CUIT_CAS_URL: str = "https://cas.cuit.edu.cn"

    # =============================================================================
    # 数据来源配置
    # =============================================================================
    # 可选值:
    #   - mock: 使用内置模拟数据（默认，适合测试）
    #   - manual: 使用 data/manual_data.json 中的数据
    #   - cuit: 对接成都信息工程大学教务系统（需要配置账号密码）
    DATA_SOURCE: str = "mock"  # 默认使用模拟数据
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
        # 检查 API 密钥是否已配置
        current_service = cls.get_api_config()
        api_key = current_service.get("api_key", "")

        if "your_" in api_key or not api_key:
            print("警告：API 密钥未配置，将使用本地规则引擎")
            print("提示：请编辑 config.py 或复制 config_example.py 并填写你的 API 密钥")

        # 创建必要的目录
        for dir_path in [cls.LOG_DIR, cls.DATA_DIR, cls.MEMORY_DIR]:
            os.makedirs(dir_path, exist_ok=True)

        return True
    
    @classmethod
    def get_api_config(cls, service: str = None) -> dict:
        """
        获取 API 配置
        
        Args:
            service: 服务名称 (zhipu/siliconflow/deepseek/longchat/alibaba)，默认使用 DEFAULT_AI_SERVICE
        
        Returns:
            API 配置字典
        """
        if service is None:
            service = cls.DEFAULT_AI_SERVICE
        
        config_map = {
            "zhipu": {"api_key": cls.ZHIPU_API_KEY, "model": cls.ZHIPU_MODEL_NAME, "base_url": cls.ZHIPU_API_BASE},
            "siliconflow": {"api_key": cls.SILICONFLOW_API_KEY, "model": cls.SILICONFLOW_MODEL_NAME, "base_url": cls.SILICONFLOW_API_BASE},
            "deepseek": {"api_key": cls.DEEPSEEK_API_KEY, "model": cls.DEEPSEEK_MODEL_NAME, "base_url": cls.DEEPSEEK_API_BASE},
            "longchat": {"api_key": cls.LONGCHAT_API_KEY, "model": cls.LONGCHAT_MODEL_NAME, "base_url": cls.LONGCHAT_API_BASE},
            "alibaba": {"api_key": cls.ALIBABA_API_KEY, "model": cls.ALIBABA_MODEL_NAME, "base_url": cls.ALIBABA_API_BASE},
        }
        
        return config_map.get(service, config_map["zhipu"])
    
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
