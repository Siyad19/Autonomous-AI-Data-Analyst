import pandas as pd

class DataProfiler:

    def __init__(self, df:pd.DataFrame):
        self.df = df


    def get_profile(self):
        """
        Generate basic information about the dataset.
        """

        profile = {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "columns_list": list(self.df.columns),
            "data_types": {
                column: str(dtype)
                for column, dtype in self.df.dtypes.items()
            },
            "missing_values": {
                column: int(value)
                for column, value in self.df.isnull().sum().items()
                if value > 0
            },
            "duplicate_rows": int(self.df.duplicated().sum())
        }
        # print(self.df.dtypes)
        # print(self.df.isnull().sum())
        # print(self.df.duplicated().sum())

        return profile