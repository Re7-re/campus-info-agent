"""
成绩查询功能模块
支持真实数据和模拟数据的查询
"""

from typing import Dict, Any, Optional, List
from .base_feature import BaseFeature
from data.mock_data import MOCK_STUDENT
from utils.data_loader import data_loader
import logging

logger = logging.getLogger(__name__)


class GradeFeature(BaseFeature):
    """
    成绩查询功能模块
    支持按学期查询成绩、查看全部成绩、按课程名称筛选等
    """
    
    def __init__(self):
        super().__init__(
            name="成绩查询",
            description="查询学生各学期成绩信息"
        )
        # 尝试加载真实数据
        self.grades = data_loader.load_grades()
        
        # 如果没有真实数据，使用模拟数据
        if not self.grades:
            logger.warning("未加载到真实成绩数据，使用模拟数据")
            self._use_mock_data()
        else:
            logger.info(f"成功加载 {len(self.grades)} 条真实成绩记录")
    
    def _use_mock_data(self):
        """使用模拟数据"""
        self.grades = []
        # 将模拟数据转换为统一格式
        for semester, courses in MOCK_STUDENT["grade"].items():
            for course_name, score in courses.items():
                self.grades.append({
                    'semester': semester,
                    'course_name': course_name,
                    'score': score,
                    'credits': 3.0,  # 模拟学分
                    'grade_point': self._score_to_gpa(score)
                })
    
    def _score_to_gpa(self, score: float) -> float:
        """将分数转换为GPA"""
        if score >= 90:
            return 4.0
        elif score >= 85:
            return 3.7
        elif score >= 82:
            return 3.3
        elif score >= 78:
            return 3.0
        elif score >= 75:
            return 2.7
        elif score >= 72:
            return 2.3
        elif score >= 68:
            return 2.0
        elif score >= 64:
            return 1.5
        elif score >= 60:
            return 1.0
        else:
            return 0.0
    
    def execute(self, query: str = None, semester: str = None, course: str = None, **kwargs) -> Dict[str, Any]:
        """
        执行成绩查询
        
        Args:
            query: 查询关键词（兼容旧接口）
            semester: 学期筛选条件
            course: 课程名称筛选条件
            **kwargs: 其他参数
        
        Returns:
            查询结果字典
        """
        try:
            # 兼容旧接口：query参数作为关键词
            keyword = query or course or ''
            
            # 过滤数据
            filtered_grades = self._filter_grades(semester, keyword)
            
            if not filtered_grades:
                return {
                    "success": False,
                    "message": f"未找到符合条件的成绩记录"
                }
            
            # 按学期组织数据
            grades_by_semester = self._organize_by_semester(filtered_grades)
            
            # 生成友好的文本输出
            output = self._format_grades_output(grades_by_semester)
            
            # 计算统计信息
            stats = self._calculate_statistics(filtered_grades)
            
            return {
                "success": True,
                "grades": filtered_grades,
                "grades_by_semester": grades_by_semester,
                "statistics": stats,
                "message": output
            }
            
        except Exception as e:
            logger.error(f"查询成绩时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"查询成绩时出错: {str(e)}"
            }
    
    def _normalize_semester(self, semester: str) -> str:
        """
        标准化学期格式，支持多种输入格式
        
        Args:
            semester: 学期字符串
        
        Returns:
            标准化后的学期格式
        """
        if not semester:
            return semester
        
        # 处理格式如 "2023-2024-1" -> "2023-2024学年 第1学期"
        import re
        match = re.match(r'(\d{4})-(\d{4})-(\d)', semester)
        if match:
            year1, year2, term = match.groups()
            return f"{year1}-{year2}学年 第{term}学期"
        
        # 处理格式如 "2023-2024学年第1学期" -> "2023-2024学年 第1学期"
        semester = semester.replace('学年第', '学年 第')
        
        return semester
    
    def _filter_grades(self, semester: str = None, keyword: str = None) -> List[Dict[str, Any]]:
        """
        过滤成绩数据
        
        Args:
            semester: 学期筛选条件
            keyword: 关键词筛选条件
        
        Returns:
            过滤后的成绩列表
        """
        filtered = self.grades
        
        # 按学期过滤
        if semester and semester != "全部":
            normalized_semester = self._normalize_semester(semester)
            filtered = [g for g in filtered if normalized_semester in g.get('semester', '') or semester in g.get('semester', '')]
        
        # 按关键词过滤（匹配课程名称）
        if keyword:
            keyword_lower = keyword.lower()
            filtered = [g for g in filtered if keyword_lower in g.get('course_name', '').lower()]
        
        return filtered
    
    def _organize_by_semester(self, grades: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        按学期组织成绩数据
        
        Args:
            grades: 成绩列表
        
        Returns:
            按学期组织的成绩字典
        """
        organized = {}
        for grade in grades:
            semester = grade.get('semester', '未知学期')
            if semester not in organized:
                organized[semester] = []
            organized[semester].append(grade)
        
        # 按学期名称排序（最新的在前面）
        sorted_sems = sorted(organized.keys(), reverse=True)
        return {sem: organized[sem] for sem in sorted_sems}
    
    def _format_grades_output(self, grades_by_semester: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        格式化成绩输出
        
        Args:
            grades_by_semester: 按学期组织的成绩
        
        Returns:
            格式化的文本输出
        """
        output_parts = []
        
        for semester, grades in grades_by_semester.items():
            output_parts.append(f"\n【{semester}】")
            
            # 计算学期平均分
            scores = [g['score'] for g in grades if g.get('score')]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            for grade in grades:
                course_name = grade.get('course_name', '未知课程')
                score = grade.get('score', 0)
                credits = grade.get('credits', 0)
                grade_point = grade.get('grade_point', 0)
                
                # 根据分数给出评价
                rating = self._get_score_rating(score)
                output_parts.append(f"  {course_name}: {score:.0f}分 ({credits:.1f}学分, GPA:{grade_point:.1f}) {rating}")
            
            output_parts.append(f"  平均分: {avg_score:.2f}")
        
        return "\n".join(output_parts)
    
    def _get_score_rating(self, score: float) -> str:
        """根据分数给出评价"""
        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 70:
            return "中等"
        elif score >= 60:
            return "及格"
        else:
            return "不及格"
    
    def _calculate_statistics(self, grades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算成绩统计信息
        
        Args:
            grades: 成绩列表
        
        Returns:
            统计信息字典
        """
        if not grades:
            return {}
        
        scores = [g['score'] for g in grades if g.get('score')]
        credits = [g['credits'] for g in grades if g.get('credits')]
        
        total_credits = sum(credits)
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # 计算GPA
        total_points = sum([g['score'] * g['credits'] for g in grades if g.get('score') and g.get('credits')])
        gpa = total_points / total_credits if total_credits > 0 else 0
        
        # 分数段统计
        score_ranges = {
            "90-100": len([s for s in scores if s >= 90]),
            "80-89": len([s for s in scores if 80 <= s < 90]),
            "70-79": len([s for s in scores if 70 <= s < 80]),
            "60-69": len([s for s in scores if 60 <= s < 70]),
            "60以下": len([s for s in scores if s < 60])
        }
        
        return {
            "total_courses": len(grades),
            "total_credits": total_credits,
            "avg_score": round(avg_score, 2),
            "gpa": round(gpa, 2),
            "score_ranges": score_ranges,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0
        }
    
    def get_available_semesters(self) -> List[str]:
        """获取可用的学期列表"""
        semesters = set()
        for grade in self.grades:
            if 'semester' in grade:
                semesters.add(grade['semester'])
        
        # 排序：最新的在前面
        return sorted(list(semesters), reverse=True)
    
    def get_gpa(self, semester: str = None) -> Dict[str, Any]:
        """
        获取GPA
        
        Args:
            semester: 学期，None表示全部
        
        Returns:
            GPA信息
        """
        try:
            filtered = self._filter_grades(semester)
            stats = self._calculate_statistics(filtered)
            
            if not stats:
                return {"success": False, "message": "没有成绩数据"}
            
            return {
                "success": True,
                "semester": semester or "全部",
                "gpa": stats['gpa'],
                "avg_score": stats['avg_score'],
                "total_credits": stats['total_credits'],
                "total_courses": stats['total_courses'],
                "message": f"{semester or '全部学期'} GPA: {stats['gpa']:.2f}, 平均分: {stats['avg_score']:.2f}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"计算GPA时出错: {str(e)}"
            }
    
    def get_ui_components(self) -> Dict[str, Any]:
        """获取UI组件配置"""
        semesters = self.get_available_semesters()
        return {
            "type": "grade_query",
            "title": "成绩查询",
            "description": "查询各学期成绩信息",
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
                    "label": "查询成绩",
                    "action": "query_grade"
                },
                {
                    "type": "textbox",
                    "label": "查询结果",
                    "key": "result",
                    "readonly": True
                }
            ]
        }
