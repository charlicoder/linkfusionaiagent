from langgraph.graph import MessagesState
from typing import TypedDict, List, Literal, Dict
from langchain_core.documents import Document


class RagState(MessagesState):
    question: str
    # answer: str
    context: List[Document]


class RouterState(MessagesState):
    route: Literal["tools_call", "retrieval"]


class Router(TypedDict):
    route: Literal["tools_call", "retrieval"]


class CampaignNameInput(TypedDict):
    content: str


class CampaignNameOutput(TypedDict):
    """Respond to the user with campaign name or set null"""

    campaign_name: str | None
    contacts: List[Dict[str, str]]
    action: str
