from prompts.quality_prompt import get_quality_prompt
from llm.model import get_llm

def data_quality_analyzer_agent(quality_report):
    # LLM 
    llm = get_llm()

    # Prompt for data quality analyzer agent
    prompt = get_quality_prompt(
        quality_report
    )

    # Stream response from LLM
    full_response = ""

    # Get response
    # response = llm.invoke(prompt)
    for chunk in llm.stream(prompt):
        if chunk.content:
            yield chunk.content

    return full_response.strip()