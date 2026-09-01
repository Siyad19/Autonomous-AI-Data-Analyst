from langgraph.graph import StateGraph, START, END
from graph.state import AnalystState
from agents.planner_agent import planner_agent
from agents.python_agent import python_agent
from agents.sql_agent import sql_agent
from agents.visualize_agent import visualize_agent
from agents.explanation_agent import explanation_agent
from graph.router import router_task

workflow = StateGraph(AnalystState)

workflow.add_node(
    "planner",
    planner_agent
)
workflow.add_node(
    "python",
    python_agent
)
workflow.add_node(
    "sql",
    sql_agent
)
workflow.add_node(
    "visualize",
    visualize_agent
)
workflow.add_node(
    "explanation",
    explanation_agent
)

# START Edge -> planner_agent
workflow.add_edge(
    START,
    "planner"
)

# Planner -> assigning to appropriate agent.
workflow.add_conditional_edges(
    "planner",
    router_task,
    {
        "sql": "sql",
        "python": "python",
        "visualize": "visualize"
    }
)

# END Edge -> Agents
workflow.add_edge(
    "sql",
    "explanation",
)
workflow.add_edge(
    "python",
    "explanation",
)
workflow.add_edge(
    "visualize",
    "explanation",
)

# Pass the results to explanation agent, then END.
workflow.add_edge(
    "explanation",
    END
)

# Complie
graph = workflow.compile()