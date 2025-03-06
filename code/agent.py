from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, START

from code.aiagent.state import RouterState
from code.aiagent.nodes import router_node, normal_llm_node, route_after_prediction
from code.aiagent.graphs import rag_graph, rc_tool_graph

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
        self.graph.add_node("retrieval", rag_graph)
        self.graph.add_node("tools", rc_tool_graph)
        self.graph.add_edge(START, "router_node")
        self.graph.add_conditional_edges("router_node", route_after_prediction)
        self.graph.add_edge("normal_llm_node", END)
        self.graph.add_edge("retrieval", END)
        self.graph.add_edge("retrieval", END)

    def get_graph(self, memory):
        return self.graph.compile(checkpointer=memory)


graph = AgentGraph().get_graph(memory)


if __name__ == "__main__":
    inputs = {"messages": [("user", "What is the status of my campaign?")]}
    # question = {"question": "How to create new campaign?"}
    config = {"configurable": {"thread_id": "1"}}
    response = graph.invoke(inputs, config=config, stream_mode="values")
    print(response["messages"][-1].content)
