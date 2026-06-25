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
    # 第一教学楼 (H1xxx) - H1101表示第一教学楼一楼1101教室
    "H1101", "H1102", "H1103", "H1104", "H1105", "H1106", "H1107", "H1108",
    "H1201", "H1202", "H1203", "H1204", "H1205", "H1206", "H1207", "H1208",
    "H1301", "H1302", "H1303", "H1304", "H1305", "H1306", "H1307", "H1308",
    "H1401", "H1402", "H1403", "H1404", "H1405", "H1406", "H1407", "H1408",
    "H1501", "H1502", "H1503", "H1504", "H1505", "H1506", "H1507", "H1508",
    "H1601", "H1602", "H1603", "H1604", "H1605", "H1606", "H1607", "H1608",
    # 第二教学楼 (H2xxx)
    "H2101", "H2102", "H2103", "H2104", "H2105", "H2106", "H2107", "H2108",
    "H2201", "H2202", "H2203", "H2204", "H2205", "H2206", "H2207", "H2208",
    "H2301", "H2302", "H2303", "H2304", "H2305", "H2306", "H2307", "H2308",
    "H2401", "H2402", "H2403", "H2404", "H2405", "H2406", "H2407", "H2408",
    "H2501", "H2502", "H2503", "H2504", "H2505", "H2506", "H2507", "H2508",
    "H2601", "H2602", "H2603", "H2604", "H2605", "H2606", "H2607", "H2608",
    # 第三教学楼 (H3xxx)
    "H3101", "H3102", "H3103", "H3104", "H3105", "H3106", "H3107", "H3108",
    "H3201", "H3202", "H3203", "H3204", "H3205", "H3206", "H3207", "H3208",
    "H3301", "H3302", "H3303", "H3304", "H3305", "H3306", "H3307", "H3308",
    "H3401", "H3402", "H3403", "H3404", "H3405", "H3406", "H3407", "H3408",
    "H3501", "H3502", "H3503", "H3504", "H3505", "H3506", "H3507", "H3508",
    "H3601", "H3602", "H3603", "H3604", "H3605", "H3606", "H3607", "H3608",
    # 第四教学楼 (H4xxx)
    "H4101", "H4102", "H4103", "H4104", "H4105", "H4106", "H4107", "H4108",
    "H4201", "H4202", "H4203", "H4204", "H4205", "H4206", "H4207", "H4208",
    "H4301", "H4302", "H4303", "H4304", "H4305", "H4306", "H4307", "H4308",
    "H4401", "H4402", "H4403", "H4404", "H4405", "H4406", "H4407", "H4408",
    "H4501", "H4502", "H4503", "H4504", "H4505", "H4506", "H4507", "H4508",
    "H4601", "H4602", "H4603", "H4604", "H4605", "H4606", "H4607", "H4608",
    # 第五教学楼 (H5xxx)
    "H5101", "H5102", "H5103", "H5104", "H5105", "H5106", "H5107", "H5108",
    "H5201", "H5202", "H5203", "H5204", "H5205", "H5206", "H5207", "H5208",
    "H5301", "H5302", "H5303", "H5304", "H5305", "H5306", "H5307", "H5308",
    "H5401", "H5402", "H5403", "H5404", "H5405", "H5406", "H5407", "H5408",
    "H5501", "H5502", "H5503", "H5504", "H5505", "H5506", "H5507", "H5508",
    "H5601", "H5602", "H5603", "H5604", "H5605", "H5606", "H5607", "H5608"
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
TERMS =  [
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


def generate_schedule_data() -> Dict[str, List[Dict[str, str]]]:
    """生成真实课表数据（包含所有学期）"""
    # 2023-2024学年第1学期（大一上学期）
    semester_2023_2024_1 = [
        # 星期一
        {'weekday': '星期一', 'period': '第1节', 'course_name': '人工智能导论', 'teacher': '尹庆', 'location': 'H1104', 'weeks': '9-14周'},
        {'weekday': '星期一', 'period': '第2节', 'course_name': '线性代数C', 'teacher': '牟谷芳', 'location': 'H1601', 'weeks': '1-12周'},
        {'weekday': '星期一', 'period': '第5节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H4203', 'weeks': '10周'},
        {'weekday': '星期一', 'period': '第6节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H4203', 'weeks': '10周'},
        {'weekday': '星期一', 'period': '第7节', 'course_name': '思想道德与法治', 'teacher': '李菁', 'location': 'H2303', 'weeks': '3-17周'},
        {'weekday': '星期一', 'period': '第8节', 'course_name': '思想道德与法治', 'teacher': '李菁', 'location': 'H2303', 'weeks': '3-17周'},
        # 星期二
        {'weekday': '星期二', 'period': '第1节', 'course_name': '高等数学1C', 'teacher': '青音', 'location': 'H2302', 'weeks': '1-16周'},
        {'weekday': '星期二', 'period': '第2节', 'course_name': '高等数学1C', 'teacher': '青音', 'location': 'H2302', 'weeks': '1-16周'},
        {'weekday': '星期二', 'period': '第3节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H4201', 'weeks': '9周'},
        {'weekday': '星期二', 'period': '第4节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H1106', 'weeks': '3-8周'},
        {'weekday': '星期二', 'period': '第5节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H2105', 'weeks': '11-12周'},
        {'weekday': '星期二', 'period': '第6节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H1106', 'weeks': '3-8周'},
        {'weekday': '星期二', 'period': '第7节', 'course_name': '大学英语1', 'teacher': '陈桂林', 'location': 'H1304', 'weeks': '3-14周'},
        {'weekday': '星期二', 'period': '第8节', 'course_name': '大学英语1', 'teacher': '陈桂林', 'location': 'H1304', 'weeks': '3-14周'},
        # 星期三
        {'weekday': '星期三', 'period': '第1节', 'course_name': '线性代数C', 'teacher': '牟谷芳', 'location': 'H1601', 'weeks': '3-12周'},
        {'weekday': '星期三', 'period': '第2节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H1601', 'weeks': '3-12周'},
        {'weekday': '星期三', 'period': '第4节', 'course_name': '人工智能导论', 'teacher': '尹庆', 'location': 'H4504', 'weeks': '9-14周'},
        {'weekday': '星期三', 'period': '第5节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H1206', 'weeks': '11-12周'},
        {'weekday': '星期三', 'period': '第6节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H1206', 'weeks': '11-12周'},
        # 星期四
        {'weekday': '星期四', 'period': '第1节', 'course_name': '大学英语1', 'teacher': '陈桂林', 'location': 'H4304', 'weeks': '3-14周'},
        {'weekday': '星期四', 'period': '第2节', 'course_name': '大学英语1', 'teacher': '陈桂林', 'location': 'H4304', 'weeks': '3-14周'},
        {'weekday': '星期四', 'period': '第5节', 'course_name': '人生规划与职业教育', 'teacher': '李英', 'location': 'H2205', 'weeks': '9-10周'},
        {'weekday': '星期四', 'period': '第6节', 'course_name': '人生规划与职业教育', 'teacher': '李英', 'location': 'H4201', 'weeks': '11-14周'},
        {'weekday': '星期四', 'period': '第7节', 'course_name': '思想道德与法治', 'teacher': '李菁', 'location': 'H1206', 'weeks': '11-14周'},
        {'weekday': '星期四', 'period': '第8节', 'course_name': 'C语言程序设计', 'teacher': '李雪冬', 'location': 'H1305', 'weeks': '3-10周'},
        # 星期五
        {'weekday': '星期五', 'period': '第3节', 'course_name': '高等数学1C', 'teacher': '青音', 'location': 'H2302', 'weeks': '1-16周'},
        {'weekday': '星期五', 'period': '第4节', 'course_name': '高等数学1C', 'teacher': '青音', 'location': 'H2302', 'weeks': '1-16周'},
        {'weekday': '星期五', 'period': '第5节', 'course_name': '体育1', 'teacher': '高健雄', 'location': '第二篮球场3', 'weeks': '双2-16周'},
        {'weekday': '星期五', 'period': '第6节', 'course_name': '体育1', 'teacher': '高健雄', 'location': '第二篮球场3', 'weeks': '双2-16周'},
    ]
    
    # 2023-2024学年第2学期（大一下学期）
    semester_2023_2024_2 = [
        # 星期一
        {'weekday': '星期一', 'period': '第3节', 'course_name': '大学英语2', 'teacher': '胡云', 'location': 'H4306', 'weeks': '双2-16周'},
        {'weekday': '星期一', 'period': '第4节', 'course_name': '大学英语2', 'teacher': '胡云', 'location': 'H4306', 'weeks': '双2-16周'},
        {'weekday': '星期一', 'period': '第5节', 'course_name': '中国近现代史纲要', 'teacher': '冯波', 'location': 'H2103', 'weeks': '1-17周'},
        {'weekday': '星期一', 'period': '第6节', 'course_name': '中国近现代史纲要', 'teacher': '冯波', 'location': 'H2103', 'weeks': '1-17周'},
        {'weekday': '星期一', 'period': '第7节', 'course_name': '软件工程导论', 'teacher': '李雪冬', 'location': 'H4502', 'weeks': '9-14周'},
        {'weekday': '星期一', 'period': '第8节', 'course_name': 'TRIZ创新方法', 'teacher': '李凡', 'location': 'H1206', 'weeks': '9-15周'},
        {'weekday': '星期一', 'period': '第9节', 'course_name': 'TRIZ创新方法', 'teacher': '李凡', 'location': 'H1206', 'weeks': '9-15周'},
        # 星期二
        {'weekday': '星期二', 'period': '第1节', 'course_name': '高等数学2C', 'teacher': '青音', 'location': 'H2106', 'weeks': '1-16周'},
        {'weekday': '星期二', 'period': '第2节', 'course_name': '高等数学2C', 'teacher': '青音', 'location': 'H2106', 'weeks': '1-16周'},
        {'weekday': '星期二', 'period': '第3节', 'course_name': '大学物理B', 'teacher': '胡琳', 'location': 'H2305', 'weeks': '1-13周'},
        {'weekday': '星期二', 'period': '第4节', 'course_name': '大学物理B', 'teacher': '胡琳', 'location': 'H2305', 'weeks': '1-13周'},
        {'weekday': '星期二', 'period': '第5节', 'course_name': '体育2', 'teacher': '高健雄', 'location': '第二篮球场3', 'weeks': '双2-16周'},
        {'weekday': '星期二', 'period': '第6节', 'course_name': '体育2', 'teacher': '高健雄', 'location': '第二篮球场3', 'weeks': '双2-16周'},
        {'weekday': '星期二', 'period': '第7节', 'course_name': '计算机组成原理B', 'teacher': '何磊', 'location': 'H1208', 'weeks': '1-16周'},
        {'weekday': '星期二', 'period': '第8节', 'course_name': '计算机组成原理B', 'teacher': '何磊', 'location': 'H1208', 'weeks': '1-16周'},
        {'weekday': '星期二', 'period': '第9节', 'course_name': '形势与政策', 'teacher': '李正义', 'location': 'H2104', 'weeks': '1-8周'},
        {'weekday': '星期二', 'period': '第10节', 'course_name': '形势与政策', 'teacher': '李正义', 'location': 'H2104', 'weeks': '1-8周'},
        # 星期三
        {'weekday': '星期三', 'period': '第1节', 'course_name': '软件工程导论', 'teacher': '李雪冬', 'location': 'H4409', 'weeks': '9-14周'},
        {'weekday': '星期三', 'period': '第2节', 'course_name': '软件工程导论', 'teacher': '李雪冬', 'location': 'H4409', 'weeks': '9-14周'},
        {'weekday': '星期三', 'period': '第3节', 'course_name': '数据结构', 'teacher': '高琳', 'location': 'H4502', 'weeks': '1-13周'},
        {'weekday': '星期三', 'period': '第4节', 'course_name': '数据结构', 'teacher': '高琳', 'location': 'H4502', 'weeks': '1-11周'},
        {'weekday': '星期三', 'period': '第5节', 'course_name': '中国近现代史纲要', 'teacher': '冯波', 'location': 'H2103', 'weeks': '1-5周'},
        {'weekday': '星期三', 'period': '第7节', 'course_name': '高等数学2C', 'teacher': '青音', 'location': 'H4207', 'weeks': '1-11周'},
        {'weekday': '星期三', 'period': '第8节', 'course_name': '高等数学2C', 'teacher': '青音', 'location': 'H4207', 'weeks': '1-11周'},
        {'weekday': '星期三', 'period': '第9节', 'course_name': '古生物的那些事儿', 'teacher': '黄婷', 'location': 'H1202', 'weeks': '1-11周'},
        {'weekday': '星期三', 'period': '第10节', 'course_name': '古生物的那些事儿', 'teacher': '黄婷', 'location': 'H1202', 'weeks': '1-10周'},
        {'weekday': '星期三', 'period': '第11节', 'course_name': '古生物的那些事儿', 'teacher': '黄婷', 'location': 'H1202', 'weeks': '1-10周'},
        # 星期四
        {'weekday': '星期四', 'period': '第1节', 'course_name': '计算机组成原理B', 'teacher': '何磊', 'location': 'H1208', 'weeks': '1-11周'},
        {'weekday': '星期四', 'period': '第2节', 'course_name': '计算机组成原理B', 'teacher': '何磊', 'location': 'H1208', 'weeks': '1-11周'},
        {'weekday': '星期四', 'period': '第3节', 'course_name': '大学英语2', 'teacher': '胡云', 'location': 'H4307', 'weeks': '1-16周'},
        {'weekday': '星期四', 'period': '第4节', 'course_name': '大学英语2', 'teacher': '胡云', 'location': 'H4307', 'weeks': '1-16周'},
        {'weekday': '星期四', 'period': '第5节', 'course_name': '数据结构', 'teacher': '高琳', 'location': 'H4307', 'weeks': '1-11周'},
        {'weekday': '星期四', 'period': '第6节', 'course_name': '数据结构', 'teacher': '高琳', 'location': 'H4307', 'weeks': '1-11周'},
        {'weekday': '星期四', 'period': '第7节', 'course_name': '大学物理B', 'teacher': '胡云', 'location': 'H1205', 'weeks': '1-13周'},
        {'weekday': '星期四', 'period': '第8节', 'course_name': '大学物理B', 'teacher': '胡云', 'location': 'H1205', 'weeks': '1-13周'},
        {'weekday': '星期四', 'period': '第9节', 'course_name': 'TRIZ创新方法', 'teacher': '李凡', 'location': 'H1206', 'weeks': '9-13周'},
        {'weekday': '星期四', 'period': '第10节', 'course_name': 'TRIZ创新方法', 'teacher': '李凡', 'location': 'H1206', 'weeks': '9-13周'},
        # 星期五
        {'weekday': '星期五', 'period': '第1节', 'course_name': '数据结构', 'teacher': '高琳', 'location': 'H4409', 'weeks': '1-13周'},
        {'weekday': '星期五', 'period': '第2节', 'course_name': '数据结构', 'teacher': '高琳', 'location': 'H4409', 'weeks': '1-13周'},
        {'weekday': '星期五', 'period': '第3节', 'course_name': '高等数学2C', 'teacher': '青音', 'location': 'H1206', 'weeks': '1-16周'},
        {'weekday': '星期五', 'period': '第4节', 'course_name': '高等数学2C', 'teacher': '青音', 'location': 'H1206', 'weeks': '1-16周'},
        {'weekday': '星期五', 'period': '第5节', 'course_name': '形势与政策', 'teacher': '李雪冬', 'location': 'H2305', 'weeks': '12-15周'},
        {'weekday': '星期五', 'period': '第6节', 'course_name': '形势与政策', 'teacher': '李雪冬', 'location': 'H2305', 'weeks': '12-15周'},
    ]
    
    # 2024-2025学年第1学期（大二上学期）
    semester_2024_2025_1 = [
        # 星期一
        {'weekday': '星期一', 'period': '第3节', 'course_name': '电路分析基础B', 'teacher': '姚玉琴', 'location': 'H1102', 'weeks': '1-12周'},
        {'weekday': '星期一', 'period': '第4节', 'course_name': '电路分析基础B', 'teacher': '姚玉琴', 'location': 'H1102', 'weeks': '1-12周'},
        {'weekday': '星期一', 'period': '第5节', 'course_name': '数字电路与逻辑设计B', 'teacher': '王雯', 'location': 'H4204', 'weeks': '1-10周'},
        {'weekday': '星期一', 'period': '第6节', 'course_name': '数字电路与逻辑设计B', 'teacher': '王雯', 'location': 'H4204', 'weeks': '1-10周'},
        {'weekday': '星期一', 'period': '第7节', 'course_name': '算法分析理论与设计', 'teacher': '刘颖,何青', 'location': 'H2103', 'weeks': '9-14周'},
        {'weekday': '星期一', 'period': '第8节', 'course_name': '算法分析理论与设计', 'teacher': '刘颖,何青', 'location': 'H2103', 'weeks': '9-14周'},
        # 星期二
        {'weekday': '星期二', 'period': '第1节', 'course_name': '操作系统原理', 'teacher': '王光斌', 'location': 'H4506', 'weeks': '1-12周'},
        {'weekday': '星期二', 'period': '第2节', 'course_name': '操作系统原理', 'teacher': '王光斌', 'location': 'H4506', 'weeks': '1-12周'},
        {'weekday': '星期二', 'period': '第3节', 'course_name': '体育3', 'teacher': '肖波', 'location': '网球场2', 'weeks': '1-10周'},
        {'weekday': '星期二', 'period': '第4节', 'course_name': '体育3', 'teacher': '肖波', 'location': '网球场2', 'weeks': '1-10周'},
        {'weekday': '星期二', 'period': '第5节', 'course_name': '马克思主义基本原理', 'teacher': '王雯', 'location': 'H4408', 'weeks': '1-17周'},
        {'weekday': '星期二', 'period': '第6节', 'course_name': '马克思主义基本原理', 'teacher': '王雯', 'location': 'H4408', 'weeks': '1-17周'},
        {'weekday': '星期二', 'period': '第7节', 'course_name': 'Python程序设计', 'teacher': '刘颖', 'location': 'H1504', 'weeks': '9-16周'},
        {'weekday': '星期二', 'period': '第8节', 'course_name': 'Python程序设计', 'teacher': '刘颖', 'location': 'H1504', 'weeks': '9-16周'},
        # 星期三
        {'weekday': '星期三', 'period': '第1节', 'course_name': '跨文化英语', 'teacher': '方芳', 'location': 'H4204', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第2节', 'course_name': '跨文化英语', 'teacher': '方芳', 'location': 'H4204', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第3节', 'course_name': '数字电路与逻辑设计B', 'teacher': '赵磊', 'location': 'H4205', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第4节', 'course_name': '数字电路与逻辑设计B', 'teacher': '赵磊', 'location': 'H4205', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第5节', 'course_name': '算法分析理论与设计', 'teacher': '王超', 'location': 'H1205', 'weeks': '9-14周'},
        {'weekday': '星期三', 'period': '第6节', 'course_name': '算法分析理论与设计', 'teacher': '王超', 'location': 'H1205', 'weeks': '9-14周'},
        {'weekday': '星期三', 'period': '第7节', 'course_name': '数据库原理及应用A', 'teacher': '方芳,邹欣怡', 'location': 'H1407', 'weeks': '4-13周'},
        {'weekday': '星期三', 'period': '第8节', 'course_name': '数据库原理及应用A', 'teacher': '方芳,邹欣怡', 'location': 'H1407', 'weeks': '4-13周'},
        # 星期四
        {'weekday': '星期四', 'period': '第1节', 'course_name': '操作系统原理', 'teacher': '王光斌', 'location': 'H4406', 'weeks': '1-12周'},
        {'weekday': '星期四', 'period': '第2节', 'course_name': '操作系统原理', 'teacher': '王光斌', 'location': 'H4406', 'weeks': '1-12周'},
        {'weekday': '星期四', 'period': '第3节', 'course_name': '电路分析基础B', 'teacher': '姚玉琴', 'location': 'H1206', 'weeks': '1-12周'},
        {'weekday': '星期四', 'period': '第4节', 'course_name': '电路分析基础B', 'teacher': '姚玉琴', 'location': 'H1206', 'weeks': '1-12周'},
        {'weekday': '星期四', 'period': '第5节', 'course_name': '创新创业教育基础', 'teacher': '胡庆霞,何青', 'location': 'H1205', 'weeks': '9-14周'},
        {'weekday': '星期四', 'period': '第6节', 'course_name': '创新创业教育基础', 'teacher': '胡庆霞,何青', 'location': 'H1205', 'weeks': '9-14周'},
        {'weekday': '星期四', 'period': '第9节', 'course_name': '世界文化与自然遗产赏析', 'teacher': '庞勇', 'location': 'H1208', 'weeks': '1-11周'},
        {'weekday': '星期四', 'period': '第10节', 'course_name': '世界文化与自然遗产赏析', 'teacher': '庞勇', 'location': 'H1208', 'weeks': '1-10周'},
        {'weekday': '星期四', 'period': '第11节', 'course_name': '世界文化与自然遗产赏析', 'teacher': '庞勇', 'location': 'H1208', 'weeks': '1-10周'},
        # 星期五
        {'weekday': '星期五', 'period': '第3节', 'course_name': 'Python程序设计', 'teacher': '刘颖', 'location': 'H1205', 'weeks': '9-16周'},
        {'weekday': '星期五', 'period': '第4节', 'course_name': 'Python程序设计', 'teacher': '刘颖', 'location': 'H1205', 'weeks': '9-16周'},
        {'weekday': '星期五', 'period': '第5节', 'course_name': '数据库原理及应用A', 'teacher': '方芳,邹欣怡', 'location': 'H1205', 'weeks': '4-12周'},
        {'weekday': '星期五', 'period': '第6节', 'course_name': '数据库原理及应用A', 'teacher': '方芳,邹欣怡', 'location': 'H1205', 'weeks': '4-12周'},
        {'weekday': '星期五', 'period': '第7节', 'course_name': '马克思主义基本原理', 'teacher': '王雯', 'location': 'H4204', 'weeks': '1-5周'},
        {'weekday': '星期五', 'period': '第8节', 'course_name': '形势与政策2', 'teacher': '张晓锋', 'location': 'H4204', 'weeks': '14-15周'},
    ]
    
    # 2024-2025学年第2学期（大二下学期）
    semester_2024_2025_2 = [
        # 星期一
        {'weekday': '星期一', 'period': '第3节', 'course_name': '机器学习', 'teacher': '卢蜀中', 'location': 'H1407', 'weeks': '1-10周'},
        {'weekday': '星期一', 'period': '第4节', 'course_name': '机器学习', 'teacher': '卢蜀中', 'location': 'H1407', 'weeks': '1-10周'},
        {'weekday': '星期一', 'period': '第5节', 'course_name': '信号与系统A', 'teacher': '孙曙光', 'location': 'H1207', 'weeks': '1-15周'},
        {'weekday': '星期一', 'period': '第6节', 'course_name': '信号与系统A', 'teacher': '孙曙光', 'location': 'H1207', 'weeks': '1-15周'},
        # 星期二
        {'weekday': '星期二', 'period': '第3节', 'course_name': '体育4', 'teacher': '肖波', 'location': '网球场1', 'weeks': '1-16周'},
        {'weekday': '星期二', 'period': '第4节', 'course_name': '体育4', 'teacher': '肖波', 'location': '网球场1', 'weeks': '1-16周'},
        {'weekday': '星期二', 'period': '第5节', 'course_name': '概率论与数理统计C', 'teacher': '陈勇刚', 'location': 'H4502', 'weeks': '1-15周'},
        {'weekday': '星期二', 'period': '第6节', 'course_name': '概率论与数理统计C', 'teacher': '陈勇刚', 'location': 'H4502', 'weeks': '1-15周'},
        {'weekday': '星期二', 'period': '第7节', 'course_name': '计算机网络A', 'teacher': '刘陆平', 'location': 'H1205', 'weeks': '5-16周'},
        {'weekday': '星期二', 'period': '第8节', 'course_name': '计算机网络A', 'teacher': '刘陆平', 'location': 'H1205', 'weeks': '5-16周'},
        # 星期三
        {'weekday': '星期三', 'period': '第3节', 'course_name': '信号与系统A', 'teacher': '孙曙光', 'location': 'H1207', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第4节', 'course_name': '信号与系统A', 'teacher': '孙曙光', 'location': 'H1207', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第5节', 'course_name': '科技英语', 'teacher': '刘芳', 'location': 'H4307', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第6节', 'course_name': '科技英语', 'teacher': '刘芳', 'location': 'H4307', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第7节', 'course_name': '毛泽东思想和中国特色社会主义理论体系概论', 'teacher': '李孟杰', 'location': 'H2208', 'weeks': '1-17周'},
        {'weekday': '星期三', 'period': '第8节', 'course_name': '毛泽东思想和中国特色社会主义理论体系概论', 'teacher': '李孟杰', 'location': 'H2208', 'weeks': '1-17周'},
        {'weekday': '星期三', 'period': '第9节', 'course_name': '创造性思维与创新方法', 'teacher': '李雪峰', 'location': 'H2104', 'weeks': '4,8,15周'},
        {'weekday': '星期三', 'period': '第10节', 'course_name': '创造性思维与创新方法', 'teacher': '李雪峰', 'location': 'H2104', 'weeks': '4,8,15周'},
        {'weekday': '星期三', 'period': '第11节', 'course_name': '创造性思维与创新方法', 'teacher': '李雪峰', 'location': 'H2104', 'weeks': '4,8,15周'},
        # 星期四
        {'weekday': '星期四', 'period': '第1节', 'course_name': '计算机网络A', 'teacher': '刘陆平', 'location': 'H1205', 'weeks': '1-16周'},
        {'weekday': '星期四', 'period': '第2节', 'course_name': '计算机网络A', 'teacher': '刘陆平', 'location': 'H1205', 'weeks': '1-16周'},
        {'weekday': '星期四', 'period': '第3节', 'course_name': '概率论与数理统计C', 'teacher': '陈勇刚', 'location': 'H14502', 'weeks': '1-12周'},
        {'weekday': '星期四', 'period': '第4节', 'course_name': '概率论与数理统计C', 'teacher': '陈勇刚', 'location': 'H14502', 'weeks': '1-12周'},
        # 星期五
        {'weekday': '星期五', 'period': '第1节', 'course_name': '机器学习', 'teacher': '卢蜀中', 'location': 'H1205', 'weeks': '1-10周'},
        {'weekday': '星期五', 'period': '第2节', 'course_name': '机器学习', 'teacher': '卢蜀中', 'location': 'H1205', 'weeks': '1-10周'},
        {'weekday': '星期五', 'period': '第3节', 'course_name': '形势与政策3', 'teacher': '陈亚菲', 'location': 'H4507', 'weeks': '11-14周'},
        {'weekday': '星期五', 'period': '第4节', 'course_name': '形势与政策3', 'teacher': '陈亚菲', 'location': 'H4507', 'weeks': '11-14周'},
        {'weekday': '星期五', 'period': '第5节', 'course_name': '毛泽东思想和中国特色社会主义理论体系概论', 'teacher': '李孟杰', 'location': 'H2204', 'weeks': '1-5周'},
        {'weekday': '星期五', 'period': '第6节', 'course_name': '毛泽东思想和中国特色社会主义理论体系概论', 'teacher': '李孟杰', 'location': 'H2204', 'weeks': '1-5周'},
    ]
    
    # 2025-2026学年第1学期（大三上学期）
    semester_2025_2026_1 = [
        # 星期一
        {'weekday': '星期一', 'period': '第2节', 'course_name': '习近平新时代中国特色社会主义思想概论', 'teacher': '李璐', 'location': 'H4203', 'weeks': '1-5周'},
        {'weekday': '星期一', 'period': '第3节', 'course_name': '习近平新时代中国特色社会主义思想概论', 'teacher': '李璐', 'location': 'H4203', 'weeks': '1-5周'},
        {'weekday': '星期一', 'period': '第5节', 'course_name': 'Web前端编程', 'teacher': '尹庆', 'location': 'H4204', 'weeks': '1-10周'},
        {'weekday': '星期一', 'period': '第6节', 'course_name': 'Web前端编程', 'teacher': '尹庆', 'location': 'H4204', 'weeks': '1-10周'},
        {'weekday': '星期一', 'period': '第7节', 'course_name': 'Hadoop大数据技术', 'teacher': '赵秋云', 'location': 'H1104', 'weeks': '1-5周'},
        {'weekday': '星期一', 'period': '第8节', 'course_name': 'Hadoop大数据技术', 'teacher': '赵秋云', 'location': 'H1104', 'weeks': '1-5周'},
        # 星期二
        {'weekday': '星期二', 'period': '第3节', 'course_name': '数字图像处理', 'teacher': '赵秋云', 'location': 'H6405', 'weeks': '11-18周'},
        {'weekday': '星期二', 'period': '第4节', 'course_name': '数字图像处理', 'teacher': '赵秋云', 'location': 'H6405', 'weeks': '11-18周'},
        {'weekday': '星期二', 'period': '第5节', 'course_name': '离散数学', 'teacher': '刘颖', 'location': 'H6405', 'weeks': '1-5周'},
        {'weekday': '星期二', 'period': '第6节', 'course_name': '离散数学', 'teacher': '刘颖', 'location': 'H6405', 'weeks': '1-5周'},
        {'weekday': '星期二', 'period': '第7节', 'course_name': 'Spark大数据技术', 'teacher': '郭继文', 'location': 'H1504', 'weeks': '11-15周'},
        {'weekday': '星期二', 'period': '第8节', 'course_name': 'Spark大数据技术', 'teacher': '郭继文', 'location': 'H1504', 'weeks': '11-15周'},
        # 星期三
        {'weekday': '星期三', 'period': '第1节', 'course_name': '深度学习基础', 'teacher': '刘颖,何长春', 'location': 'H1401', 'weeks': '1-10周'},
        {'weekday': '星期三', 'period': '第2节', 'course_name': '深度学习基础', 'teacher': '刘颖,何长春', 'location': 'H1401', 'weeks': '1-10周'},
        {'weekday': '星期三', 'period': '第3节', 'course_name': '体育5', 'teacher': '高琳', 'location': '第二田径场1', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第4节', 'course_name': '体育5', 'teacher': '高琳', 'location': '第二田径场1', 'weeks': '1-16周'},
        {'weekday': '星期三', 'period': '第5节', 'course_name': 'Hadoop大数据技术', 'teacher': '赵秋云', 'location': 'H1304', 'weeks': '1-12周'},
        {'weekday': '星期三', 'period': '第6节', 'course_name': 'Hadoop大数据技术', 'teacher': '赵秋云', 'location': 'H1304', 'weeks': '1-12周'},
        {'weekday': '星期三', 'period': '第7节', 'course_name': '习近平新时代中国特色社会主义思想概论', 'teacher': '郭继文', 'location': 'H4209', 'weeks': '1-17周'},
        {'weekday': '星期三', 'period': '第8节', 'course_name': '习近平新时代中国特色社会主义思想概论', 'teacher': '郭继文', 'location': 'H4209', 'weeks': '1-17周'},
        {'weekday': '星期三', 'period': '第10节', 'course_name': '大学生理财规划', 'teacher': '罗爽', 'location': 'H1201', 'weeks': '2-12周'},
        {'weekday': '星期三', 'period': '第11节', 'course_name': '大学生理财规划', 'teacher': '罗爽', 'location': 'H1201', 'weeks': '2-11周'},
        {'weekday': '星期三', 'period': '第12节', 'course_name': '大学生理财规划', 'teacher': '罗爽', 'location': 'H1201', 'weeks': '2-11周'},
        # 星期四
        {'weekday': '星期四', 'period': '第3节', 'course_name': '数字图像处理', 'teacher': '赵秋云', 'location': 'H4203', 'weeks': '11-18周'},
        {'weekday': '星期四', 'period': '第4节', 'course_name': '数字图像处理', 'teacher': '赵秋云', 'location': 'H4203', 'weeks': '11-18周'},
        # 星期五
        {'weekday': '星期五', 'period': '第1节', 'course_name': '知识图谱基础', 'teacher': '付仕明', 'location': 'H4509', 'weeks': '1-10周'},
        {'weekday': '星期五', 'period': '第2节', 'course_name': '知识图谱基础', 'teacher': '付仕明', 'location': 'H4509', 'weeks': '1-12周'},
        {'weekday': '星期五', 'period': '第3节', 'course_name': '离散数学', 'teacher': '刘颖', 'location': 'H4203', 'weeks': '1-12周'},
        {'weekday': '星期五', 'period': '第4节', 'course_name': '离散数学', 'teacher': '刘颖', 'location': 'H4203', 'weeks': '1-12周'},
        {'weekday': '星期五', 'period': '第5节', 'course_name': '形势与政策4', 'teacher': '周科宇', 'location': 'H1401', 'weeks': '11-14周'},
        {'weekday': '星期五', 'period': '第6节', 'course_name': '形势与政策4', 'teacher': '周科宇', 'location': 'H1401', 'weeks': '11-14周'},
        {'weekday': '星期五', 'period': '第7节', 'course_name': 'Spark大数据技术', 'teacher': '郭继文', 'location': 'H1304', 'weeks': '11-15周'},
        {'weekday': '星期五', 'period': '第8节', 'course_name': 'Spark大数据技术', 'teacher': '郭继文', 'location': 'H1304', 'weeks': '11-15周'},
        {'weekday': '星期五', 'period': '第9节', 'course_name': '深度学习基础', 'teacher': '刘颖,何长春', 'location': 'H1401', 'weeks': '1-10周'},
    ]
    
    # 2025-2026学年第2学期（大三下学期）
    semester_2025_2026_2 = [
        # 星期一
        {'weekday': '星期一', 'period': '第1节', 'course_name': '机器视觉技术', 'teacher': '刘强', 'location': 'H1407', 'weeks': '2-9周'},
        {'weekday': '星期一', 'period': '第2节', 'course_name': '机器视觉技术', 'teacher': '刘强', 'location': 'H1407', 'weeks': '2-9周'},
        {'weekday': '星期一', 'period': '第5节', 'course_name': '面向对象程序设计(JAVA)', 'teacher': '林玲', 'location': 'H1401', 'weeks': '2-9周'},
        # 星期二
        {'weekday': '星期二', 'period': '第5节', 'course_name': '就业指导', 'teacher': '高弘弘', 'location': 'H1404', 'weeks': '12-17周'},
        # 星期三
        {'weekday': '星期三', 'period': '第1节', 'course_name': '体育6', 'teacher': '廖兵', 'location': '第二田径场1', 'weeks': '1-17周'},
        {'weekday': '星期三', 'period': '第5节', 'course_name': '高级程序学习', 'teacher': '尹庆', 'location': 'H1401', 'weeks': '2-11周'},
        {'weekday': '星期三', 'period': '第6节', 'course_name': '面向对象程序设计(JAVA)', 'teacher': '林玲', 'location': 'H1401', 'weeks': '2-9周'},
        {'weekday': '星期三', 'period': '第7节', 'course_name': '面向对象程序设计(JAVA)', 'teacher': '林玲', 'location': 'H1401', 'weeks': '2-9周'},
    ]
    
    # 为每个课程添加学期信息
    for course in semester_2023_2024_1:
        course['semester'] = '2023-2024学年 第1学期'
    for course in semester_2023_2024_2:
        course['semester'] = '2023-2024学年 第2学期'
    for course in semester_2024_2025_1:
        course['semester'] = '2024-2025学年 第1学期'
    for course in semester_2024_2025_2:
        course['semester'] = '2024-2025学年 第2学期'
    for course in semester_2025_2026_1:
        course['semester'] = '2025-2026学年 第1学期'
    for course in semester_2025_2026_2:
        course['semester'] = '2025-2026学年 第2学期'
    
    return {
        '2023-2024-1': semester_2023_2024_1,
        '2023-2024-2': semester_2023_2024_2,
        '2024-2025-1': semester_2024_2025_1,
        '2024-2025-2': semester_2024_2025_2,
        '2025-2026-1': semester_2025_2026_1,
        '2025-2026-2': semester_2025_2026_2
    }


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


def generate_notice_data() -> List[Dict[str, str]]:
    """生成大量通知数据（返回字典格式）"""
    notices = []
    today = datetime.now()
    
    # 通知内容模板
    content_templates = {
        "教务通知": [
            {"title": "课程调整通知", "content": "因教师培训，本周三《高等数学》课程调整至周五下午"},
            {"title": "停课通知", "content": "接教务处通知，下周一停课一天，请同学们注意安排学习计划"},
            {"title": "补课安排", "content": "本周六上午补上周四因运动会耽误的课程"},
            {"title": "教学评估通知", "content": "本学期教学评估工作即将开始，请同学们配合完成评教"},
            {"title": "教材发放通知", "content": "新学期教材已到，请各班级学习委员统一领取"},
            {"title": "课程大纲更新", "content": "部分课程大纲已更新，请同学们登录教务系统查看"}
        ],
        "考试安排": [
            {"title": "期末考试安排发布", "content": "2024-2025学年第一学期期末考试安排已发布，请登录系统查询"},
            {"title": "补考通知", "content": "补考时间安排在开学后第二周，请相关同学准时参加"},
            {"title": "缓考申请截止", "content": "缓考申请将于本周五截止，请需要申请的同学抓紧时间"},
            {"title": "考试地点变更", "content": "《计算机网络》考试地点变更至H5207，请同学们注意"},
            {"title": "考试时间调整", "content": "《操作系统》考试时间调整为1月8日上午"},
            {"title": "诚信考试提醒", "content": "期末考试即将开始，请同学们遵守考试纪律，诚信应考"}
        ],
        "选课通知": [
            {"title": "选课系统开放", "content": "下学期选课系统已开放，请同学们在规定时间内完成选课"},
            {"title": "退选课截止", "content": "退选课时间将于本周日截止，请同学们确认选课结果"},
            {"title": "补选通知", "content": "补选阶段将于下周一开启，请未完成选课的同学注意"},
            {"title": "选课指南发布", "content": "2025-2026学年选课指南已发布，请同学们仔细阅读"},
            {"title": "热门课程推荐", "content": "本学期热门选修课程推荐名单已公布"},
            {"title": "选课注意事项", "content": "选课时请注意课程时间冲突问题"}
        ],
        "校园活动": [
            {"title": "校园招聘会", "content": "秋季校园招聘会将于11月15日在体育馆举行，欢迎同学们参加"},
            {"title": "文化节活动", "content": "第十二届校园文化节即将开幕，精彩活动等你来"},
            {"title": "体育赛事", "content": "校运会将于10月20日开幕，请各学院做好准备"},
            {"title": "社团招新", "content": "百团大战即将开始，欢迎新同学加入心仪的社团"},
            {"title": "文艺晚会", "content": "迎新文艺晚会将于本周五晚7点在大礼堂举行"},
            {"title": "讲座预告", "content": "著名学者XXX教授将于下周来校举办学术讲座"}
        ],
        "学术讲座": [
            {"title": "AI前沿讲座", "content": "人工智能前沿技术讲座系列本周继续，欢迎师生参加"},
            {"title": "学术论坛", "content": "计算机学院学术论坛将于本月底举行"},
            {"title": "专家报告", "content": "邀请中科院院士来校做专题报告"},
            {"title": "科研分享会", "content": "研究生科研成果分享会本周四下午举行"},
            {"title": "学术沙龙", "content": "每周三下午学术沙龙活动继续进行中"},
            {"title": "论文写作指导", "content": "图书馆将举办论文写作指导讲座"}
        ],
        "就业信息": [
            {"title": "企业宣讲会", "content": "华为技术有限公司将于下周来校举办宣讲会"},
            {"title": "招聘会信息", "content": "成都市春季大型招聘会将于3月举行"},
            {"title": "实习岗位发布", "content": "多家企业发布实习岗位，欢迎大三同学投递"},
            {"title": "就业指导讲座", "content": "就业指导中心将举办系列就业指导讲座"},
            {"title": "简历优化工作坊", "content": "本周六将举办简历优化工作坊"},
            {"title": "面试技巧培训", "content": "面试技巧培训课程开始报名"}
        ],
        "后勤服务": [
            {"title": "宿舍维修通知", "content": "本周将对学生宿舍进行例行检查和维修"},
            {"title": "食堂菜单更新", "content": "新学期食堂菜单已更新，新增多种菜品"},
            {"title": "校园网维护", "content": "今晚11点至凌晨2点将进行校园网络维护"},
            {"title": "图书馆开放时间调整", "content": "考试周图书馆开放时间延长至晚上11点"},
            {"title": "教学楼空调检修", "content": "H1教学楼空调系统将进行检修"},
            {"title": "校园绿化维护", "content": "后勤部门将对校园绿化进行维护"}
        ],
        "图书馆公告": [
            {"title": "新书到馆通知", "content": "近期到馆新书已上架，请读者前往借阅"},
            {"title": "数据库培训", "content": "图书馆将举办数据库使用培训"},
            {"title": "借阅期限延长", "content": "考试期间图书借阅期限延长至45天"},
            {"title": "特藏展览", "content": "图书馆将举办珍贵文献特藏展览"},
            {"title": "数字资源试用", "content": "新增多个数据库试用资源"},
            {"title": "图书馆活动周", "content": "读书月活动周即将开始"}
        ],
        "学生事务": [
            {"title": "奖学金申请", "content": "国家奖学金申请工作已开始，请符合条件的同学申请"},
            {"title": "助学金公示", "content": "2025年春季助学金名单已公示"},
            {"title": "评优通知", "content": "优秀学生评选工作即将开始"},
            {"title": "学生证补办", "content": "学生证补办工作每周三集中办理"},
            {"title": "学籍异动", "content": "本学期学籍异动申请已开始"},
            {"title": "毕业手续办理", "content": "2025届毕业生手续办理须知"}
        ],
        "安全提示": [
            {"title": "防火安全提醒", "content": "冬季天干物燥，请同学们注意防火安全，不要使用违规电器"},
            {"title": "防诈骗宣传", "content": "近期电信诈骗频发，请提高警惕，不要轻易相信陌生来电"},
            {"title": "交通安全提示", "content": "上下课高峰期请注意交通安全，遵守交通规则"},
            {"title": "宿舍安全检查", "content": "本周将进行宿舍安全检查，请配合检查工作"},
            {"title": "网络安全预警", "content": "注意保护个人信息，不要泄露账号密码"},
            {"title": "食品安全通知", "content": "夏季请注意饮食卫生，不吃变质食物"}
        ]
    }
    
    # 生成50条通知
    for i in range(50):
        notice_type = random.choice(NOTICE_TYPES)
        days_ago = random.randint(0, 30)
        notice_date = today - timedelta(days=days_ago)
        
        content = random.choice(content_templates[notice_type]).copy()
        content["time"] = notice_date.strftime("%Y-%m-%d %H:%M:%S")
        content["type"] = notice_type
        notices.append(content)
    
    return sorted(notices, key=lambda x: x["time"], reverse=True)


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
