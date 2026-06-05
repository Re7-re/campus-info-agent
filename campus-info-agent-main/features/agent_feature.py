from .base_feature import BaseFeature
from zhipuai import ZhipuAI
from config import Config
from utils.memory import ConversationMemory
from typing import Dict, Any

class AgentFeature(BaseFeature):
    def __init__(self):
        super().__init__(
            name="AI智能助手",
            description="自然语言多轮对话，自动路由工具查询校园信息"
        )
        self.client = ZhipuAI(api_key=Config.ZHIPU_API_KEY)
        # 修正参数名max_history
        self.memory = ConversationMemory(max_history=Config.MAX_MEMORY_SIZE, save_dir=Config.MEMORY_DIR)

    def execute(self, user_msg: str, use_memory: bool = True) -> Dict[str, Any]:
        if use_memory:
            history = self.memory.get_context_summary()
            prompt = f"历史对话:{history}\n用户提问:{user_msg}"
        else:
            prompt = user_msg

        resp = self.client.chat.completions.create(
            model=Config.MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        ans = resp.choices[0].message.content
        if use_memory:
            self.memory.add_message("user", user_msg)
            self.memory.add_message("assistant", ans)
        return {"message": ans}

    def clear_memory(self):
        self.memory.clear_history()

    def get_memory_stats(self) -> Dict[str, Any]:
        return {
            "session_id": self.memory.session_id,
            "total_messages": len(self.memory.conversation_history),
            "max_history": self.memory.max_history
        }

    def get_ui_components(self):
        return {}