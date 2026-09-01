from langchain_core.tools import tool

def create_python_tools(df):

    @tool
    def calculate_mean(column: str):
        """Claculate mean/average of a numerical column."""
        return float(df[column].mean())

    @tool
    def calculate_median(column: str):
        """Calculate median of a numerical column."""
        return float(df[column].median())

    @tool
    def calculate_mode(column: str):
        """Calculate mode of a column."""
        return df[column].model().tolist()

    @tool
    def calculate_std(column: str):
        """Calculate standard deviation of a numerical column."""
        return float(df[column].std())

    @tool
    def calculate_variance(column: str):
        """"Calculate the variance of a numerical column."""
        return float(df[column].var())

    @tool
    def calculate_correlation(column1: str, column2: str):
        """Calculate the correlation between two numerical columns."""
        return float(df[column1].corr(df[column2]))

    @tool
    def calculate_corr_with_target(target: str):
        """Calculate the correlation between target and all numerical columns."""
        correlation = df.corr(numerical_only=True)[target]
        return correlation.to_dict()

    @tool
    def get_unique_values(column: str):
        """Return unique values from a column."""
        return df[column].dropna().unique().tolist()

    @tool
    def get_value_counts(column: str):
        """"Return the frequency counts for values in a column."""
        return df[column].value_counts().to_dict()

    @tool
    def get_missing_values():
        """Return the missing value counts for all columns."""
        return df.isnull().sum().to_dict()

    @tool
    def find_outliers(column: str):
        """find the outliers using IQR method."""
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[(df[column] < lower) | (df[column] > upper)]

        return{
            "count": len(outliers),
            "lower_bound": float(lower),
            "upper_bound": float(upper)
        } 

    @tool
    def describe_column(column: str):
        """Return descriptive statistics for a numerical column."""
        return df[column].describe().to_dict()

    return[
        calculate_mean,
        calculate_median,
        calculate_mode,
        calculate_correlation,
        calculate_corr_with_target,
        calculate_std,
        calculate_variance,
        get_missing_values,
        get_unique_values,
        get_value_counts,
        find_outliers,
        describe_column
    ]