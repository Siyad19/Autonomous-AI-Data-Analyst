from graph.state import AnalystState
from llm.model import get_llm
from prompts.python_prompt import get_python_prompt
from tools.python_tools import create_python_tools

def python_agent(state: AnalystState):

    question = state["question"]
    schema = state["schema"]
    df = state["df"]

    llm = get_llm()

    tools = create_python_tools(df)

    llm_with_tools = llm.bind_tools(tools)

    prompt = get_python_prompt(
        schema,
        question
    )

    response = llm_with_tools.invoke(
        prompt
    )

    analysis = response.content.strip()

    return {
        "result": analysis
    }