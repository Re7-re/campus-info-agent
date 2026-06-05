# agent/agent_core.py
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from config import Config
from agent.tools import TOOLS

def get_llm(service: str = None):
    """
    根据配置获取LLM模型
    
    Args:
        service: AI服务名称，可选值: zhipu, siliconflow, deepseek
    
    Returns:
        ChatOpenAI实例
    """
    if service is None:
        service = Config.DEFAULT_AI_SERVICE
    
    if service == "zhipu":
        return ChatOpenAI(
            api_key=Config.ZHIPU_API_KEY,
            model=Config.ZHIPU_MODEL_NAME,
            base_url=Config.ZHIPU_API_BASE
        )
    elif service == "siliconflow":
        return ChatOpenAI(
            api_key=Config.SILICONFLOW_API_KEY,
            model=Config.SILICONFLOW_MODEL_NAME,
            base_url=Config.SILICONFLOW_API_BASE
        )
    elif service == "deepseek":
        return ChatOpenAI(
            api_key=Config.DEEPSEEK_API_KEY,
            model=Config.DEEPSEEK_MODEL_NAME,
            base_url=Config.DEEPSEEK_API_BASE
        )
    elif service == "longchat":
        return ChatOpenAI(
            api_key=Config.LONGCHAT_API_KEY,
            model=Config.LONGCHAT_MODEL_NAME,
            base_url=Config.LONGCHAT_API_BASE
        )
    elif service == "alibaba":
        return ChatOpenAI(
            api_key=Config.ALIBABA_API_KEY,
            model=Config.ALIBABA_MODEL_NAME,
            base_url=Config.ALIBABA_API_BASE
        )
    else:
        raise ValueError(f"不支持的 AI 服务：{service}")

# 获取默认LLM
llm = get_llm()

# 绑定工具
llm_with_tools = llm.bind_tools(TOOLS)

# 节点
def agent_node(state: MessagesState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 工具节点
tool_node = ToolNode(TOOLS)

# 构建流程
workflow = StateGraph(MessagesState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# 判断是否调用工具
def should_continue(state):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"

# 流程
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")
workflow.set_entry_point("agent")

# 编译
agent = workflow.compile()
