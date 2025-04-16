from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage
from code.aiagent.state import RouterState
from code.aiagent.nodes import (
    router_node,
    normal_llm_node,
    chatbot,
    route_after_prediction,
)
from code.aiagent.tools import all_tools
from code.aiagent.graphs import ToolsFlow, RagFlow

memory = MemorySaver()

graph_builder = StateGraph(RouterState)

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=all_tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")


graph = graph_builder.compile(checkpointer=memory)
