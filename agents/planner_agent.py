from graph.state import AnalystState
from prompts.planner_prompt import get_planner_prompt
from llm.model import get_llm

def planner_agent(state: AnalystState):

    question = state["question"]
    schema = state["schema"]

    # LLM 
    llm = get_llm()

    # Prompt for planner agent
    prompt = get_planner_prompt(
        question,
        schema
    )

    # Get response
    response = llm.invoke(prompt)

    # Fetch task type with uppercase format
    task_type = response.content.strip().upper()

    # Clean possible formatting
    task_type = task_type.replace(
         "`",
        ""
    ).strip()

    # Verify task type before passing
    if task_type not in [
        "SQL",
        "PYTHON",
        "VISUALIZATION"
    ]:
        raise ValueError(
            f"Invalid planner response: {task_type}"
        )
    
    return{
        "task_type": task_type
    }