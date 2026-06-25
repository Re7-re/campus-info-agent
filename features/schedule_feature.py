"""
课程表查询功能模块
支持真实数据和模拟数据的查询
"""

import random
from typing import Dict, Any, Optional, List
from .base_feature import BaseFeature
from utils.data_loader import data_loader
import logging

logger = logging.getLogger(__name__)


class ScheduleFeature(BaseFeature):
    """
    课程表查询功能模块
    支持按学期、按星期查询课程表
    """
    
    def __init__(self):
        super().__init__(
            name="课表查询",
            description="查询课程表信息"
        )
        # 尝试加载真实数据
        self.schedules = data_loader.load_schedules()
        
        # 如果没有真实数据，使用模拟数据
        if not self.schedules:
            logger.warning("未加载到真实课程表数据，使用模拟数据")
            self._use_mock_data()
        else:
            logger.info(f"成功加载 {len(self.schedules)} 个学期的课程表")
    
    def _use_mock_data(self):
        """使用模拟数据"""
        from data.mock_data import generate_schedule_data
        
        # 生成包含所有学期的课程表数据
        schedule_data = generate_schedule_data()
        
        # 数据已经是统一格式，直接使用
        self.schedules = schedule_data
    
    def execute(self, semester: str = None, weekday: str = None, **kwargs) -> Dict[str, Any]:
        """
        执行课程表查询
        
        Args:
            semester: 学期筛选条件
            weekday: 星期几筛选条件
            **kwargs: 其他参数
        
        Returns:
            查询结果字典
        """
        try:
            # 过滤数据
            filtered_schedule = self._filter_schedule(semester, weekday)
            
            if not filtered_schedule:
                return {
                    "success": False,
                    "message": f"未找到符合条件的课程"
                }
            
            # 生成友好的文本输出
            output = self._format_schedule_output(filtered_schedule, weekday)
            
            return {
                "success": True,
                "schedule": filtered_schedule,
                "message": output
            }
            
        except Exception as e:
            logger.error(f"查询课程表时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"查询课程表时出错: {str(e)}"
            }
    
    def _normalize_semester(self, semester: str) -> str:
        """
        标准化学期格式，支持多种输入格式
        
        Args:
            semester: 学期字符串
        
        Returns:
            标准化后的学期格式（统一为 2023-2024-1 格式）
        """
        if not semester:
            return semester
        
        import re
        # 处理格式如 "2023-2024-1" -> 保持不变
        match = re.match(r'(\d{4})-(\d{4})-(\d)', semester)
        if match:
            return semester
        
        # 处理格式如 "第2023-2024第一学期（大一上学期）" -> "2023-2024-1"
        chinese_num = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '十': '10'}
        match = re.search(r'(\d{4})-(\d{4})第([一二三四五六七八九十1-9])学期', semester)
        if match:
            year1, year2, term = match.groups()
            term = chinese_num.get(term, term)
            return f"{year1}-{year2}-{term}"
        
        # 处理格式如 "2023-2024学年第1学期" -> "2023-2024-1"
        match = re.search(r'(\d{4})-(\d{4})[年学]第(\d)学期', semester)
        if match:
            year1, year2, term = match.groups()
            return f"{year1}-{year2}-{term}"
        
        return semester
    
    def _filter_schedule(self, semester: str = None, weekday: str = None) -> List[Dict[str, Any]]:
        """
        过滤课程表数据
        
        Args:
            semester: 学期筛选条件
            weekday: 星期几筛选条件
        
        Returns:
            过滤后的课程列表
        """
        filtered = []
        
        if semester and semester != "全部":
            # 查询指定学期
            # 尝试直接匹配
            semesters_to_query = []
            if semester in self.schedules:
                semesters_to_query.append(semester)
            else:
                # 尝试标准化后的学期格式
                normalized_semester = self._normalize_semester(semester)
                for key in self.schedules.keys():
                    if normalized_semester in key or key in normalized_semester:
                        semesters_to_query.append(key)
            
            # 如果没有找到匹配，使用原始输入
            if not semesters_to_query:
                semesters_to_query = [semester]
        else:
            # 查询所有学期
            semesters_to_query = list(self.schedules.keys())
        
        for sem in semesters_to_query:
            courses = self.schedules.get(sem, [])
            for course in courses:
                # 按星期过滤
                if weekday and weekday != "全部":
                    if course.get('weekday') != weekday:
                        continue
                
                filtered.append(course)
        
        # 按星期和节次排序
        weekday_order = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        filtered.sort(key=lambda x: (
            weekday_order.index(x.get('weekday', '星期一')) if x.get('weekday') in weekday_order else 0,
            self._extract_period_number(x.get('period', '第1节'))
        ))
        
        return filtered
    
    def _extract_period_number(self, period: str) -> int:
        """提取节次数字"""
        import re
        match = re.search(r'第(\d+)节', period)
        return int(match.group(1)) if match else 0
    
    def _format_schedule_output(self, schedule: List[Dict[str, Any]], weekday: str = None) -> str:
        """
        格式化课程表输出
        
        Args:
            schedule: 课程列表
            weekday: 查询的星期
        
        Returns:
            格式化的文本输出
        """
        if not schedule:
            return "没有找到课程安排"
        
        output_parts = []
        
        # 如果查询了特定星期
        if weekday and weekday != "全部":
            output_parts.append(f"📅 {weekday} 课程表\n")
            # 按节次组织
            current_period = None
            for course in schedule:
                period = course.get('period', '')
                if period != current_period:
                    if current_period is not None:
                        output_parts.append("")
                    output_parts.append(f"【{period}】")
                    current_period = period
                
                course_name = course.get('course_name', '未知课程')
                teacher = course.get('teacher', '未知教师')
                location = course.get('location', '待定')
                weeks = course.get('weeks', '')
                
                output_parts.append(f"  📚 {course_name}")
                output_parts.append(f"     👤 教师: {teacher}")
                output_parts.append(f"     📍 地点: {location}")
                if weeks:
                    output_parts.append(f"     📆 周次: {weeks}")
        else:
            # 显示完整课程表
            # 按星期组织
            weekday_order = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            
            for day in weekday_order:
                day_courses = [c for c in schedule if c.get('weekday') == day]
                if day_courses:
                    output_parts.append(f"\n📅 {day}")
                    current_period = None
                    for course in day_courses:
                        period = course.get('period', '')
                        if period != current_period:
                            output_parts.append(f"  【{period}】")
                            current_period = period
                        
                        course_name = course.get('course_name', '未知课程')
                        teacher = course.get('teacher', '未知教师')
                        location = course.get('location', '待定')
                        
                        output_parts.append(f"    📚 {course_name} | {teacher} | {location}")
        
        return "\n".join(output_parts)
    
    def get_available_semesters(self) -> List[str]:
        """获取可用的学期列表"""
        return sorted(list(self.schedules.keys()), reverse=True)
    
    def get_available_weekdays(self) -> List[str]:
        """获取可用的星期列表"""
        return ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    
    def get_today_schedule(self) -> Dict[str, Any]:
        """获取今天的课程表"""
        import datetime
        weekday_map = {0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'}
        today_weekday = weekday_map[datetime.datetime.now().weekday()]
        
        return self.execute(weekday=today_weekday)
    
    def get_ui_components(self) -> Dict[str, Any]:
        """获取UI组件配置"""
        semesters = self.get_available_semesters()
        weekdays = self.get_available_weekdays()
        return {
            "type": "schedule_query",
            "title": "课表查询",
            "description": "查询课程表信息",
            "components": [
                {
                    "type": "dropdown",
                    "label": "选择学期",
                    "choices": ["全部"] + semesters,
                    "default": "全部" if not semesters else semesters[0],
                    "key": "semester"
                },
                {
                    "type": "dropdown",
                    "label": "选择星期",
                    "choices": ["全部"] + weekdays,
                    "default": "全部",
                    "key": "weekday"
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
