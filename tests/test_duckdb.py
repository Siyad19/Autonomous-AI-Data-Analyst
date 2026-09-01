import pandas as pd

from data.duckdb_manager import DuckDBManager

df = pd.read_csv("house_price.csv")

db = DuckDBManager()

db.register_dataframe(df, "data")

result = db.execute_query("""
    SELECT AVG(price) FROM data;
""")

print(result)