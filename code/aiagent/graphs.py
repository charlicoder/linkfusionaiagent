from langgraph.graph import StateGraph, END, START, MessagesState
from langgraph.prebuilt import ToolNode, create_react_agent
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.runnables.config import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver

from code.aiagent.models import llm
from code.aiagent.tools import all_tools
from code.aiagent.state import RagState
from code.aiagent.nodes import retrieve, generate

memory = MemorySaver()

tool_node = ToolNode(all_tools)
llm_with_tools = llm.bind_tools(all_tools)


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


def call_model(state: MessagesState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# rc_tool_graph = create_react_agent(llm, all_tools)


class ToolsFlow:
    def __init__(self):
        self.workflow = StateGraph(MessagesState)

        # Define the two nodes we will cycle between
        self.workflow.add_node("agent", call_model)
        self.workflow.add_node("tools", tool_node)

        self.workflow.add_edge(START, "agent")
        self.workflow.add_conditional_edges("agent", should_continue, ["tools", END])
        self.workflow.add_edge("tools", "agent")

    def get_tools_graph(self, memory=None):
        return self.workflow.compile(checkpointer=memory)


class RagFlow:
    def __init__(self):
        self.rag_workflow = StateGraph(RagState)
        # rag_workflow.add_node(retrieve)
        # rag_workflow.add_node(retrieve)
        self.rag_workflow.add_sequence([retrieve, generate])

        self.rag_workflow.add_edge(START, "retrieve")
        self.rag_workflow.add_edge("generate", END)

    def get_rag_graph(self, memory=None):
        return self.rag_workflow.compile(checkpointer=memory)
