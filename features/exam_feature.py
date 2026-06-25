"""
考试安排查询功能模块
支持真实数据和模拟数据的查询
"""

from typing import Dict, Any, Optional, List
from .base_feature import BaseFeature
from utils.data_loader import data_loader
import logging

logger = logging.getLogger(__name__)


class ExamFeature(BaseFeature):
    """
    考试安排查询功能模块
    支持按学期查询考试安排、查看全部考试等
    """
    
    def __init__(self):
        super().__init__(
            name="考试查询",
            description="查询期末考试安排信息"
        )
        # 尝试加载真实数据
        self.exams = data_loader.load_exams()
        
        # 如果没有真实数据，使用模拟数据
        if not self.exams:
            logger.warning("未加载到真实考试数据，使用模拟数据")
            self._use_mock_data()
        else:
            logger.info(f"成功加载 {len(self.exams)} 条真实考试记录")
    
    def _use_mock_data(self):
        """使用模拟数据"""
        from data.mock_data import MOCK_STUDENT
        self.exams = []
        for exam in MOCK_STUDENT.get("exam", []):
            self.exams.append({
                'semester': exam.get('学期', ''),
                'course_name': exam.get('课程名称', ''),
                'exam_date': exam.get('日期', ''),
                'exam_time': exam.get('时间', ''),
                'exam_location': exam.get('地点', '待定'),
                'exam_type': exam.get('类型', '期末考试'),
                'note': exam.get('备注', '')
            })
    
    def execute(self, semester: str = None, course: str = None, **kwargs) -> Dict[str, Any]:
        """
        执行考试查询
        
        Args:
            semester: 学期筛选条件
            course: 课程名称筛选条件
            **kwargs: 其他参数
        
        Returns:
            查询结果字典
        """
        try:
            # 过滤数据
            filtered_exams = self._filter_exams(semester, course)
            
            if not filtered_exams:
                return {
                    "success": False,
                    "message": f"未找到符合条件的考试安排"
                }
            
            # 按日期排序
            filtered_exams = sorted(filtered_exams, key=lambda x: (x.get('exam_date', ''), x.get('exam_time', '')))
            
            # 生成友好的文本输出
            output = self._format_exams_output(filtered_exams)
            
            return {
                "success": True,
                "exams": filtered_exams,
                "message": output
            }
            
        except Exception as e:
            logger.error(f"查询考试安排时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"查询考试安排时出错: {str(e)}"
            }
    
    def _normalize_semester(self, semester: str) -> str:
        """
        标准化学期格式，支持多种输入格式
        
        Args:
            semester: 学期字符串
        
        Returns:
            标准化后的学期格式（与数据库格式一致）
        """
        if not semester:
            return semester
        
        import re
        # 处理格式如 "2023-2024-1" -> "2023-2024学年第1学期"
        match = re.match(r'(\d{4})-(\d{4})-(\d)', semester)
        if match:
            year1, year2, term = match.groups()
            return f"{year1}-{year2}学年第{term}学期"
        
        return semester
    
    def _filter_exams(self, semester: str = None, course: str = None) -> List[Dict[str, Any]]:
        """
        过滤考试数据
        
        Args:
            semester: 学期筛选条件
            course: 课程名称筛选条件
        
        Returns:
            过滤后的考试列表
        """
        filtered = self.exams
        
        # 按学期过滤
        if semester and semester != "全部":
            normalized_semester = self._normalize_semester(semester)
            filtered = [e for e in filtered if normalized_semester in e.get('semester', '') or semester in e.get('semester', '')]
        
        # 按课程名称过滤
        if course:
            course_lower = course.lower()
            filtered = [e for e in filtered if course_lower in e.get('course_name', '').lower()]
        
        return filtered
    
    def _format_exams_output(self, exams: List[Dict[str, Any]]) -> str:
        """
        格式化考试输出
        
        Args:
            exams: 考试列表
        
        Returns:
            格式化的文本输出
        """
        if not exams:
            return "没有找到考试安排"
        
        output_parts = []
        current_date = None
        
        for exam in exams:
            exam_date = exam.get('exam_date', '待定')
            exam_time = exam.get('exam_time', '待定')
            course_name = exam.get('course_name', '未知课程')
            location = exam.get('exam_location', '待定')
            exam_type = exam.get('exam_type', '期末考试')
            note = exam.get('note', '')
            
            # 添加日期分隔
            if exam_date != current_date:
                if current_date is not None:
                    output_parts.append("")
                output_parts.append(f"📅 {exam_date}")
                current_date = exam_date
            
            output_parts.append(f"  ⏰ {exam_time} | {course_name}")
            output_parts.append(f"     地点: {location} | 类型: {exam_type}")
            
            if note:
                output_parts.append(f"     备注: {note}")
        
        return "\n".join(output_parts)
    
    def get_available_semesters(self) -> List[str]:
        """获取可用的学期列表"""
        semesters = set()
        for exam in self.exams:
            if 'semester' in exam:
                semesters.add(exam['semester'])
        
        # 排序：最新的在前面
        return sorted(list(semesters), reverse=True)
    
    def get_ui_components(self) -> Dict[str, Any]:
        """获取UI组件配置"""
        semesters = self.get_available_semesters()
        return {
            "type": "exam_query",
            "title": "考试查询",
            "description": "查询期末考试安排",
            "components": [
                {
                    "type": "dropdown",
                    "label": "选择学期",
                    "choices": ["全部"] + semesters,
                    "default": "全部",
                    "key": "semester"
                },
                {
                    "type": "button",
                    "label": "查询考试",
                    "action": "query_exam"
                },
                {
                    "type": "textbox",
                    "label": "查询结果",
                    "key": "result",
                    "readonly": True
                }
            ]
        }
