from graph.state import AnalystState

def router_task(state: AnalystState):

    task_type = state["task_type"]

    if task_type == "SQL":
        return "sql"
    elif task_type == "PYTHON":
        return "python"
    elif task_type == "VISUALIZATION":
        return "visualize"
    else:
        raise ValueError(
            f"Unknown task type: {task_type}"
        )