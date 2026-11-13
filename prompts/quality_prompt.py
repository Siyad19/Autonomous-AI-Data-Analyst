def get_quality_prompt(quality_report):
    return f"""
You are a Data Quality Analyst.

Analyze the following data quality report.

DATA QUALITY REPORT:
{quality_report}

Your responsibilities:

1. Assess the overall quality of the dataset.
2. Identify major data quality problems.
3. Identify strengths of the dataset.
4. Explain important findings in simple language.
5. Provide practical recommendations.

Do NOT invent statistics.
Use only the information provided in the report.

Return the response in this structure:

Data quality score:
(out of 100)

Overall Assessment:
...

Strengths:
- ...

Issues:
- ...

Recommendations:
- ...
"""