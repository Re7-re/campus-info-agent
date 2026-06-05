# agent/agent_core.py
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from config import ZHIPU_API_KEY, MODEL_NAME
from agent.tools import TOOLS

# 智谱模型
llm = ChatOpenAI(
    api_key=ZHIPU_API_KEY,
    model=MODEL_NAME,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

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