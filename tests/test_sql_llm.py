import pandas as pd

from llm.model import get_llm

df = pd.read_csv("house_price.csv")

schema = "\n".join(
    f"- {column}: {dtype}"
    for column, dtype in df.dtypes.items()
)

question = "What is the average price?"

prompt = f"""
You are an expert data analyst.

You have access to a DuckDB table called `data`.

Dataset schema:

{schema}

User question:

{question}

Generate a DuckDB-compatible SQL query.

Rules:
1. Use only the table `data`.
2. Use only columns from the schema.
3. Generate SELECT queries only.
4. Return only the SQL query.
"""

llm = get_llm()

response = llm.invoke(prompt)

print("RESPONSE:")
print(response.content)