from typing import TypedDict, Any
import pandas as pd

class AnalystState(TypedDict, total=False):
    question: str
    schema: str
    df: pd.DataFrame
    task_type: str
    sql_query: str
    result: str
    chart: Any
    explanation: str