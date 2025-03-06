from langgraph.graph import StateGraph, END, START, MessagesState
from langgraph.prebuilt import ToolNode, create_react_agent
from langchain_core.runnables.config import RunnableConfig

from code.aiagent.models import llm
from code.aiagent.tools import all_tools
from code.aiagent.state import RagState
from code.aiagent.nodes import retrieve, generate


# tool_node = ToolNode(all_tools)
# llm_with_tools = llm.bind_tools(all_tools)

rc_tool_graph = create_react_agent(llm, all_tools)


class RagFlow:
    def __init__(self):
        self.rag_workflow = StateGraph(RagState)
        # rag_workflow.add_node(retrieve)
        # rag_workflow.add_node(retrieve)
        self.rag_workflow.add_sequence([retrieve, generate])

        self.rag_workflow.add_edge(START, "retrieve")
        self.rag_workflow.add_edge("generate", END)

    def get_rag_graph(self):
        return self.rag_workflow.compile()


rag_graph = RagFlow().get_rag_graph()
