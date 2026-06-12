"""
数据库初始化脚本
将模拟数据导入到数据库中
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import DatabaseManager
from data.mock_data import MOCK_STUDENT
from utils.logger import get_logger


def init_database_with_mock_data():
    """初始化数据库并导入模拟数据"""
    logger =  get_logger("database_init")
    
    try:
        # 创建数据库管理器
        db_manager = DatabaseManager()
        logger.info("数据库管理器创建成功")
        
        # 添加教室数据
        logger.info("开始导入教室数据...")
        classrooms = [
            {'building': 'A栋', 'room_number': '101', 'capacity': 50, 'has_projector': True, 'has_computer': True, 'has_air_conditioner': True},
            {'building': 'A栋', 'room_number': '203', 'capacity': 40, 'has_projector': True, 'has_computer': True, 'has_air_conditioner': True},
            {'building': 'B栋', 'room_number': '305', 'capacity': 60, 'has_projector': True, 'has_computer': False, 'has_air_conditioner': True},
            {'building': 'B栋', 'room_number': '407', 'capacity': 30, 'has_projector': False, 'has_computer': True, 'has_air_conditioner': True},
            {'building': 'C栋', 'room_number': '502', 'capacity': 45, 'has_projector': True, 'has_computer': True, 'has_air_conditioner': True},
        ]
        
        for classroom in classrooms:
            db_manager.add_classroom(classroom)
        logger.info(f"教室数据导入完成，共 {len(classrooms)} 条")
        
        # 添加通知数据
        logger.info("开始导入通知数据...")
        notices = [
            {'title': '校园网升级通知', 'content': '为了提供更好的网络服务，学校将于6月5日进行校园网升级，届时可能会影响网络使用。', 'category': '网络', 'priority': 'normal', 'publish_date': '2026-06-05', 'publisher': '网络中心'},
            {'title': '期末考试安排发布', 'content': '2026年春季学期期末考试安排已发布，请同学们及时查询并做好考试准备。', 'category': '考试', 'priority': 'important', 'publish_date': '2026-06-08', 'publisher': '教务处'},
            {'title': '暑假开始通知', 'content': '2026年暑假将于6月15日正式开始，请同学们注意安全，合理安排假期时间。', 'category': '假期', 'priority': 'normal', 'publish_date': '2026-06-15', 'publisher': '学生处'},
            {'title': '选课系统开放', 'content': '2026年秋季学期选课系统将于6月20日开放，请同学们提前了解课程信息并按时选课。', 'category': '选课', 'priority': 'important', 'publish_date': '2026-06-20', 'publisher': '教务处'},
            {'title': '成绩查询开放', 'content': '2026年春季学期成绩将于6月25日开放查询，请同学们及时查询。', 'category': '成绩', 'priority': 'normal', 'publish_date': '2026-06-25', 'publisher': '教务处'},
        ]
        
        for notice in notices:
            db_manager.add_notice(notice)
        logger.info(f"通知数据导入完成，共 {len(notices)} 条")
        
        # 添加知识库数据
        logger.info("开始导入知识库数据...")
        knowledge_items = [
            {
                'question': '如何查询成绩？',
                'answer': '可以通过智能助手询问"查询成绩"或"我的成绩"，系统会显示所有学期的成绩信息。也可以指定学期查询，如"查询2024春季学期成绩"。',
                'category': '成绩查询',
                'keywords': ['成绩', '查询', 'GPA', '学分']
            },
            {
                'question': '如何查询课表？',
                'answer': '可以通过智能助手询问"查询课表"或"我的课表"，系统会显示完整的周课表。也可以查询特定日期，如"今天有什么课"或"周一的课表"。',
                'category': '课表查询',
                'keywords': ['课表', '课程', '上课', '时间']
            },
            {
                'question': '如何查询空教室？',
                'answer': '可以通过智能助手询问"查询空教室"或"有哪些空教室"，系统会显示当前可用的教室列表。也可以搜索特定教室，如"搜索A栋教室"。',
                'category': '教室查询',
                'keywords': ['教室', '空教室', '自习', '学习']
            },
            {
                'question': '如何查询考试安排？',
                'answer': '可以通过智能助手询问"查询考试"或"考试安排"，系统会显示所有考试信息。也可以查询特定科目，如"数学考试什么时候"。',
                'category': '考试查询',
                'keywords': ['考试', '期末', '安排', '时间']
            },
            {
                'question': '如何查询通知？',
                'answer': '可以通过智能助手询问"查询通知"或"最新通知"，系统会显示最新的校园通知。也可以查询重要通知或特定分类的通知。',
                'category': '通知查询',
                'keywords': ['通知', '公告', '消息', '重要']
            },
            {
                'question': '系统支持哪些功能？',
                'answer': '系统支持以下功能：1. AI智能助手 - 自然语言对话查询；2. 成绩查询 - 查询各学期成绩和GPA；3. 课表查询 - 查询周课表和今日课表；4. 教室查询 - 查询空教室和搜索教室；5. 考试查询 - 查询考试安排；6. 通知查询 - 查询校园通知。',
                'category': '系统功能',
                'keywords': ['功能', '支持', '帮助', '使用']
            }
        ]
        
        for knowledge in knowledge_items:
            db_manager.add_knowledge(knowledge)
        logger.info(f"知识库数据导入完成，共 {len(knowledge_items)} 条")
        
        # 获取数据库统计信息
        stats = db_manager.get_database_stats()
        logger.info("数据库统计信息：")
        for table, count in stats.items():
            logger.info(f"  {table}: {count} 条记录")
        
        logger.info("数据库初始化完成！")
        return True
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        return False


if __name__ == "__main__":
    print("开始初始化数据库...")
    success = init_database_with_mock_data()
    if success:
        print("数据库初始化成功！")
    else:
        print("数据库初始化失败！")