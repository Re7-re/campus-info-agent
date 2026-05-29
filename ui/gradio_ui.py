# ui/gradio_ui.py
import gradio as gr


# 对话函数（智能体 + 手动双支持）
def chat_response(message, history):
    try:
        from langchain_core.messages import HumanMessage
        from agent.agent_core import agent

        messages = [HumanMessage(content=message)]
        result = agent.invoke({"messages": messages})
        return result["messages"][-1].content
    except Exception as e:
        return f"[智能体暂时离线] 你输入的内容是：{message}\n错误信息：{str(e)}"


# 界面
def create_ui():
    with gr.Blocks(title="校园信息智能查询智能体") as demo:
        gr.Markdown("""
        # 🏫 校园信息智能查询智能体
        **支持：成绩查询 | 课表查询 | 空教室 | 考试安排 | 校园通知**
        """)

        chatbot = gr.Chatbot(height=550)
        msg = gr.Textbox(placeholder="请输入你的问题...")
        clear = gr.ClearButton([msg, chatbot])

        def respond(user_input, chat_history):
            bot_response = chat_response(user_input, chat_history)
            chat_history.append((user_input, bot_response))
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
    return demo