"""
通知查询功能模块
"""

from typing import Dict, Any, List
from .base_feature import BaseFeature
from data.mock_data import MOCK_STUDENT


class NoticeFeature(BaseFeature):
    """
    通知查询功能模块
    支持查询最新校园通知、通知详情等
    """
    
    def __init__(self):
        super().__init__(
            name="通知查询",
            description="查询最新校园通知信息"
        )
        self.notice_data = MOCK_STUDENT["notice"]
    
    def execute (self, count: int = 5, **kwargs) -> Dict[str, Any]:
        """
        执行通知查询
        
        Args:
            count: 返回通知数量，默认5条
            **kwargs: 其他参数
        
        Returns:
            查询结果字典
        """
        try:
            notices_to_show = self.notice_data[:count]
            notice_list = "【校园通知】\n" + "\n".join([f"{i+1}. {n}" for i, n in enumerate(notices_to_show)])
            
            result = {
                "success": True,
                "notices": notices_to_show,
                "count": len(notices_to_show),
                "message": notice_list
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"查询通知时出错: {str(e)}"
            }
    
    def get_ui_components(self) -> Dict[str, Any]:
        """
        获取UI组件配置
        
        Returns:
            UI组件配置字典
        """
        return {
            "type": "notice_query",
            "title": "通知查询",
            "description": "查询最新校园通知",
            "components": [
                {
                    "type": "slider",
                    "label": "显示通知数量",
                    "min": 1,
                    "max": 10,
                    "default": 5,
                    "key": "count"
                },
                {
                    "type": "button",
                    "label": "查询通知",
                    "action": "query_notice"
                },
                {
                    "type": "textbox",
                    "label": "查询结果",
                    "key": "result",
                    "readonly": True
                }
            ]
        }
    
    def get_latest_notices(self, count: int = 5) -> List[str]:
        """
        获取最新通知
        
        Args:
            count: 返回通知数量
        
        Returns:
            最新通知列表
        """
        return self.notice_data[:count]
    
    def search_notices(self, keyword: str) -> List[str]:
        """
        搜索通知
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的通知列表
        """
        return [
            notice for notice in self.notice_data
            if keyword in notice
        ]
    
    def get_notice_categories(self) -> Dict[str, List[str]]:
        """
        获取通知分类
        
        Returns:
            分类通知字典
        """
        categories = {
            "教学": [],
            "行政": [],
            "活动": [],
            "其他": []
        }
        
        for notice in self.notice_data:
            if "考试" in notice or "课程" in notice or "教学" in notice:
                categories["教学"].append(notice)
            elif "升级" in notice or "维护" in notice or "行政" in notice:
                categories["行政"].append(notice)
            elif "活动" in notice or "比赛" in notice:
                categories["活动"].append(notice)
            else:
                categories["其他"].append(notice)
        
        return categories
    
    def get_important_notices(self) -> List[str]:
        """
        获取重要通知
        
        Returns:
            重要通知列表
        """
        important_keywords = ["考试", "选课", "放假", "紧急", "重要"]
        important_notices = []
        
        for notice in self.notice_data:
            if any(keyword in notice for keyword in important_keywords):
                important_notices.append(notice)
        
        return important_notices