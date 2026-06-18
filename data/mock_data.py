"""
模拟校园数据
提供用于测试的模拟学生数据
"""

from typing import Dict, List, Any


# 模拟学生数据
MOCK_STUDENT: Dict[str, Any] = {
    "id": "2023132060",
    "name": "蔡华兵",
    "grade": {
        "2025-2026-1": {
            "高等数学": 92,
            "Python编程": 95,
            "AI导论": 88
        },
        "2025-2026-2": {
            "机器学习": 90,
            "工程实践": 96
        }
    },
    "schedule": {
        "周一": ["高数", "英语", "", "Python", "", ""],
        "周二": ["AI导论", "", "体育课", "", "", ""],
        "周三": ["机器学习", "", "", "工程实践", "", ""],
        "周四": ["", "英语", "", "", "", ""],
        "周五": ["高数", "", "", "Python", "", ""]
    },
    "classroom": ["101", "203", "305", "407", "502"],
    "exam": [
        {
            "name": "高数",
            "time": "6月10日 上午9点",
            "location": "一教101"
        },
        {
            "name": "Python",
            "time": "6月12日 下午2点",
            "location": "二教203"
        },
        {
            "name": "机器学习",
            "time": "6月15日 上午10点",
            "location": "三教305"
        }
    ],
    "notice": [
        "6月5日 校园网升级通知",
        "6月8日 期末考试安排发布",
        "6月15日 暑假开始",
        "6月20日 选课系统开放",
        "6月25日 成绩查询开放"
    ]
}


def get_student_data(student_id: str = None) -> Dict[str, Any]:
    """
    获取学生数据
    
    Args:
        student_id: 学生ID，如果为None则返回默认学生数据
    
    Returns:
        学生数据字典
    """
    if student_id is None or student_id == MOCK_STUDENT["id"]:
        return MOCK_STUDENT.copy()
    else:
        # 返回空数据结构
        return {
            "id": student_id,
            "name": "未知学生",
            "grade": {},
            "schedule": {},
            "classroom": [],
            "exam": [],
            "notice": []
        }


def get_grade_data(term: str = None) -> Dict[str, Any]:
    """
    获取成绩数据
    
    Args:
        term: 学期，如果为None则返回全部成绩
    
    Returns:
        成绩数据字典
    """
    grade_data = MOCK_STUDENT["grade"]
    if term and term in grade_data:
        return grade_data[term].copy()
    return grade_data.copy()


def get_schedule_data(day: str = None) -> Dict[str, Any]:
    """
    获取课表数据
    
    Args:
        day: 星期，如果为None则返回全部课表
    
    Returns:
        课表数据字典
    """
    schedule_data = MOCK_STUDENT["schedule"]
    if day and day in schedule_data:
        return schedule_data[day].copy()
    return schedule_data.copy()


def get_classroom_data() -> List[str]:
    """
    获取教室数据
    
    Returns:
        教室列表
    """
    return MOCK_STUDENT["classroom"].copy()


def get_exam_data(subject: str = None) -> List[Dict[str, str]]:
    """
    获取考试数据
    
    Args:
        subject: 科目名称，如果为None则返回全部考试
    
    Returns:
        考试数据列表
    """
    exam_data = MOCK_STUDENT["exam"]
    if subject:
        return [exam for exam in exam_data if subject in exam["name"]]
    return exam_data.copy()


def get_notice_data(count: int = 5) -> List[str]:
    """
    获取通知数据
    
    Args:
        count: 返回通知数量
    
    Returns:
        通知列表
    """
    return MOCK_STUDENT["notice"][:count].copy()