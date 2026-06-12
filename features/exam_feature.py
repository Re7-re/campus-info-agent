"""
考试查询功能模块
"""

from typing import Dict, Any, Optional, List
from .base_feature import BaseFeature
from data.mock_data import MOCK_STUDENT
from datetime import datetime


class ExamFeature(BaseFeature):
    """
    考试查询功能模块
    支持查询考试安排、即将到来的考试等
    """
    
    def __init__(self):
        super().__init__(
            name="考试查询",
            description=" 查询期末考试安排信息"
        )
        self.exam_data = MOCK_STUDENT["exam"]
    
    def execute(self, subject: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        执行考试查询
        
        Args:
            subject: 科目名称，如果为None则查询全部
            **kwargs: 其他参数
        
        Returns:
            查询结果字典
        """
        try:
            if subject:
                # 查询指定科目考试
                matched_exams = [e for e in self.exam_data if subject in e["name"]]
                if matched_exams:
                    exam = matched_exams[0]
                    result = {
                        "success": True,
                        "subject": subject,
                        "exam": exam,
                        "message": f"【{exam['name']}】\n时间：{exam['time']}\n地点：{exam['location']}"
                    }
                else:
                    result = {
                        "success": False,
                        "message": f"未找到科目 {subject} 的考试安排"
                    }
            else:
                # 查询全部考试
                exam_list = "【考试安排】\n"
                for e in self.exam_data:
                    exam_list += f"{e['name']} | {e['time']} | {e['location']}\n"
                
                result = {
                    "success": True,
                    "exams": self.exam_data,
                    "message": exam_list
                }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"查询考试时出错: {str(e)}"
            }
    
    def get_ui_components(self) -> Dict[str, Any]:
        """
        获取UI组件配置
        
        Returns:
            UI组件配置字典
        """
        subjects = [e["name"] for e in self.exam_data]
        
        return {
            "type": "exam_query",
            "title": "考试查询",
            "description": "查询期末考试安排",
            "components": [
                {
                    "type": "dropdown",
                    "label": "选择科目",
                    "choices": ["全部"] + subjects,
                    "default": "全部",
                    "key": "subject"
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
    
    def get_upcoming_exams(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        获取即将到来的考试
        
        Args:
            days: 查询未来多少天的考试
        
        Returns:
            即将到来的考试列表
        """
        upcoming_exams = []
        today = datetime.now()
        
        for exam in self.exam_data:
            try:
                # 解析考试时间（简化处理，实际需要更复杂的时间解析）
                exam_date = self._parse_exam_date(exam["time"])
                if exam_date:
                    days_until = (exam_date - today).days
                    if 0 <= days_until <= days:
                        upcoming_exams.append({
                            **exam,
                            "days_until": days_until
                        })
            except Exception:
                continue
        
        # 按时间排序
        upcoming_exams.sort(key=lambda x: x["days_until"])
        return upcoming_exams
    
    def _parse_exam_date(self, time_str: str) -> Optional[datetime]:
        """
        解析考试时间字符串
        
        Args:
            time_str: 时间字符串
        
        Returns:
            解析后的日期时间对象
        """
        try:
            # 简化的时间解析逻辑
            # 实际应用中需要更复杂的时间解析
            if "月" in time_str and "日" in time_str:
                parts = time_str.split()
                date_part = parts[0]  # "6月10日"
                time_part = parts[1] if len(parts) > 1 else "上午9点"  # "上午9点"
                
                # 解析日期
                month_day = date_part.replace("月", "-").replace("日", "")
                current_year = datetime.now().year
                date_str = f"{current_year}-{month_day}"
                
                # 解析时间
                hour = 9  # 默认上午9点
                if "下午" in time_part:
                    hour = 14  # 默认下午2点
                elif "上午" in time_part:
                    hour = 9
                
                return datetime.strptime(f"{date_str} {hour}:00", "%Y-%m-%d %H:%M")
        except Exception:
            pass
        
        return None
    
    def get_exam_summary(self) -> Dict[str, Any]:
        """
        获取考试摘要信息
        
        Returns:
            考试摘要
        """
        upcoming = self.get_upcoming_exams()
        
        return {
            "total_exams": len(self.exam_data),
            "upcoming_exams": len(upcoming),
            "next_exam": upcoming[0] if upcoming else None,
            "message": f"共有 {len(self.exam_data)} 门考试，其中 {len(upcoming)} 门即将到来"
        }