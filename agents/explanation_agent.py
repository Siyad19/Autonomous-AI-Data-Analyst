from graph.state import AnalystState
from llm.model import get_llm
from prompts.explanation_prompt import get_explanation_prompt

def explanation_agent(state: AnalystState):

    question = state['question']
    result = state['result']

    llm = get_llm()

    prompt = get_explanation_prompt(
        question,
        result
    )

    response = llm.invoke(prompt)

    final_result = response.content.strip()

    return {
        "explanation": final_result
    }