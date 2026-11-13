import pandas as pd

class DataQualityAnalyzer:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def check_missing_values(self):
        missing_values = self.df.isnull().sum()
        return {
            column: int(count)
            for column, count in missing_values.items()
            if count > 0
        }

    def check_duplicate_rows(self):
        duplicate_count = int(self.df.duplicated().sum())
        return duplicate_count

    def check_duplicate_columns(self):
        duplicate_columns = self.df.columns[self.df.columns.duplicated()].tolist()
        return duplicate_columns

    def check_data_types(self):
        data_types = {
            column: str(dtype)
            for column, dtype in self.df.dtypes.items()
        }
        return data_types

    def numerical_summary(self):
        numerical_summary = self.df.select_dtypes(
            include="number"
        )
        if numerical_summary.empty:
            return {}

        summary = {}
        for column in numerical_summary.columns:
            summary[column] = {
                "mean": numerical_summary[column].mean(),
                "median": numerical_summary[column].median(),
                "standard deviation": numerical_summary[column].std(),
                "min": numerical_summary[column].min(),
                "max": numerical_summary[column].max()
            }

        return summary

    def check_outliers(self):
        numerical_df = self.df.select_dtypes(include="number")

        outliers = {}

        for column in numerical_df.columns:
            q1 = numerical_df[column].quantile(0.25)
            q3 = numerical_df[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            count_outliers = ((numerical_df[column] < lower_bound) | (numerical_df[column] > upper_bound)).sum()
            if count_outliers > 0:
                outliers[column] = int(count_outliers)

        return outliers

    def get_data_quality_report(self):
        report = {
            "missing_values": self.check_missing_values(),
            "duplicate_rows": self.check_duplicate_rows(),
            "duplicate_columns": self.check_duplicate_columns(),
            "data_types": self.check_data_types(),
            "numerical_summary": self.numerical_summary(),
            "outliers": self.check_outliers()
        }
        return report