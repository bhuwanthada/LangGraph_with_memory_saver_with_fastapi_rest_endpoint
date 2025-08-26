from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langchain.tools import tool
from typing import TypedDict, Optional, List

load_dotenv()


@tool
def give_name_agent_1(message: str):
    """This method is used to calculate the name."""
    return f"Hello, {message} from agent-1"


@tool
def give_name_agent_2(message: str):
    """This method is used to get the message value."""
    return f"Hello, {message} from agent-2"


@tool
def given_name_agent_3(message: str):
    """This method is used to get the message value."""
    return f"Hello, {message} from agent-3"


class AgentState(TypedDict):
    user_id: str
    current_message: str
    message_history: Optional[List]


def agent_one(state: AgentState):
    m_history = state.get("message_history")
    id = state.get("user_id")
    resp = give_name_agent_1.invoke(id)
    m_history.append(f"agent_1: {resp}")
    return {"current_message": resp, "message_history": m_history}


def agent_two(state: AgentState):
    m_history = state.get("message_history")
    id = state.get("user_id")
    resp = give_name_agent_2.invoke(id)
    m_history.append(f"agent_2: {resp}")

    return {"current_message": resp, "message_history": m_history}


def agent_three(state: AgentState):
    m_history = state.get("message_history")
    id = state.get("user_id")
    resp = given_name_agent_3.invoke(id)
    m_history.append(f"agent_3: {resp}")
    return {"current_message": resp, "message_history": m_history}


def compile_graph():
    memory_obj = MemorySaver()
    graph = StateGraph(AgentState)
    graph.add_node("agent_one", agent_one)
    graph.add_node("agent_two", agent_two)
    graph.add_node("agent_three", agent_three)

    graph.add_edge("agent_one", "agent_two")
    graph.add_edge("agent_two", "agent_three")
    graph.add_edge(START, "agent_one")
    graph.add_edge("agent_three", END)
    app = graph.compile(checkpointer=memory_obj, interrupt_after=["agent_two"])
    return memory_obj, app
