"""
Gradio UI模块 - 集成版本
提供登录注册和主系统的完整集成
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
from data.user_data import UserData
from utils.logger import setup_logger


class IntegratedCampusUI:
    """
    集成校园信息查询系统UI类
    支持登录注册和主系统的无缝切换
    """
    
    def __init__(self):
        """初始化UI"""
        # 设置日志
        self.logger = setup_logger("integrated_campus_ui")
        
        # 初始化用户数据管理
        self.user_data = UserData()
        
        # 当前登录用户
        self.current_user = None
        
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
        
        self.logger.info("集成校园信息UI初始化完成")
    
    def create_integrated_ui(self) -> gr.Blocks:
        """
        创建集成UI界面
        
        Returns:
            Gradio Blocks对象
        """
        with gr.Blocks(
            title="校园信息智能查询系统",
            css="""
            /* 全局样式 */
            :root {
                --primary-color: #1e40af;
                --primary-light: #3b82f6;
                --primary-dark: #1e3a8a;
                --secondary-color: #0ea5e9;
                --accent-color: #06b6d4;
                --bg-color: #f0f9ff;
                --sidebar-bg: #e0f2fe;
                --card-bg: #ffffff;
                --text-color: #1e293b;
                --text-secondary: #64748b;
                --border-color: #bfdbfe;
                --success-color: #059669;
                --warning-color: #d97706;
            }
            
            body {
                font-size: 16px !important;
                color: var(--text-color);
                background-color: var(--bg-color);
            }
            
            .container {
                max-width: 1400px !important;
                margin: 0 auto !important;
            }
            
            .login-box {
                max-width: 450px !important;
                margin: 50px auto !important;
                padding: 30px !important;
                background: var(--card-bg);
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(30, 64, 175, 0.1);
            }
            
            /* 侧边栏样式 */
            .sidebar-container {
                background-color: var(--sidebar-bg);
                border-radius: 8px;
                padding: 15px;
                min-width: 200px;
                max-width: 350px;
            }
            
            .main-content {
                background-color: var(--card-bg);
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(30, 64, 175, 0.05);
            }
            
            /* 可拖动分隔线 */
            .resizer {
                width: 8px;
                cursor: col-resize;
                background-color: var(--border-color);
                border-radius: 4px;
                margin: 0 4px;
                transition: background-color 0.2s;
            }
            
            .resizer:hover {
                background-color: var(--primary-color);
            }
            
            /* 按钮样式 */
            button {
                font-size: 15px !important;
                border-radius: 8px !important;
                transition: all 0.2s ease;
            }
            
            button:hover {
                transform: translateY(-1px);
                box-shadow: 0 2px 8px rgba(30, 64, 175, 0.2);
            }
            
            /* 输入框样式 */
            input, textarea {
                font-size: 15px !important;
                border-radius: 8px !important;
                border: 1px solid var(--border-color) !important;
            }
            
            input:focus, textarea:focus {
                border-color: var(--primary-color) !important;
                box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1) !important;
            }
            
            /* 标签页样式 */
            .gr-tab {
                font-size: 15px !important;
                color: var(--text-secondary);
            }
            
            .gr-tab.selected {
                color: var(--primary-color);
                font-weight: 600;
                border-bottom-color: var(--primary-color) !important;
            }
            
            /* 聊天框样式 */
            .gr-chatbot {
                font-size: 15px !important;
                border-radius: 8px !important;
                border: 1px solid var(--border-color);
            }
            
            /* 下拉框样式 */
            .gr-dropdown {
                font-size: 15px !important;
                border-radius: 8px !important;
            }
            
            /* 滑块样式 */
            .gr-slider {
                font-size: 14px !important;
            }
            
            /* Markdown 样式 */
            .gr-markdown {
                font-size: 15px !important;
            }
            
            .gr-markdown h1 {
                font-size: 28px !important;
                color: var(--primary-dark);
                font-weight: 700;
            }
            
            .gr-markdown h2 {
                font-size: 22px !important;
                color: var(--primary-color);
                font-weight: 600;
            }
            
            .gr-markdown h3 {
                font-size: 18px !important;
                color: var(--primary-color);
                font-weight: 600;
            }
            
            /* 折叠面板样式 */
            .gr-accordion {
                border: 1px solid var(--border-color) !important;
                border-radius: 8px !important;
            }
            
            .gr-accordion .gr-accordion-header {
                background-color: var(--sidebar-bg) !important;
                font-size: 15px !important;
                color: var(--primary-dark);
                font-weight: 600;
            }
            
            /* 按钮变体样式 */
            button.primary {
                background: linear-gradient(135deg, var(--primary-color), var(--primary-light)) !important;
                border: none !important;
                color: white !important;
            }
            
            button.secondary {
                background-color: var(--sidebar-bg) !important;
                border: 1px solid var(--border-color) !important;
                color: var(--primary-dark) !important;
            }
            
            button.stop {
                background-color: #dc2626 !important;
                border: none !important;
                color: white !important;
            }
            
            /* 文本框样式 */
            .gr-textbox {
                font-size: 15px !important;
            }
            
            /* 复选框样式 */
            .gr-checkbox {
                font-size: 15px !important;
            }
            
            /* 表格样式 */
            table {
                font-size: 14px !important;
            }
            """
        ) as demo:
            
            # 登录页面
            with gr.Column(visible=True, elem_classes="login-box") as login_page:
                gr.Markdown("""
                # 🏫 校园信息智能查询系统
                
                ### 欢迎使用多功能校园服务平台
                """)
                
                with gr.Tabs() as auth_tabs:
                    # 登录标签
                    with gr.TabItem("登录"):
                        gr.Markdown("### 用户登录")
                        gr.Markdown("请输入您的账号和密码登录系统")
                        
                        username = gr.Textbox(
                            label="用户名",
                            placeholder="请输入用户名",
                            max_lines=1,
                            container=True
                        )
                        
                        password = gr.Textbox(
                            label="密码",
                            placeholder="请输入密码",
                            type="password",
                            max_lines=1,
                            container=True
                        )
                        
                        login_message = gr.Markdown(label="提示信息")
                        
                        with gr.Row():
                            login_btn = gr.Button("登录", variant="primary", size="lg", scale=2)
                            register_tab_btn = gr.Button("去注册", variant="secondary", scale=1)
                        
                        # 测试账号提示
                        with gr.Accordion("测试账号", open=False):
                            gr.Markdown("""
                            **管理员账号：**
                            - 用户名：admin
                            - 密码：admin123
                            
                            **学生账号：**
                            - 用户名：student
                            - 密码：student123
                            """)
                    
                    # 注册标签
                    with gr.TabItem("注册"):
                        gr.Markdown("### 用户注册")
                        gr.Markdown("创建新账号以使用系统功能")
                        
                        reg_username = gr.Textbox(
                            label="用户名",
                            placeholder="3-20位字母数字",
                            max_lines=1,
                            container=True
                        )
                        
                        reg_password = gr.Textbox(
                            label="密码",
                            placeholder="至少6位，包含字母和数字",
                            type="password",
                            max_lines=1,
                            container=True
                        )
                        
                        reg_confirm_password = gr.Textbox(
                            label="确认密码",
                            placeholder="再次输入密码",
                            type="password",
                            max_lines=1,
                            container=True
                        )
                        
                        reg_email = gr.Textbox(
                            label="邮箱",
                            placeholder="请输入邮箱地址",
                            max_lines=1,
                            container=True
                        )
                        
                        reg_phone = gr.Textbox(
                            label="手机号",
                            placeholder="请输入手机号码",
                            max_lines=1,
                            container=True
                        )
                        
                        reg_nickname = gr.Textbox(
                            label="昵称（可选）",
                            placeholder="您的昵称",
                            max_lines=1,
                            container=True
                        )
                        
                        reg_message = gr.Markdown(label="提示信息")
                        
                        with gr.Row():
                            register_btn = gr.Button("注册", variant="primary", size="lg", scale=2)
                            login_tab_btn = gr.Button("去登录", variant="secondary", scale=1)
            
            # 主系统页面
            with gr.Column(visible=False) as main_page:
                # 顶部导航栏
                with gr.Row():
                    gr.Markdown(f"### 校园信息智能查询系统")
                    user_info = gr.Markdown(f"当前用户：{self.current_user['nickname'] if self.current_user else '未登录'}")
                    logout_btn = gr.Button("退出登录", variant="stop", size="sm")
                
                gr.Markdown("---")
                
                with gr.Row(equal_height=True):
                    # 左侧边栏
                    with gr.Column(scale=1, min_width=220, elem_classes="sidebar-container"):
                        gr.Markdown("### 功能导航")
                        
                        # 功能按钮
                        feature_buttons = {}
                        for feature_name in self.features.keys():
                            btn = gr.Button(
                                f"{feature_name}",
                                variant="secondary" if feature_name != "智能助手" else "primary",
                                size="lg"
                            )
                            feature_buttons[feature_name] = btn
                        
                        gr.Markdown("---")
                        
                        # 会话管理
                        with gr.Accordion("会话管理", open=True):
                            new_session_btn = gr.Button("新会话", variant="primary", size="sm")
                            history_btn = gr.Button("历史会话", variant="secondary", size="sm")
                            save_session_btn = gr.Button("保存会话", variant="secondary", size="sm")
                            session_stats = gr.Textbox(
                                label="会话统计",
                                interactive=False,
                                lines=3,
                                value="点击按钮查看会话信息"
                            )
                        
                        # 会话列表
                        with gr.Accordion("历史会话列表", open=False):
                            session_list_display = gr.Textbox(
                                label="会话列表",
                                interactive=False,
                                lines=8,
                                value="暂无历史会话"
                            )
                            session_id_input = gr.Textbox(
                                label="会话ID",
                                placeholder="输入会话ID进行操作",
                                max_lines=1
                            )
                            with gr.Row():
                                switch_session_btn = gr.Button("切换会话", size="sm")
                                delete_session_btn = gr.Button("删除会话", variant="stop", size="sm")
                        
                        gr.Markdown("---")
                        
                        # 系统信息
                        with gr.Accordion("系统信息", open=False):
                            gr.Markdown("""
                            **功能模块：**
                            - AI智能助手
                            - 成绩查询  
                            - 课表查询
                            - 教室查询
                            - 考试查询
                            - 通知查询
                            
                            **特色功能：**
                            - 对话记忆
                            - 知识库支持
                            - 自然语言交互
                            - 会话管理
                            """)
                    
                    # 可拖动分隔线
                    gr.HTML("""
                    <div class="resizer" style="width: 8px; cursor: col-resize; background-color: #bfdbfe; 
                        border-radius: 4px; margin: 0 4px; transition: background-color 0.2s; height: 100%;">
                    </div>
                    """)
                    
                    # 右侧内容区
                    with gr.Column(scale=4, min_width=600, elem_classes="main-content"):
                        # 功能内容区
                        with gr.Tabs() as tabs:
                            for feature_name in self.features.keys():
                                with gr.TabItem(feature_name):
                                    self.create_feature_ui(feature_name)
            
            # 登录处理函数
            def do_login(username_val, password_val):
                result = self.user_data.login(username_val, password_val)
                if result["success"]:
                    self.current_user = result["user"]
                    self.logger.info(f"用户登录成功: {username_val}")
                    return (
                        gr.Markdown(f"✅ {result['message']}"),
                        gr.update(visible=False),  # 隐藏登录页面
                        gr.update(visible=True),   # 显示主页面
                        gr.Markdown(f"当前用户：{result['user']['nickname']}"),
                        gr.update(selected=0)  # 切换到智能助手标签
                    )
                else:
                    return (
                        gr.Markdown(f"❌ {result['message']}"),
                        gr.update(visible=True),  # 保持登录页面显示
                        gr.update(visible=False),  # 不显示主页面
                        gr.Markdown("当前用户：未登录"),
                        gr.update(selected=0)
                    )
            
            # 注册处理函数
            def do_register(uname, pwd, cpwd, email, phone, nickname):
                result = self.user_data.register(
                    username=uname,
                    password=pwd,
                    confirm_password=cpwd,
                    email=email,
                    phone=phone,
                    nickname=nickname
                )
                if result["success"]:
                    self.logger.info(f"用户注册成功: {uname}")
                    return gr.Markdown(f"✅ {result['message']}<br>请切换到登录页面进行登录")
                else:
                    return gr.Markdown(f"❌ {result['message']}")
            
            # 退出登录处理函数
            def do_logout():
                self.current_user = None
                self.logger.info("用户退出登录")
                return (
                    gr.update(visible=True),   # 显示登录页面
                    gr.update(visible=False),  # 隐藏主页面
                    gr.Markdown("当前用户：未登录"),
                    gr.Markdown("### 用户登录\n请输入您的账号和密码登录系统")
                )
            
            # 切换标签页
            def switch_to_register():
                return gr.Tabs(selected=1)
            
            def switch_to_login():
                return gr.Tabs(selected=0)
            
            # 切换功能模块
            def switch_feature(feature_name):
                """切换功能标签页"""
                feature_names = list(self.features.keys())
                return gr.Tabs(selected=feature_names.index(feature_name))
            
            # 会话管理功能
            def create_new_session():
                """创建新会话"""
                agent_feature = self.features["智能助手"]
                result = agent_feature.create_new_session()
                return result["message"]
            
            def show_session_history():
                """显示会话历史"""
                agent_feature = self.features["智能助手"]
                result = agent_feature.get_session_list()
                if result["success"]:
                    sessions = result["sessions"]
                    if sessions:
                        history_text = "会话列表：\n\n"
                        for session in sessions:
                            current_mark = " [当前]" if session["is_current"] else ""
                            history_text += f"• {session['title']}{current_mark}\n"
                            history_text += f"  ID: {session['session_id']}\n"
                            history_text += f"  创建: {session['created_at']}\n"
                            history_text += f"  消息数: {session['message_count']}\n\n"
                        return history_text
                    else:
                        return "暂无历史会话"
                else:
                    return f"获取会话列表失败: {result['message']}"
            
            def save_current_session():
                """保存当前会话"""
                agent_feature = self.features["智能助手"]
                result = agent_feature.save_current_session()
                return result["message"]
            
            def show_session_stats():
                """显示会话统计"""
                agent_feature = self.features["智能助手"]
                result = agent_feature.get_session_statistics()
                if result["success"]:
                    stats = result["statistics"]
                    stats_text = f"总会话数: {stats['total_sessions']}\n"
                    stats_text += f"总消息数: {stats['total_messages']}\n"
                    stats_text += f"当前会话: {stats['current_session_id'] or '无'}\n"
                    stats_text += f"当前消息数: {stats['current_messages']}"
                    return stats_text
                else:
                    return f"获取统计信息失败: {result['message']}"
            
            def switch_to_session(session_id):
                """切换到指定会话"""
                if not session_id.strip():
                    return "请输入会话ID"
                agent_feature = self.features["智能助手"]
                result = agent_feature.switch_session(session_id)
                return result["message"]
            
            def delete_session(session_id):
                """删除指定会话"""
                if not session_id.strip():
                    return "请输入会话ID"
                agent_feature = self.features["智能助手"]
                result = agent_feature.delete_session(session_id)
                if result["success"]:
                    # 刷新会话列表
                    return result["message"] + "\n\n" + show_session_history()
                return result["message"]
            
            # 绑定事件
            login_btn.click(do_login, [username, password], [login_message, login_page, main_page, user_info, tabs])
            username.submit(do_login, [username, password], [login_message, login_page, main_page, user_info, tabs])
            password.submit(do_login, [username, password], [login_message, login_page, main_page, user_info, tabs])
            
            register_btn.click(do_register, [reg_username, reg_password, reg_confirm_password, reg_email, reg_phone, reg_nickname], [reg_message])
            
            register_tab_btn.click(switch_to_register, outputs=[auth_tabs])
            login_tab_btn.click(switch_to_login, outputs=[auth_tabs])
            
            logout_btn.click(do_logout, outputs=[login_page, main_page, user_info, login_message])
            
            # 会话管理事件绑定
            new_session_btn.click(create_new_session, outputs=[session_stats])
            history_btn.click(show_session_history, outputs=[session_list_display])
            save_session_btn.click(save_current_session, outputs=[session_stats])
            switch_session_btn.click(switch_to_session, [session_id_input], [session_stats])
            delete_session_btn.click(delete_session, [session_id_input], [session_list_display])
            
            for feature_name, btn in feature_buttons.items():
                btn.click(
                    lambda fn=feature_name: switch_feature(fn),
                    outputs=[tabs]
                )
        
        return demo
    
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
    
    def _create_agent_ui(self, feature: AgentFeature) -> gr.Column:
        """创建智能助手UI"""
        with gr.Column() as ui_block:
            gr.Markdown("### AI智能助手")
            gr.Markdown("支持自然语言查询，可以回答各种校园信息问题")
            
            chatbot = gr.Chatbot(
                height=500,
                label="对话记录"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="请输入你的问题...",
                    label="",
                    scale=4,
                    container=False
                )
                submit_btn = gr.Button("发送", scale=1, variant="primary")
            
            with gr.Row():
                use_memory = gr.Checkbox(
                    label="启用对话记忆",
                    value=True,
                    scale=1
                )
                clear_btn = gr.Button("清空对话", scale=1)
            
            # 状态显示
            with gr.Accordion("对话状态", open=False):
                memory_info = gr.Textbox(
                    label="记忆信息",
                    interactive=False,
                    lines=2
                )
            
            # 事件绑定
            def respond(message, history, memory_enabled):
                if not message.strip():
                    return "", history, "请输入消息"
                
                try:
                    result = feature.execute(message, use_memory=memory_enabled)
                    response = result.get("message", "抱歉，我遇到了一些问题。")
                    
                    # 更新对话历史（兼容新旧格式）
                    if isinstance(history, list):
                        # 新版本的 messages 格式
                        history.append({"role": "user", "content": message})
                        history.append({"role": "assistant", "content": response})
                    else:
                        # 旧版本的 tuple 格式
                        history = history or []
                        history.append((message, response))
                    
                    # 更新记忆信息
                    stats = feature.get_memory_stats()
                    memory_text = f"会话 ID: {stats['session_id']} | 消息数：{stats['total_messages']}/{stats['max_history']}"
                    
                    return "", history, memory_text
                except Exception as e:
                    error_msg = f"发生错误：{str(e)}"
                    if isinstance(history, list):
                        history.append({"role": "user", "content": message})
                        history.append({"role": "assistant", "content": error_msg})
                    else:
                        history = history or []
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
            gr.Markdown("### 成绩查询")
            gr.Markdown("查询各学期成绩信息（6个学期）")
            
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
                lines=12,
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
            gr.Markdown("### 课表查询")
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
            gr.Markdown("### 教室查询")
            gr.Markdown("查询当前可用空教室（共70间）")
            
            query_btn = gr.Button("查询空教室", variant="primary", size="lg")
            
            result_text = gr.Textbox(
                label="查询结果",
                lines=10,
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
            gr.Markdown("### 考试查询")
            gr.Markdown("查询期末考试安排（共50条）")
            
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
                lines=12,
                interactive=False
            )
            
            with gr.Row():
                upcoming_btn = gr.Button("即将到来的考试", scale=1)
                summary_btn = gr.Button("考试摘要", scale=1)
            
            extra_info = gr.Textbox(
                label="附加信息",
                lines=8,
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
            gr.Markdown("### 通知查询")
            gr.Markdown("查询最新校园通知（共100条）")
            
            with gr.Row():
                count_slider = gr.Slider(
                    minimum=1,
                    maximum=50,
                    value=10,
                    step=1,
                    label="显示通知数量",
                    scale=3
                )
                query_btn = gr.Button("查询通知", scale=1, variant="primary")
            
            result_text = gr.Textbox(
                label="查询结果",
                lines=15,
                interactive=False
            )
            
            with gr.Row():
                important_btn = gr.Button("重要通知", scale=1)
                category_btn = gr.Button("分类通知", scale=1)
            
            extra_info = gr.Textbox(
                label="附加信息",
                lines=8,
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


def create_integrated_ui() -> gr.Blocks:
    """
    创建集成UI界面的工厂函数
    
    Returns:
        Gradio Blocks对象
    """
    ui_creator = IntegratedCampusUI()
    return ui_creator.create_integrated_ui()