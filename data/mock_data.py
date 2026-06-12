"""
校园数据模块
支持真实教务数据和模拟数据
"""

from typing import Dict, List, Any
import random
import json
import os
from datetime import datetime, timedelta

# 尝试导入教务爬虫
try:
    from .cuit_spider import CuitSpider
    HAS_CUIT_SPIDER = True
except ImportError:
    HAS_CUIT_SPIDER = False

# ==================== 课程名称库 ====================
COURSES = [
    "高等数学", "线性代数", "概率统计", "离散数学", "复变函数",
    "Python编程", "Java编程", "C++程序设计", "数据结构", "算法设计",
    "AI导论", "机器学习", "深度学习", "计算机视觉", "自然语言处理",
    "数据挖掘", "数据库原理", "操作系统", "计算机网络", "软件工程",
    "人工智能", "神经网络", "模式识别", "数字信号处理", "图像处理",
    "软件工程", "软件测试", "系统架构", "云计算", "大数据技术",
    "Web开发", "移动开发", "嵌入式系统", "物联网", "区块链技术",
    "英语", "大学物理", "工程实践", "创新创业", "职业规划",
    "体育", "音乐欣赏", "艺术设计", "心理健康", "形势政策"
]

# ==================== 教室名称库 ====================
CLASSROOMS = [
    # 一教
    "一教101", "一教102", "一教103", "一教104", "一教105",
    "一教201", "一教202", "一教203", "一教204", "一教205",
    "一教301", "一教302", "一教303", "一教304", "一教305",
    "一教401", "一教402", "一教403", "一教404", "一教405",
    # 二教
    "二教101", "二教102", "二教103", "二教104", "二教105",
    "二教201", "二教202", "二教203", "二教204", "二教205",
    "二教301", "二教302", "二教303", "二教304", "二教305",
    "二教401", "二教402", "二教403", "二教404", "二教405",
    # 三教
    "三教101", "三教102", "三教103", "三教104", "三教105",
    "三教201", "三教202", "三教203", "三教204", "三教205",
    "三教301", "三教302", "三教303", "三教304", "三教305",
    "三教401", "三教402", "三教403", "三教404", "三教405",
    # 四教
    "四教101", "四教102", "四教103", "四教104", "四教105",
    "四教201", "四教202", "四教203", "四教204", "四教205",
    "四教301", "四教302", "四教303", "四教304", "四教305",
    "四教401", "四教402", "四教403", "四教404", "四教405",
    # 实验楼
    "实验楼A101", "实验楼A102", "实验楼A103", "实验楼A201", "实验楼A202",
    "实验楼B101", "实验楼B102", "实验楼B103", "实验楼B201", "实验楼B202"
]

# ==================== 教师名称库 ====================
TEACHERS = [
    "张教授", "李教授", "王教授", "刘教授", "陈教授",
    "赵副教授", "孙副教授", "周副教授", "吴副教授", "郑副教授",
    "黄讲师", "许讲师", "何讲师", "胡讲师", "马讲师",
    "朱老师", "林老师", "郭老师", "何老师", "罗老师"
]

# ==================== 通知类型 ====================
NOTICE_TYPES = [
    "教务通知", "考试安排", "选课通知", "校园活动", "学术讲座",
    "就业信息", "后勤服务", "图书馆公告", "学生事务", "安全提示"
]

# ==================== 学期列表 ====================
TERMS = [
    "2023-2024-1", "2023-2024-2",
    "2024-2025-1", "2024-2025-2",
    "2025-2026-1", "2025-2026-2"
]

# ==================== 星期列表 ====================
DAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# ==================== 时间段 ====================
TIME_SLOTS = ["第1-2节", "第3-4节", "第5-6节", "第7-8节", "第9-10节", "第11-12节"]


def generate_grade_data() -> Dict[str, Dict[str, int]]:
    """生成大量成绩数据"""
    grades = {}
    for term in TERMS:
        term_courses = random.sample(COURSES, random.randint(5, 8))
        term_grades = {course: random.randint(60, 100) for course in term_courses}
        grades[term] = term_grades
    return grades


# ==================== 时间段详细时间映射 ====================
TIME_SLOT_DETAILS = {
    0: {"slot": "第1-2节", "time": "08:00-09:35", "duration": "95分钟"},
    1: {"slot": "第3-4节", "time": "10:00-11:35", "duration": "95分钟"},
    2: {"slot": "第5-6节", "time": "14:00-15:35", "duration": "95分钟"},
    3: {"slot": "第7-8节", "time": "16:00-17:35", "duration": "95分钟"},
    4: {"slot": "第9-10节", "time": "19:00-20:35", "duration": "95分钟"},
    5: {"slot": "第11-12节", "time": "20:45-22:00", "duration": "75分钟"}
}


def generate_schedule_data() -> Dict[str, List[str]]:
    """生成大量课表数据（带详细时间）"""
    schedule = {}
    for day in DAYS:
        day_courses = []
        for period in range(6):
            if random.random() > 0.3:  # 70%概率有课
                course = random.choice(COURSES)
                classroom = random.choice(CLASSROOMS)
                teacher = random.choice(TEACHERS)
                time_info = TIME_SLOT_DETAILS[period]
                day_courses.append(f"{course}\n{time_info['time']} | {classroom} | {teacher}")
            else:
                day_courses.append("")
        schedule[day] = day_courses
    return schedule


def generate_exam_data() -> List[Dict[str, str]]:
    """生成大量考试数据"""
    exams = []
    today = datetime.now()
    
    for _ in range(50):
        course = random.choice(COURSES)
        exam_date = today + timedelta(days=random.randint(5, 60))
        exam_time = random.choice(["上午9:00", "上午10:30", "下午14:00", "下午15:30"])
        classroom = random.choice(CLASSROOMS)
        
        exams.append({
            "name": course,
            "time": f"{exam_date.month}月{exam_date.day}日 {exam_time}",
            "location": classroom,
            "duration": random.choice(["1小时30分", "2小时", "2小时30分"]),
            "type": random.choice(["期末考试", "期中考试", "随堂测验", "论文答辩"])
        })
    
    return sorted(exams, key=lambda x: x["time"])


def generate_notice_data() -> List[str]:
    """生成大量通知数据"""
    notices = []
    today = datetime.now()
    
    # 生成100条通知
    for i in range(100):
        notice_type = random.choice(NOTICE_TYPES)
        days_ago = random.randint(0, 30)
        notice_date = today - timedelta(days=days_ago)
        
        # 通知内容模板
        content_templates = {
            "教务通知": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['课程调整', '停课通知', '补课安排', '教学评估'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['教材发放', '课程大纲更新', '教学计划调整'])}"
            ],
            "考试安排": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['期末考试安排发布', '补考通知', '缓考申请截止'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['考试地点变更', '考试时间调整', '诚信考试提醒'])}"
            ],
            "选课通知": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['选课系统开放', '退选课截止', '补选通知'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['选课指南发布', '热门课程推荐', '选课注意事项'])}"
            ],
            "校园活动": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['校园招聘会', '文化节活动', '体育赛事'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['社团招新', '文艺晚会', '讲座预告'])}"
            ],
            "学术讲座": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['AI前沿讲座', '学术论坛', '专家报告'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['科研分享会', '学术沙龙', '论文写作指导'])}"
            ],
            "就业信息": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['企业宣讲会', '招聘会信息', '实习岗位发布'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['就业指导讲座', '简历优化工作坊', '面试技巧培训'])}"
            ],
            "后勤服务": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['宿舍维修通知', '食堂菜单更新', '校园网维护'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['图书馆开放时间调整', '教学楼空调检修', '校园绿化维护'])}"
            ],
            "图书馆公告": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['新书到馆通知', '数据库培训', '借阅期限延长'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['特藏展览', '数字资源试用', '图书馆活动周'])}"
            ],
            "学生事务": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['奖学金申请', '助学金公示', '评优通知'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['学生证补办', '学籍异动', '毕业手续办理'])}"
            ],
            "安全提示": [
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['防火安全提醒', '防诈骗宣传', '交通安全提示'])}",
                f"{notice_date.month}月{notice_date.day}日 {random.choice(['宿舍安全检查', '网络安全预警', '食品安全通知'])}"
            ]
        }
        
        content = random.choice(content_templates[notice_type])
        notices.append(content)
    
    return sorted(notices, reverse=True)


def generate_classroom_data() -> List[str]:
    """生成大量教室数据"""
    return CLASSROOMS.copy()


# ==================== 模拟学生数据 ====================
MOCK_STUDENT: Dict[str, Any] = {
    "id": "2023132060",
    "name": "蔡华兵",
    "grade": generate_grade_data(),
    "schedule": generate_schedule_data(),
    "classroom": generate_classroom_data(),
    "exam": generate_exam_data(),
    "notice": generate_notice_data()
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
        # 为其他学生生成随机数据
        return {
            "id": student_id,
            "name": f"学生{student_id[-4:]}",
            "grade": generate_grade_data(),
            "schedule": generate_schedule_data(),
            "classroom": generate_classroom_data(),
            "exam": generate_exam_data(),
            "notice": generate_notice_data()
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


def get_notice_data(count: int = 10) -> List[str]:
    """
    获取通知数据
    
    Args:
        count: 返回通知数量
    
    Returns:
        通知列表
    """
    return MOCK_STUDENT["notice"][:count].copy()


def get_all_terms() -> List[str]:
    """获取所有学期列表"""
    return TERMS.copy()


def get_all_days() -> List[str]:
    """获取所有星期列表"""
    return DAYS.copy()


# ==================== 真实教务数据支持 ====================

def load_cuit_data(filepath: str = "data/cuit_data.json") -> Dict[str, Any]:
    """
    从文件加载真实教务数据
    
    Args:
        filepath: 数据文件路径
    
    Returns:
        教务数据字典，如果文件不存在则返回空字典
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 加载教务数据失败: {str(e)}")
    return {}


def fetch_cuit_data(username: str, password: str, cookies: dict = None, save: bool = True) -> Dict[str, Any]:
    """
    从成都信息工程大学教务系统获取真实数据
    
    Args:
        username: 学号
        password: 密码
        cookies: 可选的登录Cookie（如果提供则直接使用Cookie访问）
        save: 是否保存到文件
    
    Returns:
        包含课表、成绩、考试、通知、教室的字典
    """
    if not HAS_CUIT_SPIDER:
        print("Cuit spider module not loaded")
        return {}
    
    try:
        # 使用Cookie或密码登录
        spider = CuitSpider(username, password, cookies=cookies)
        data = spider.get_all_data()
        
        if save and data:
            os.makedirs("data", exist_ok=True)
            with open("data/cuit_data.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("Cuit data saved to data/cuit_data.json")
        
        return data
    except Exception as e:
        print("Fetch cuit data failed: " + str(e))
        return {}


def update_student_with_cuit_data(student_id: str = None, 
                                   username: str = None, 
                                   password: str = None,
                                   cookies: dict = None) -> Dict[str, Any]:
    """
    使用真实教务数据更新学生信息
    
    Args:
        student_id: 学生ID
        username: 教务系统学号
        password: 教务系统密码
        cookies: 可选的登录Cookie
    
    Returns:
        更新后的学生数据
    """
    # 尝试加载已保存的教务数据
    cuit_data = load_cuit_data()
    
    # 如果没有保存的数据，尝试从教务系统获取
    if not cuit_data and username and password:
        cuit_data = fetch_cuit_data(username, password, cookies=cookies)
    
    # 如果获取到真实数据，更新学生信息
    if cuit_data:
        return {
            "id": username or student_id or "2023132060",
            "name": "蔡华兵",
            "grade": cuit_data.get("grade", MOCK_STUDENT["grade"]),
            "schedule": cuit_data.get("schedule", MOCK_STUDENT["schedule"]),
            "classroom": cuit_data.get("classroom", MOCK_STUDENT["classroom"]),
            "exam": cuit_data.get("exam", MOCK_STUDENT["exam"]),
            "notice": cuit_data.get("notice", MOCK_STUDENT["notice"])
        }
    
    # 返回模拟数据
    return get_student_data(student_id)
