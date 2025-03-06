from langgraph.graph import MessagesState
from typing import TypedDict, List, Literal
from langchain_core.documents import Document


class RagState(MessagesState):
    question: str
    # answer: str
    context: List[Document]


class RouterState(MessagesState):
    route: Literal["tools_call", "retrieval"]


class Router(TypedDict):
    route: Literal["tools_call", "retrieval"]
