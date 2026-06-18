# agent/agent_core.py
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from config import Config
from agent.tools import TOOLS
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

# 设置重试策略
retry_strategy = Retry(
    total=Config.API_RETRY_COUNT,
    backoff_factor=Config.API_RETRY_DELAY,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods= ["GET", "POST"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

logger = logging.getLogger("agent_core")

def get_llm(service: str = None):
    """
    根据配置获取LLM模型
    
    Args:
        service: AI服务名称，可选值: zhipu, siliconflow, deepseek, longchat, alibaba
    
    Returns:
        ChatOpenAI实例
    """
    if service is None:
        service = Config.DEFAULT_AI_SERVICE
    
    common_params = {
        "request_timeout": Config.API_TIMEOUT,
        "max_retries": Config.API_RETRY_COUNT
    }
    
    try:
        if service == "zhipu":
            return ChatOpenAI(
                api_key=Config.ZHIPU_API_KEY,
                model=Config.ZHIPU_MODEL_NAME,
                base_url=Config.ZHIPU_API_BASE,
                **common_params
            )
        elif service == "siliconflow":
            return ChatOpenAI(
                api_key=Config.SILICONFLOW_API_KEY,
                model=Config.SILICONFLOW_MODEL_NAME,
                base_url=Config.SILICONFLOW_API_BASE,
                **common_params
            )
        elif service == "deepseek":
            return ChatOpenAI(
                api_key=Config.DEEPSEEK_API_KEY,
                model=Config.DEEPSEEK_MODEL_NAME,
                base_url=Config.DEEPSEEK_API_BASE,
                **common_params
            )
        elif service == "longchat":
            return ChatOpenAI(
                api_key=Config.LONGCHAT_API_KEY,
                model=Config.LONGCHAT_MODEL_NAME,
                base_url=Config.LONGCHAT_API_BASE,
                **common_params
            )
        elif service == "alibaba":
            return ChatOpenAI(
                api_key=Config.ALIBABA_API_KEY,
                model=Config.ALIBABA_MODEL_NAME,
                base_url=Config.ALIBABA_API_BASE,
                **common_params
            )
        else:
            raise ValueError(f"不支持的 AI 服务：{service}")
    except Exception as e:
        logger.error(f"创建LLM模型失败 ({service}): {str(e)}")
        raise

# 获取默认LLM
try:
    llm = get_llm()
    llm_with_tools = llm.bind_tools(TOOLS)
    logger.info(f"成功初始化LLM模型: {Config.DEFAULT_AI_SERVICE}")
except Exception as e:
    logger.error(f"LLM模型初始化失败: {str(e)}")
    llm = None
    llm_with_tools = None

# 节点
def agent_node(state: MessagesState):
    messages = state["messages"]
    try:
        if llm_with_tools is None:
            raise Exception("LLM模型未初始化")
        
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    except Exception as e:
        logger.error(f"智能体节点执行错误: {str(e)}")
        raise

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
try:
    agent = workflow.compile()
    logger.info("智能体工作流编译成功")
except Exception as e:
    logger.error(f"智能体工作流编译失败: {str(e)}")
    agent = None
