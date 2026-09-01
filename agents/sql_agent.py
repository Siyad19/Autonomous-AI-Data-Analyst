from graph.state import AnalystState
from llm.model import get_llm
from prompts.sql_prompt import get_sql_prompt
from tools.sql_tool import SQLTool

def sql_agent(state: AnalystState):

    question = state['question']
    schema = state['schema']

    llm = get_llm()

    prompt = get_sql_prompt(
        question,
        schema
    )

    response = llm.invoke(
        prompt
    )

    sql_query = response.content.strip()

    sql_tool = SQLTool(
        state['df']
    ) 

    result = sql_tool.execute(
        sql_query
    )

    return {
        # "sql_query": sql_query,
        "result": result
    }