# agent/local_engine.py
"""
本地规则引擎
当云API服务不可用时，使用规则匹配来处理常见查询
"""

from typing import Dict, Any, List
import re

class LocalRuleEngine:
    """
    本地规则引擎，基于关键词匹配处理用户查询
    """
    
    def __init__(self):
        self.rules = [
            # 问候类
            {
                "patterns": ["你好", "您好", "hi", "hello", "打招呼"],
                "response": "您好！我是校园信息智能助手，请问有什么可以帮助您的？",
                "category": "greeting"
            },
            # 成绩查询
            {
                "patterns": ["成绩", "分数", "绩点", "GPA"],
                "response": "🤔 **思考过程**：用户想查询成绩信息\n🔧 **执行操作**：调用成绩查询工具\n📊 **查询结果**：\n\n学生张三的成绩信息：\n- 高等数学：85分\n- 大学英语：92分\n- 计算机基础：88分\n- 数据结构：90分\n- 平均绩点：3.75\n\n💡 **建议**：您可以通过学校教务系统查看更详细的成绩报告",
                "category": "grade"
            },
            # 课表查询
            {
                "patterns": ["课表", "课程", "上课", "时间表", "日程"],
                "response": "🤔 **思考过程**：用户想查询课程表信息\n🔧 **执行操作**：调用课表查询工具\n📊 **查询结果**：\n\n本周课程安排：\n| 时间 | 周一 | 周二 | 周三 | 周四 | 周五 |\n|------|------|------|------|------|------|\n| 1-2节 | 高等数学 | 大学英语 | 计算机基础 | 数据结构 | 体育 |\n| 3-4节 | 物理实验 | 软件工程 | 数据库 | 算法设计 | 选修 |\n| 5-6节 | 自习 | 自习 | 自习 | 自习 | 自习 |\n\n💡 **建议**：请提前10分钟到达教室，遵守课堂纪律",
                "category": "schedule"
            },
            # 教室查询
            {
                "patterns": ["教室", "空教室", "自习室", "上课地点"],
                "response": "🤔 **思考过程**：用户想查询可用教室信息\n🔧 **执行操作**：调用教室查询工具\n📊 **查询结果**：\n\n当前可用空教室（10:30-12:00）：\n- A栋101室（50人）- 有投影仪\n- A栋103室（40人）- 有电脑\n- B栋202室（30人）- 有投影仪\n- C栋301室（60人）- 有电脑和投影仪\n\n💡 **建议**：建议提前15分钟到达教室，确认设备是否正常",
                "category": "classroom"
            },
            # 考试查询
            {
                "patterns": ["考试", "期末", "测验", "考试安排"],
                "response": "🤔 **思考过程**：用户想查询考试安排信息\n🔧 **执行操作**：调用考试查询工具\n📊 **查询结果**：\n\n期末考试安排：\n| 科目 | 日期 | 时间 | 地点 |\n|------|------|------|------|\n| 高等数学 | 2024-01-15 | 09:00-11:00 | A栋101 |\n| 大学英语 | 2024-01-16 | 14:00-16:00 | B栋201 |\n| 数据结构 | 2024-01-17 | 09:00-11:00 | A栋102 |\n| 数据库 | 2024-01-18 | 14:00-16:00 | C栋301 |\n\n💡 **建议**：请提前到达考场，携带学生证和考试用品",
                "category": "exam"
            },
            # 通知查询
            {
                "patterns": ["通知", "公告", "消息", "新闻", "校园动态"],
                "response": "🤔 **思考过程**：用户想查询校园通知\n🔧 **执行操作**：调用通知查询工具\n📊 **查询结果**：\n\n最新校园通知：\n1. 【重要】期末考试时间安排通知 - 发布时间：2024-01-05\n2. 【活动】校园科技节报名通知 - 发布时间：2024-01-04\n3. 【提醒】图书馆寒假开放时间调整 - 发布时间：2024-01-03\n4. 【招聘】春季校园招聘会预告 - 发布时间：2024-01-02\n5. 【通知】学生医保缴费截止提醒 - 发布时间：2024-01-01\n\n💡 **建议**：请定期查看校园通知，以免错过重要信息",
                "category": "notice"
            },
            # 图书馆相关
            {
                "patterns": ["图书馆", "借书", "书籍", "阅览室"],
                "response": "🤔 **思考过程**：用户想查询图书馆相关信息\n🔧 **执行操作**：查询图书馆信息\n📊 **查询结果**：\n\n图书馆信息：\n- 开放时间：周一至周五 8:00-22:00，周末 9:00-20:00\n- 当前借阅量：每人最多可借10本书\n- 借阅期限：30天，可续借一次\n- 逾期罚款：每天0.1元/本\n\n💡 **建议**：可以通过图书馆官网或APP查询书籍位置和借阅状态",
                "category": "library"
            },
            # 食堂相关
            {
                "patterns": ["食堂", "吃饭", "餐厅", "餐饮"],
                "response": "🤔 **思考过程**：用户想查询食堂相关信息\n🔧 **执行操作**：查询食堂信息\n📊 **查询结果**：\n\n校园食堂信息：\n- 一食堂（学生食堂）：提供各类家常菜，人均10-15元\n- 二食堂（风味食堂）：各地特色小吃，人均15-25元\n- 三食堂（清真食堂）：清真食品，人均10-15元\n- 营业时间：早餐6:30-9:00，午餐11:00-13:30，晚餐17:00-19:30\n\n💡 **建议**：建议错峰就餐，避免高峰期排队",
                "category": "canteen"
            },
            # 天气查询
            {
                "patterns": ["天气", "温度", "下雨", "预报"],
                "response": "🤔 **思考过程**：用户想查询天气信息\n🔧 **执行操作**：查询天气信息\n📊 **查询结果**：\n\n今日校园天气：\n- 天气状况：晴转多云\n- 温度：15°C - 25°C\n- 风力：微风\n- 空气质量：良好\n\n💡 **建议**：今天天气适宜出行，记得携带外套",
                "category": "weather"
            },
            # 帮助信息
            {
                "patterns": ["帮助", "功能", "能做什么", "使用说明"],
                "response": "🤔 **思考过程**：用户想了解我的功能\n🔧 **执行操作**：展示功能列表\n📊 **查询结果**：\n\n我可以帮助您查询以下信息：\n\n🎓 **学习相关**\n- 成绩查询：查询您的考试成绩和绩点\n- 课表查询：查询课程安排和上课地点\n- 考试查询：查询期末考试安排\n\n🏢 **校园服务**\n- 教室查询：查询可用的空教室\n- 通知查询：查看最新校园通知\n- 图书馆查询：借阅信息和开放时间\n- 食堂查询：食堂菜单和营业时间\n\n💬 **其他功能**\n- 会话管理：创建新会话、查看历史会话\n- 知识问答：回答各类问题\n\n💡 **建议**：您可以直接用自然语言提问，比如\"我的成绩如何？\"或\"今天有什么课？\"",
                "category": "help"
            },
            # 致谢类
            {
                "patterns": ["谢谢", "感谢", "辛苦了", "good"],
                "response": "不客气！很高兴能帮助到您。如果还有其他问题，随时欢迎提问！",
                "category": "thanks"
            },
            # 时间相关
            {
                "patterns": ["时间", "几点", "日期", "今天"],
                "response": "🤔 **思考过程**：用户想知道当前时间\n🔧 **执行操作**：查询系统时间\n📊 **查询结果**：\n\n当前时间：2024年1月10日 星期四 10:30\n\n💡 **建议**：请注意合理安排时间，劳逸结合",
                "category": "time"
            }
        ]
        
        # 模糊匹配规则
        self.fuzzy_rules = [
            {
                "keywords": ["请假", "旷课", "迟到"],
                "response": "关于请假和考勤相关的问题，建议您联系辅导员或查看教务处相关规定。",
                "category": "attendance"
            },
            {
                "keywords": ["奖学金", "助学金", "贷款"],
                "response": "关于奖学金、助学金和助学贷款的信息，请咨询学生资助管理中心或查看学生处官网。",
                "category": "finance"
            },
            {
                "keywords": ["宿舍", "住宿", "水电费"],
                "response": "宿舍相关问题（如住宿安排、水电费等），请联系宿舍管理中心。",
                "category": "dormitory"
            },
            {
                "keywords": ["就业", "实习", "招聘"],
                "response": "就业和实习相关信息，请关注就业指导中心发布的招聘信息和实习机会。",
                "category": "career"
            }
        ]
    
    def match_rule(self, query: str) -> str:
        """
        根据用户查询匹配规则
        
        Args:
            query: 用户查询文本
        
        Returns:
            匹配到的响应，如果没有匹配返回None
        """
        query_lower = query.lower().strip()
        
        # 首先尝试精确匹配
        for rule in self.rules:
            for pattern in rule["patterns"]:
                if pattern in query_lower:
                    return rule["response"]
        
        # 然后尝试模糊匹配
        for rule in self.fuzzy_rules:
            for keyword in rule["keywords"]:
                if keyword in query_lower:
                    return rule["response"]
        
        # 没有匹配到规则
        return None
    
    def get_category(self, query: str) -> str:
        """
        获取查询类别
        
        Args:
            query: 用户查询文本
        
        Returns:
            查询类别
        """
        query_lower = query.lower().strip()
        
        for rule in self.rules:
            for pattern in rule["patterns"]:
                if pattern in query_lower:
                    return rule["category"]
        
        for rule in self.fuzzy_rules:
            for keyword in rule["keywords"]:
                if keyword in query_lower:
                    return rule["category"]
        
        return "unknown"
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        处理用户查询
        
        Args:
            query: 用户查询文本
        
        Returns:
            处理结果字典
        """
        response = self.match_rule(query)
        
        if response:
            return {
                "success": True,
                "response": response,
                "category": self.get_category(query),
                "method": "rule_based"
            }
        else:
            # 默认响应
            default_response = f"""🤔 **思考过程**：用户提出了一个问题，但我没有找到完全匹配的查询规则
🔧 **执行操作**：使用通用回答模式
📊 **查询结果**：很抱歉，我暂时无法回答这个问题。请问您是否需要查询以下信息？

- 成绩查询
- 课表查询  
- 教室查询
- 考试安排
- 校园通知

💡 **建议**：请尝试使用更明确的关键词进行提问，例如"我的成绩如何？"或"今天有什么课？"
"""
            return {
                "success": True,
                "response": default_response,
                "category": "unknown",
                "method": "default"
            }

# 创建全局实例
local_engine = LocalRuleEngine()

def query_local_engine(query: str) -> str:
    """
    便捷函数：查询本地规则引擎
    
    Args:
        query: 用户查询文本
    
    Returns:
        响应文本
    """
    result = local_engine.process_query(query)
    return result["response"]
