# agent/tools.py
from langchain.tools import tool

from data.mock_data import MOCK_STUDENT


@tool
def query_grade(term: str | None = None) -> str:
    """
    查询学生成绩。

    Args:
        term: 学期，如 "2025-2026-1"。不传则返回全部成绩。

    Returns:
        格式化的成绩字符串。
    """
    grade_data =MOCK_STUDENT["grade"]
    if term and term in grade_data:
        grades = grade_data[term]
        lines = [f"{k}: {v}" for k, v in grades.items()]
        return f"【{term}成绩】\n" + "\n".join(lines)

    all_lines = []
    for t, g in grade_data.items():
        lines = [f"{k}: {v}" for k, v in g.items()]
        all_lines.append(f"【{t}】\n" + "\n".join(lines))
    return "\n".join(all_lines)


@tool
def query_schedule(day: str | None = None) -> str:
    """
    查询课表。

    Args:
        day: 星期几，如 "周一"。不传则返回全部课表。

    Returns:
        格式化的课表字符串。
    """
    schedule =MOCK_STUDENT["schedule"]
    if day and day in schedule:
        courses = schedule[day]
        lines = [f"第{i+1}节：{v}" for i, v in enumerate(courses) if v]
        return f"【{day}课表】\n" + "\n".join(lines)

    all_lines = []
    for d, s in schedule.items():
        lines = [f"第{i+1}节：{v}" for i, v in enumerate(s) if v]
        all_lines.append(f"【{d}】\n" + "\n".join(lines))
    return "\n".join(all_lines)


@tool
def query_classroom()-> str:
    """查询当前可用的空教室。"""
    rooms = MOCK_STUDENT["classroom"]
    return f"当前可用空教室：{'、'.join(rooms)}"


@tool
def query_exam() -> str:
    """查询期末考试安排。"""
    exams = MOCK_STUDENT["exam"]
    lines = [f"{e['name']} | {e['time']} | {e['location']}" for e in exams]
    return "【考试安排】\n" + "\n".join(lines)


@tool
def query_notice() -> str:
    """查询最新校园通知。"""
    notices =MOCK_STUDENT["notice"]
    lines = [f"{i+1}. {n}" for i, n in enumerate(notices)]
    return "【校园通知】\n" + "\n".join(lines)


# 工具列表（供智能体调用）
TOOLS = [query_grade, query_schedule, query_classroom, query_exam, query_notice]