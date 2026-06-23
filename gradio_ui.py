"""
Gradio UI模块
提供带有侧边栏的多功能界面
"""

import gradio as gr
from typing import Dict, Any, Optional, Callable
from features import (
    GradeFeature,
    ScheduleFeature,
    ClassroomFeature,
    ExamFeature,
    NoticeFeature,
    AgentFeature
)
from utils.logger import setup_logger


class CampusInfoUI:
    """
    校园信息查询系统UI类
    支持多功能模块切换和智能对话
    """
    
    def __init__(self):
        """初始化UI"""
        # 设置日志
        self.logger = setup_logger("campus_ui")
        
        # 初始化功能模块
        self.features = {
            "智能助手": AgentFeature(),
            "成绩查询": GradeFeature(),
            "课表查询": ScheduleFeature(),
            "教室查询": ClassroomFeature(),
            "考试查询": ExamFeature(),
            "通知查询": NoticeFeature()
        }
        
        # 当前选中的功能
        self.current_feature = "智能助手"
        
        self.logger.info("校园信息UI初始化完成")
    
    def create_feature_ui(self, feature_name: str) -> gr.Blocks:
        """
        创建特定功能的UI
        
        Args:
            feature_name: 功能名称
        
        Returns:
            Gradio界面组件
        """
        feature = self.features[feature_name]
        
        if feature_name == "智能助手":
            return self._create_agent_ui(feature)
        elif feature_name == "成绩查询":
            return self._create_grade_ui(feature)
        elif feature_name == "课表查询":
            return self._create_schedule_ui(feature)
        elif feature_name == "教室查询":
            return self._create_classroom_ui(feature)
        elif feature_name == "考试查询":
            return self._create_exam_ui(feature)
        elif feature_name == "通知查询":
            return self._create_notice_ui(feature)
        else:
            return gr.Markdown("功能开发中...")
    
    def _create_agent_ui (self, feature: AgentFeature) -> gr.Column:
        """创建智能助手UI"""
        with gr.Column () as ui_block:
            gr.Markdown ("### 🤖 AI智能助手")
            gr.Markdown ("支持自然语言查询，可以回答各种校园信息问题")
            
            chatbot = gr.Chatbot(
                height=500,
                label="对话记录"
            )
            
            with gr.Row ():
                msg =  gr.Textbox(
                    placeholder= "请输入你的问题...",
                    label ="",
                    scale =4,
                    container =False
                )
                submit_btn  = gr.Button("发送", scale=1, variant="primary")
            
            with gr.Row():
                use_memory =gr.Checkbox(
                    label= "启用对话记忆",
                    value= True,
                    scale= 1
                )
                clear_btn =gr.Button("清空对话", scale=1)
            
            # 状态显示
            with gr.Accordion ("对话状态", open=False):
                memory_info =gr.Textbox(
                    label= "记忆信息",
                    interactive= False,
                    lines= 2
                )
            
            # 事件绑定
            def respond (message, history, memory_enabled):
                if not message.strip ():
                    return "", history
                
                try:
                    result = feature.execute(message, use_memory=memory_enabled)
                    response = result.get("message", "抱歉，我遇到了一些问题。")
                    
                    # 更新对话历史
                    history.append((message, response))
                    
                    # 更新记忆信息
                    stats = feature.get_memory_stats()
                    memory_text = f"会话ID: {stats['session_id']} | 消息数: {stats['total_messages']}/{stats['max_history']}"
                    
                    return "", history, memory_text
                except Exception as e:
                    error_msg = f"发生错误: {str(e)}"
                    history.append((message, error_msg))
                    return "", history, "错误状态"
            
            def clear_chat():
                feature.clear_memory()
                return [], "对话已清空"
            
            # 绑定事件
            msg.submit(respond, [msg, chatbot, use_memory], [msg, chatbot, memory_info])
            submit_btn.click(respond, [msg, chatbot, use_memory], [msg, chatbot, memory_info])
            clear_btn.click(clear_chat, outputs=[chatbot, memory_info])
        
        return ui_block
    
    def _create_grade_ui(self, feature: GradeFeature) -> gr.Column:
        """创建成绩查询UI"""
        with gr.Column() as ui_block:
            gr.Markdown("### 📊 成绩查询")
            gr.Markdown("查询各学期成绩信息")
            
            with gr.Row():
                term_dropdown = gr.Dropdown(
                    choices=["全部"] + feature.get_available_terms(),
                    value="全部",
                    label="选择学期",
                    scale=3
                )
                query_btn = gr.Button("查询成绩", scale=1, variant="primary")
            
            result_text = gr.Textbox(
                label="查询结果",
                lines=10,
                interactive=False
            )
            
            with gr.Row():
                gpa_btn = gr.Button("计算GPA", scale=1)
                gpa_result = gr.Textbox(
                    label="GPA信息",
                    scale=2,
                    interactive=False
                )
            
            def query_grade(term):
                result = feature.execute(term=term if term != "全部" else None)
                return result.get("message", "查询失败")
            
            def calculate_gpa():
                result = feature.get_gpa()
                return result.get("message", "计算失败")
            
            query_btn.click(query_grade, [term_dropdown], [result_text])
            gpa_btn.click(calculate_gpa, outputs=[gpa_result])
        
        return ui_block
    
    def _create_schedule_ui(self, feature: ScheduleFeature) -> gr.Column:
        """创建课表查询UI"""
        with gr.Column() as ui_block:
            gr.Markdown("### 📅 课表查询")
            gr.Markdown("查询周课表信息")
            
            with gr.Row():
                day_dropdown = gr.Dropdown(
                    choices=["全部"] + feature.get_available_days(),
                    value="全部",
                    label="选择星期",
                    scale=3
                )
                query_btn = gr.Button("查询课表", scale=1, variant="primary")
            
            result_text = gr.Textbox(
                label="查询结果",
                lines=10,
                interactive=False
            )
            
            with gr.Row():
                today_btn = gr.Button("今日课表", scale=1)
                week_btn = gr.Button("本周课表", scale=1)
            
            def query_schedule(day):
                result = feature.execute(day=day if day != "全部" else None)
                return result.get("message", "查询失败")
            
            def get_today_schedule():
                result = feature.get_today_schedule()
                return result.get("message", "查询失败")
            
            def get_week_schedule():
                result = feature.get_week_schedule()
                return result.get("message", "查询失败")
            
            query_btn.click(query_schedule, [day_dropdown], [result_text])
            today_btn.click(get_today_schedule, outputs=[result_text])
            week_btn.click(get_week_schedule, outputs=[result_text])
        
        return ui_block
    
    def _create_classroom_ui(self, feature: ClassroomFeature) -> gr.Column:
        """创建教室查询UI"""
        with gr.Column() as ui_block:
            gr.Markdown("### 🏫 教室查询")
            gr.Markdown("查询当前可用空教室")
            
            query_btn = gr.Button("查询空教室", variant="primary", size="lg")
            
            result_text = gr.Textbox(
                label="查询结果",
                lines=5,
                interactive=False
            )
            
            with gr.Row():
                search_input = gr.Textbox(
                    placeholder="搜索教室...",
                    label="搜索教室",
                    scale=3
                )
                search_btn = gr.Button("搜索", scale=1)
            
            search_result = gr.Textbox(
                label="搜索结果",
                lines=3,
                interactive=False
            )
            
            def query_classroom():
                result = feature.execute()
                return result.get("message", "查询失败")
            
            def search_classroom(keyword):
                results = feature.search_classroom(keyword)
                if results:
                    return "搜索结果：" + "、".join(results)
                return "未找到匹配的教室"
            
            query_btn.click(query_classroom, outputs=[result_text])
            search_btn.click(search_classroom, [search_input], [search_result])
        
        return ui_block
    
    def _create_exam_ui(self, feature: ExamFeature) -> gr.Column:
        """创建考试查询UI"""
        with gr.Column() as ui_block:
            gr.Markdown("### 📝 考试查询")
            gr.Markdown("查询期末考试安排")
            
            subjects = [e["name"] for e in feature.exam_data]
            
            with gr.Row():
                subject_dropdown = gr.Dropdown(
                    choices=["全部"] + subjects,
                    value="全部",
                    label="选择科目",
                    scale=3
                )
                query_btn = gr.Button("查询考试", scale=1, variant="primary")
            
            result_text = gr.Textbox(
                label="查询结果",
                lines=8,
                interactive=False
            )
            
            with gr.Row():
                upcoming_btn = gr.Button("即将到来的考试", scale=1)
                summary_btn = gr.Button("考试摘要", scale=1)
            
            extra_info = gr.Textbox(
                label="附加信息",
                lines=4,
                interactive=False
            )
            
            def query_exam(subject):
                result = feature.execute(subject=subject if subject != "全部" else None)
                return result.get("message", "查询失败")
            
            def get_upcoming():
                upcoming = feature.get_upcoming_exams()
                if upcoming:
                    info = "即将到来的考试：\n"
                    for exam in upcoming:
                        info += f"{exam['name']} - {exam['days_until']}天后\n"
                    return info
                return "没有即将到来的考试"
            
            def get_summary():
                result = feature.get_exam_summary()
                return result.get("message", "获取摘要失败")
            
            query_btn.click(query_exam, [subject_dropdown], [result_text])
            upcoming_btn.click(get_upcoming, outputs=[extra_info])
            summary_btn.click(get_summary, outputs=[extra_info])
        
        return ui_block
    
    def _create_notice_ui(self, feature: NoticeFeature) -> gr.Column:
        """创建通知查询UI"""
        with gr.Column() as ui_block:
            gr.Markdown("### 📢 通知查询")
            gr.Markdown("查询最新校园通知")
            
            with gr.Row():
                count_slider = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=5,
                    step=1,
                    label="显示通知数量",
                    scale=3
                )
                query_btn = gr.Button("查询通知", scale=1, variant="primary")
            
            result_text = gr.Textbox(
                label="查询结果",
                lines=8,
                interactive=False
            )
            
            with gr.Row():
                important_btn = gr.Button("重要通知", scale=1)
                category_btn = gr.Button("分类通知", scale=1)
            
            extra_info = gr.Textbox(
                label="附加信息",
                lines=6,
                interactive=False
            )
            
            def query_notice(count):
                result = feature.execute(count=int(count))
                return result.get("message", "查询失败")
            
            def get_important():
                important = feature.get_important_notices()
                if important:
                    return "重要通知：\n" + "\n".join([f"{i+1}. {n}" for i, n in enumerate(important)])
                return "没有重要通知"
            
            def get_categories():
                categories = feature.get_notice_categories()
                info = "通知分类：\n"
                for category, notices in categories.items():
                    if notices:
                        info += f"【{category}】{len(notices)}条\n"
                return info
            
            query_btn.click(query_notice, [count_slider], [result_text])
            important_btn.click(get_important, outputs=[extra_info])
            category_btn.click(get_categories, outputs=[extra_info])
        
        return ui_block
    
    def create_ui(self) -> gr.Blocks:
        """
        创建完整的UI界面
        
        Returns:
            Gradio Blocks对象
        """
        with gr.Blocks(
            title="校园信息智能查询系统"
        ) as demo:
            
            with gr.Row():
                # 左侧边栏
                with gr.Column(scale=1):
                    gr.Markdown("""
                    # 🏫 校园信息查询系统
                    
                    **多功能智能服务平台**
                    """)
                    
                    gr.Markdown("---")
                    
                    # 功能按钮
                    feature_buttons = {}
                    for feature_name in self.features.keys():
                        btn = gr.Button(
                            f"📌 {feature_name}",
                            variant="secondary" if feature_name != "智能助手" else "primary",
                            size="lg"
                        )
                        feature_buttons[feature_name] = btn
                    
                    gr.Markdown("---")
                    
                    # 系统信息
                    with gr.Accordion("系统信息", open=False):
                        gr.Markdown("""
                        **功能模块：**
                        - 🤖 AI智能助手
                        - 📊 成绩查询  
                        - 📅 课表查询
                        - 🏫 教室查询
                        - 📝 考试查询
                        - 📢 通知查询
                        
                        **特色功能：**
                        - 对话记忆
                        - 知识库支持
                        - 自然语言交互
                        """)
                
                # 右侧内容区
                with gr.Column(scale=4):
                    # 标题栏
                    gr.Markdown("""
                    # 🎯 智能校园服务平台
                    
                    选择左侧功能模块开始使用
                    """)
                    
                    # 功能内容区
                    with gr.Tabs() as tabs:
                        for feature_name in self.features.keys():
                            with gr.TabItem(feature_name):
                                self.create_feature_ui(feature_name)
            
            # 绑定侧边栏按钮事件
            def switch_feature(feature_name):
                """切换功能标签页"""
                # 找到对应的标签页索引
                feature_names = list(self.features.keys())
                return gr.Tabs(selected=feature_names.index(feature_name))
            
            for feature_name, btn in feature_buttons.items():
                btn.click(
                    lambda fn=feature_name: switch_feature(fn),
                    outputs=[tabs]
                )
        
        return demo


def create_ui() -> gr.Blocks:
    """
    创建UI界面的工厂函数
    
    Returns:
        Gradio Blocks对象
    """
    ui_creator = CampusInfoUI()
    return ui_creator.create_ui()