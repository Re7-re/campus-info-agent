# agent/agent_core.py
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

from config import Config
from agent.tools import TOOLS


def get_llm(service: str| None = None) -> ChatOpenAI:
    """
    根据配置获取 LLM是 模型实例。

    Args:
        service: AI服务名称，可选值: zhipu, siliconflow, deepseek, longchat, alibaba。
                 若为 None，则使用 Config.DEFAULT_AI_SERVICE。

    Returns:
        ChatOpenAI 实例。

    Raises:
        ValueError: 不支持的 service 名称。
    """
    if service is None:
        service = Config.DEFAULT_AI_SERVICE

    service_config = {
        "zhipu": (Config.ZHIPU_API_KEY, Config.ZHIPU_MODEL_NAME, Config.ZHIPU_API_BASE),
        "siliconflow": (Config.SILICONFLOW_API_KEY, Config.SILICONFLOW_MODEL_NAME, Config.SILICONFLOW_API_BASE),
        "deepseek": (Config.DEEPSEEK_API_KEY, Config.DEEPSEEK_MODEL_NAME, Config.DEEPSEEK_API_BASE),
        "longchat": (Config.LONGCHAT_API_KEY, Config.LONGCHAT_MODEL_NAME, Config.LONGCHAT_API_BASE),
        "alibaba": (Config.ALIBABA_API_KEY, Config.ALIBABA_MODEL_NAME, Config.ALIBABA_API_BASE),
    }

    if service not in service_config:
        raise ValueError(f"不支持的 AI 服务：{service}")

    api_key, model_name, base_url = service_config[service]
    return ChatOpenAI(api_key=api_key, model=model_name, base_url=base_url)


# 获取默认 LLM
llm = get_llm()

# 绑定工具
llm_with_tools = llm.bind_tools(TOOLS)


# 节点函数
def agent_node(state: MessagesState) -> dict:
    """智能体节点：调用 LLM 处理消息并返回响应。"""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# 工具节点
tool_node = ToolNode(TOOLS)


def should_continue(state: MessagesState) -> str:
    """判断是否继续调用工具。若最后一条消息有 tool_calls 则返回 'tools'，否则结束。"""
    last_message = state["messages"][-1]
    return "tools" if last_message.tool_calls else "__end__"


# 构建工作流
workflow = StateGraph(MessagesState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")
workflow.set_entry_point("agent")

# 编译智能体
agent = workflow.compile()