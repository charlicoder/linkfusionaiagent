from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import HumanMessage
from code.aiagent.state import RouterState
from code.aiagent.nodes import router_node, normal_llm_node, route_after_prediction
from code.aiagent.graphs import ToolsFlow, RagFlow

# import sys
# import os

# pwd = os.getcwd()  # Get the current working directory
# sys.path.append(pwd)

memory = MemorySaver()


class AgentGraph:
    def __init__(self):
        self.graph = StateGraph(RouterState)
        self.graph.add_node(router_node)
        self.graph.add_node(normal_llm_node)
        rag_graph = RagFlow().get_rag_graph(memory)
        self.graph.add_node("retrieval", rag_graph)
        rc_tool_graph = ToolsFlow().get_tools_graph(memory)
        self.graph.add_node("tools", rc_tool_graph)
        self.graph.add_edge(START, "router_node")
        self.graph.add_conditional_edges("router_node", route_after_prediction)
        self.graph.add_edge("normal_llm_node", END)
        self.graph.add_edge("retrieval", END)
        self.graph.add_edge("retrieval", END)

    def get_graph(self, memory=None):
        return self.graph.compile(checkpointer=memory)


graph_builder = AgentGraph()
graph = graph_builder.get_graph(memory)


if __name__ == "__main__":

    # question = {"question": "How to create new campaign?"}
    config = {
        "thread_id": "1",
        "user_id": "1",
        "user_name": "Rafin",
        "env": "local",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3Nzk0MDAzLCJpYXQiOjE3NDIyNDIwMDMsImp0aSI6ImU1NzRiZTMyYTEyZjQ0YzU5N2VmMWViYmJjMjA4YzQxIiwidXNlcl9pZCI6MTM4fQ.YOG-Uy4rIaR3qrgFe0XoT5bHgzVRAbGKTpVsGLs65uw",
    }

    input_message = HumanMessage(content="hi! I'm bob")
    inputs = {"messages": [input_message]}
    response = graph.invoke(inputs, config=config, stream_mode="values")
    print(response["messages"][-1].content)

    input_message = HumanMessage(content="what's my name?")
    inputs = {"messages": [input_message]}
    # question = {"question": "How to create new campaign?"}
    # config = {"configurable": {"thread_id": "1"}}
    response = graph.invoke(inputs, config=config, stream_mode="values")
    print(response["messages"][-1].content)
