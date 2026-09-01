import duckdb
import pandas as pd


class DuckDBManager:

    def __init__(self):
        self.connection = duckdb.connect(database=":memory:")

    def register_dataframe(self, df: pd.DataFrame, table_name: str = "data"):
        """
        Register a Pandas DataFrame as a DuckDB table.
        """
        self.connection.register(table_name, df)

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query and return the result as a DataFrame.
        """
        return self.connection.execute(query).fetchdf()

    def get_schema(self, table_name: str = "data") -> pd.DataFrame:
        """
        Get table schema.
        """
        query = f"DESCRIBE {table_name}"
        return self.execute_query(query)

    def close(self):
        self.connection.close() 