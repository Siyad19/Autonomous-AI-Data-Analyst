from graph.state import AnalystState
from llm.model import get_llm
from prompts.visualize_prompt import get_visualize_prompt
from tools.visualize_tool import create_visualize_tools
from langgraph.prebuilt import ToolNode

def visualize_agent(state: AnalystState):

    question = state['question']
    schema = state['schema']
    df = state['df']

    llm = get_llm()

    prompt = get_visualize_prompt(
        schema,
        question
    )

    tools = create_visualize_tools(df)

    tool_node = ToolNode(tools)

    llm_with_tools = llm.bind_tools(tools)

    response = llm_with_tools.invoke(
        prompt
    )

    visualization_plan = response.content.strip()

    # For now, directly call the selected tool
    # fig = tools[0].invoke({
    #     "column": "price"
    # })

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call['name']
        tool_args = tool_call['args']

        selected_tool = next(
            tool for tool in tools
            if tool.name == tool_name
        )

        fig = selected_tool.invoke(tool_args)

        return{
            "result": visualization_plan,
            "chart": fig
        }

    return {
        "result": visualization_plan,
        "chart": fig
    }