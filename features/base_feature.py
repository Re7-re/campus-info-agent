"""
功能模块基类
所有功能模块的基类，定义统一接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseFeature(ABC):
    """
    功能模块基类
    所有具体功能模块都需要继承此类并实现相应方法
    """
    
    def __init__(self, name: str, description: str):
        """
        初始化功能模块
        
        Args:
            name: 功能名称
            description: 功能描述
        """
        self.name =  name
        self.description = description
        self.enabled = True
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行功能
        
        Args:
            **kwargs: 功能参数
        
        Returns:
            执行结果字典
        """
        pass
    
    @abstractmethod
    def get_ui_components(self) -> Dict[str, Any]:
        """
        获取UI组件配置
        
        Returns:
            UI组件配置字典
        """
        pass
    
    def enable(self):
        """启用功能"""
        self.enabled = True
    
    def disable(self):
        """禁用功能"""
        self.enabled = False
    
    def is_enabled(self) -> bool:
        """检查功能是否启用"""
        return self.enabled
    
    def get_info(self) -> Dict[str, Any]:
        """
        获取功能信息
        
        Returns:
            功能信息字典
        """
        return {
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled
        }