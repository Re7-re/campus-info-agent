"""
课表查询功能模块
"""

from typing import Dict, Any, Optional, List
from .base_feature import BaseFeature
from data.mock_data import MOCK_STUDENT


class ScheduleFeature(BaseFeature):
    """
    课表查询功能模块
    支持按星期查询课表、查看全部课表等
    """
    
    def __init__(self):
        super().__init__(
            name="课表查询",
            description="查询学生周课表信息"
        )
        self.schedule_data = MOCK_STUDENT["schedule"]
    
    def execute(self, day: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        执行课表查询
        
        Args:
            day: 星期，如"周一"，如果为None则查询全部
            **kwargs: 其他参数
        
        Returns:
            查询结果字典
        """
        try:
            if day and day in self.schedule_data:
                # 查询指定星期课表
                courses = self.schedule_data[day]
                result = {
                    "success": True,
                    "day": day,
                    "courses": courses,
                    "message": f"【{day}课表】\n" + "\n".join([f"第{i+1}节：{v}" for i, v in enumerate(courses) if v])
                }
            else:
                # 查询全部课表
                all_schedule = ""
                for d, s in self.schedule_data.items():
                    all_schedule += f"【{d}】\n" + "\n".join([f"第{i+1}节：{v}" for i, v in enumerate(s) if v]) + "\n"
                
                result = {
                    "success": True,
                    "day": "全部",
                    "schedule": self.schedule_data,
                    "message": all_schedule
                }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"查询课表时出错: {str(e)}"
            }
    
    def get_ui_components(self) -> Dict[str, Any]:
        """
        获取UI组件配置
        
        Returns:
            UI组件配置字典
        """
        return {
            "type": "schedule_query",
            "title": "课表查询",
            "description": "查询周课表信息",
            "components": [
                {
                    "type": "dropdown",
                    "label": "选择星期",
                    "choices": ["全部"] + list(self.schedule_data.keys()),
                    "default": "全部",
                    "key": "day"
                },
                {
                    "type": "button",
                    "label": "查询课表",
                    "action": "query_schedule"
                },
                {
                    "type": "textbox",
                    "label": "查询结果",
                    "key": "result",
                    "readonly": True
                }
            ]
        }
    
    def get_available_days(self) -> List[str]:
        """获取可用的星期列表"""
        return list(self.schedule_data.keys())
    
    def get_today_schedule(self) -> Dict[str, Any]:
        """
        获取今天的课表
        
        Returns:
            今天的课表信息
        """
        import datetime
        
        # 获取今天是星期几
        today = datetime.datetime.now().strftime("%A")
        day_mapping = {
            "Monday": "周一",
            "Tuesday": "周二", 
            "Wednesday": "周三",
            "Thursday": "周四",
            "Friday": "周五",
            "Saturday": "周六",
            "Sunday": "周日"
        }
        
        chinese_day = day_mapping.get(today, "周一")
        return self.execute(day=chinese_day)
    
    def get_week_schedule(self) -> Dict[str, Any]:
        """
        获取本周课表
        
        Returns:
            本周课表信息
        """
        return self.execute(day=None)
    
    def get_free_periods(self, day: str) -> List[int]:
        """
        获取指定日期的空闲时间段
        
        Args:
            day: 星期
        
        Returns:
            空闲时间段列表
        """
        if day not in self.schedule_data:
            return []
        
        courses = self.schedule_data[day]
        free_periods = []
        
        for i, course in enumerate(courses):
            if not course or course.strip() == "":
                free_periods.append(i + 1)
        
        return free_periods