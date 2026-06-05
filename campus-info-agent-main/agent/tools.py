# agent/tools.py
from langchain.tools import tool
from data.mock_data import MOCK_STUDENT

# 成绩查询工具
@tool
def query_grade(term: str = None):
    """查询学生成绩，支持按学期查询，不传参数返回全部成绩"""
    grade_data = MOCK_STUDENT["grade"]
    if term and term in grade_data:
        return f"【{term}成绩】\n" + "\n".join([f"{k}: {v}" for k, v in grade_data[term].items()])
    all_grades = ""
    for t, g in grade_data.items():
        all_grades += f"【{t}】\n" + "\n".join([f"{k}: {v}" for k, v in g.items()]) + "\n"
    return all_grades

# 课表查询工具
@tool
def query_schedule(day: str = None):
    """查询课表，支持按星期查询，不传参数返回全部课表"""
    schedule = MOCK_STUDENT["schedule"]
    if day and day in schedule:
        return f"【{day}课表】\n" + "\n".join([f"第{i+1}节：{v}" for i, v in enumerate(schedule[day]) if v])
    all_schedule = ""
    for d, s in schedule.items():
        all_schedule += f"【{d}】\n" + "\n".join([f"第{i+1}节：{v}" for i, v in enumerate(s) if v]) + "\n"
    return all_schedule

# 空教室查询
@tool
def query_classroom():
    """查询当前可用的空教室"""
    rooms = MOCK_STUDENT["classroom"]
    return "当前可用空教室：" + "、".join(rooms)

# 考试查询
@tool
def query_exam():
    """查询期末考试安排"""
    exams = MOCK_STUDENT["exam"]
    res = "【考试安排】\n"
    for e in exams:
        res += f"{e['name']} | {e['time']} | {e['location']}\n"
    return res

# 校园通知查询
@tool
def query_notice():
    """查询最新校园通知"""
    notices = MOCK_STUDENT["notice"]
    return "【校园通知】\n" + "\n".join([f"{i+1}. {n}" for i, n in enumerate(notices)])

# 工具列表（给智能体调用）
TOOLS = [
    query_grade,
    query_schedule,
    query_classroom,
    query_exam,
    query_notice
]