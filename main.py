# main.py
from ui.gradio_ui import create_ui

demo = create_ui()

if __name__ == "__main__":
    print("✅ 校园智能查询助手启动成功")
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True
    )