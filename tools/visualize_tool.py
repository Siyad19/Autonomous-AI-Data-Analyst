from langchain_core.tools import tool
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualize_tools(df):

    @tool
    def create_histogram(column: str):
        """Create a histogram for a numerical column."""

        fig, ax = plt.subplots()
        ax.hist(df[column].dropna())

        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        ax.set_title(f"Distribution of {column}")

        return fig

    @tool
    def create_scatterplot(x_column: str, y_column: str):
        """Create a scatter plot between two numerical columns"""

        fig, ax = plt.subplots()

        ax.scatter(
            df[x_column],
            df[y_column]
        )

        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"{x_column} vs {y_column}")

        return fig

    @tool
    def create_barplot(column: str):
        """Create a barplot/barchart for showing the categorical frequencies."""

        fig, ax = plt.subplots()

        ax.bar(df[column])

        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        ax.set_title(f"Bar chart of {column}")

        return fig

    @tool
    def create_lineplot(x_column: str, y_column: str):
        """Create a line plot using two columns."""

        fig, ax = plt.subplots()
        
        ax.plot(
            df[x_column],
            df[y_column]
        )
        
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"{x_column} vs {y_column}")
        
        return fig

    @tool
    def create_boxplot(column: str):
        """Create a boxplot for a numerical column to visualize its distribution and outliers."""

        fig, ax = plt.subplots()

        ax.boxplot(df[column].dropna())

        ax.set_ylabel(column)
        ax.set_title(f"Boxplot of {column}")

        return fig

    @tool
    def create_heatmap():
        """Create a heatmap for correlation analysis of numerical columns."""

        numerical_df = df.select_dtypes(include="number")
        correlation = numerical_df.corr()

        fig, ax = plt.subplots()

        sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap")

        return fig


    return [
        create_histogram,
        create_barplot,
        create_boxplot,
        create_lineplot,
        create_scatterplot,
        create_heatmap
    ]