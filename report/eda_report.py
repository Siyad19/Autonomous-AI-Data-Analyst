from pathlib import Path
from ydata_profiling import ProfileReport


def generate_eda_report(df):

    profile = ProfileReport(
        df,
        title="Exploratory Data Analysis Report",
        explorative=True,
    )

    report_path = Path("automated_eda_report.html")

    profile.to_file(str(report_path))

    return report_path