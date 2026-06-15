from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from ...domain.models.graph_state import BrandState

class AgentState(BrandState, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
