from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage

from code.aiagent.models import llm, router_model
from code.aiagent.state import RagState, RouterState
from code.aiagent.prompts import SYSTEM_PROMPT, MSG, ROUTER_PROMPT
from code.aiagent.vectorstore import retriever


def retrieve(state: RagState):
    print("========= state(retrieve) ======")
    print(state)
    # query = state['question'] ? state['question']:state['messages'][-1]
    query = state["question"] if "question" in state else state["messages"][-1].content
    # messages = [HumanMessage(content=query)]

    retrieved_docs = retriever.invoke(query)
    # print(f"retrieved_docs: {retrieved_docs}\n\n")
    return {"context": retrieved_docs}


# Function to generate response
def generate(state: RagState):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])

    query = state["question"] if "question" in state else state["messages"][-1].content

    # Invoke the model with system and human messages
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=MSG.format(context=docs_content, question=query)),
    ]

    response = llm.invoke(messages)
    return {"messages": [response]}


def router_node(state: RouterState):

    messages = [{"role": "system", "content": ROUTER_PROMPT}] + state["messages"]
    route = router_model.invoke(messages)
    print(f"===route=====\n {route}")
    return {"route": route["route"]}


def normal_llm_node(state: RouterState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def route_after_prediction(
    state: RouterState,
) -> Literal["tools", "retrieval", "normal_llm_node"]:
    if state["route"] == "tools_call":
        return "tools"
    elif state["route"] == "retrieval":
        return "retrieval"
    else:
        return "normal_llm_node"
