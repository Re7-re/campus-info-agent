"""
教室查询功能模块
"""

from typing import Dict, Any, List
from .base_feature import BaseFeature
from data.mock_data import MOCK_STUDENT


class ClassroomFeature(BaseFeature):
    """
    教室查询功能模块
    支持查询空教室、教室状态等
    """
    
    def __init__(self):
        super().__init__(
            name="教室查询",
            description=" 查询可用空教室信息"
        )
        self.classroom_data = MOCK_STUDENT["classroom"]
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        执行教室查询
        
        Args:
            **kwargs: 其他参数
        
        Returns:
            查询结果字典
        """
        try:
            available_rooms = self.classroom_data
            result = {
                "success": True,
                "classrooms": available_rooms,
                "count": len(available_rooms),
                "message": "当前可用空教室：" + "、".join(available_rooms)
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"查询教室时出错: {str(e)}"
            }
    
    def get_ui_components(self) -> Dict[str, Any]:
        """
        获取UI组件配置
        
        Returns:
            UI组件配置字典
        """
        return {
            "type": "classroom_query",
            "title": "教室查询",
            "description": "查询当前可用空教室",
            "components": [
                {
                    "type": "button",
                    "label": "查询空教室",
                    "action": "query_classroom"
                },
                {
                    "type": "textbox",
                    "label": "查询结果",
                    "key": "result",
                    "readonly": True
                }
            ]
        }
    
    def get_available_classrooms(self) -> List[str]:
        """获取可用教室列表"""
        return self.classroom_data.copy()
    
    def search_classroom(self, keyword: str) -> List[str]:
        """
        搜索教室
        
        Args:
            keyword: 搜索关键词
        
        Returns:
            匹配的教室列表
        """
        return [
            room for room in self.classroom_data
            if keyword in room
        ]
    
    def get_classroom_info(self, room_number: str) -> Dict[str, Any]:
        """
        获取教室详细信息
        
        Args:
            room_number: 教室编号
        
        Returns:
            教室信息
        """
        if room_number in self.classroom_data:
            return {
                "success": True,
                "room_number": room_number,
                "status": "可用",
                "message": f"教室 {room_number} 当前可用"
            }
        else:
            return {
                "success": False,
                "message": f"教室 {room_number} 不存在或不可用"
            }