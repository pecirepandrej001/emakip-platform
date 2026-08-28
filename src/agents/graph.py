from langgraph.graph import END, START, StateGraph
from src.agents.state import AgentState
from src.agents.nodes.router_agent import router_agent
from src.agents.nodes.document_analyzer import document_analyzer
from src.agents.nodes.sql_analytics_agent import sql_analytics_agent
from src.agents.nodes.reviewer_agent import reviewer_agent
from src.agents.nodes.summarizer_agent import summarizer_agent

def route_after_router(state: AgentState) -> str:
    return state.get("route", "rag")

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("router", router_agent)
    graph.add_node("rag", document_analyzer)
    graph.add_node("sql", sql_analytics_agent)
    graph.add_node("reviewer", reviewer_agent)
    graph.add_node("summarizer", summarizer_agent)

    graph.add_edge(START, "router")
    graph.add_conditional_edges("router", route_after_router, {"rag": "rag", "sql": "sql"})
    graph.add_edge("rag", "reviewer")
    graph.add_edge("sql", "reviewer")
    graph.add_edge("reviewer", "summarizer")
    graph.add_edge("summarizer", END)
    return graph.compile()

agent_graph = build_graph()

async def run_agent(question: str, user_email: str) -> AgentState:
    return await agent_graph.ainvoke({"question": question, "user_email": user_email, "steps": []})
