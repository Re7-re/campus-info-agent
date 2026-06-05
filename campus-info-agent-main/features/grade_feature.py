"""
成绩查询功能模块
"""

from typing import Dict, Any, Optional, List
from .base_feature import BaseFeature
from data.mock_data import MOCK_STUDENT


class GradeFeature(BaseFeature):
    """
    成绩查询功能模块
    支持按学期查询成绩、查看全部成绩等
    """
    
    def __init__(self):
        super().__init__(
            name="成绩查询",
            description="查询学生各学期成绩信息"
        )
        self.grade_data = MOCK_STUDENT["grade"]
    
    def execute(self, term: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        执行成绩查询
        
        Args:
            term: 学期，如"2025-2026-1"，如果为None则查询全部
            **kwargs: 其他参数
        
        Returns:
            查询结果字典
        """
        try:
            if term and term in self.grade_data:
                # 查询指定学期成绩
                grades = self.grade_data[term]
                result = {
                    "success": True,
                    "term": term,
                    "grades": grades,
                    "message": f"【{term}成绩】\n" + "\n".join([f"{k}: {v}" for k, v in grades.items()])
                }
            else:
                # 查询全部成绩
                all_grades = ""
                for t, g in self.grade_data.items():
                    all_grades += f"【{t}】\n" + "\n".join([f"{k}: {v}" for k, v in g.items()]) + "\n"
                
                result = {
                    "success": True,
                    "term": "全部",
                    "grades": self.grade_data,
                    "message": all_grades
                }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"查询成绩时出错: {str(e)}"
            }
    
    def get_ui_components(self) -> Dict[str, Any]:
        """
        获取UI组件配置
        
        Returns:
            UI组件配置字典
        """
        return {
            "type": "grade_query",
            "title": "成绩查询",
            "description": "查询各学期成绩信息",
            "components": [
                {
                    "type": "dropdown",
                    "label": "选择学期",
                    "choices": ["全部"] + list(self.grade_data.keys()),
                    "default": "全部",
                    "key": "term"
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
    
    def get_available_terms(self) -> List[str]:
        """获取可用的学期列表"""
        return list(self.grade_data.keys())
    
    def get_gpa(self, term: Optional[str] = None) -> Dict[str, Any]:
        """
        计算GPA
        
        Args:
            term: 学期，如果为None则计算全部
        
        Returns:
            GPA信息
        """
        try:
            if term:
                grades = self.grade_data.get(term, {})
            else:
                grades = {}
                for term_grades in self.grade_data.values():
                    grades.update(term_grades)
            
            if not grades:
                return {"success": False, "message": "没有成绩数据"}
            
            # 简单的GPA计算（实际应用中需要根据学校标准调整）
            total_score = sum(grades.values())
            avg_score = total_score / len(grades)
            
            # 简单的GPA转换（4.0分制）
            if avg_score >= 90:
                gpa = 4.0
            elif avg_score >= 85:
                gpa = 3.7
            elif avg_score >= 82:
                gpa = 3.3
            elif avg_score >= 78:
                gpa = 3.0
            elif avg_score >= 75:
                gpa = 2.7
            elif avg_score >= 72:
                gpa = 2.3
            elif avg_score >= 68:
                gpa = 2.0
            elif avg_score >= 64:
                gpa = 1.5
            elif avg_score >= 60:
                gpa = 1.0
            else:
                gpa = 0.0
            
            return {
                "success": True,
                "avg_score": round(avg_score, 2),
                "gpa": gpa,
                "total_courses": len(grades),
                "message": f"平均分: {avg_score:.2f}, GPA: {gpa:.1f}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"计算GPA时出错: {str(e)}"
            }