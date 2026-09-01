# Autonomous AI Data Analyst

An **AI-powered autonomous data analysis application** that allows users to upload a CSV dataset and ask questions in natural language.

The system uses **LLMs, LangChain, LangGraph, DuckDB, Pandas, and Matplotlib** to analyze data, generate SQL queries, perform Python-based analysis, and create visualizations dynamically.

## 🎯 Project Goal

The goal of this project is to build an AI Data Analyst that can:

- Understand natural-language questions about a dataset
- Decide which analysis approach is appropriate
- Generate and execute SQL queries
- Perform Python/Pandas-based analysis
- Dynamically create visualizations
- Return understandable results to the user

## 🏗️ Architecture

```text
                    CSV Dataset
                         ↓
                  Data Profiler
                         ↓
                   User Question
                         ↓
                  Planner Agent
                         ↓
                LangGraph Workflow
                         ↓
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      SQL Agent      Python Agent   Visualization Agent
          ↓              ↓              ↓
       DuckDB          Pandas        Matplotlib
          ↓              ↓              ↓
          └──────────────┼──────────────┘
                         ↓
                   Final Result
                         ↓
                     Streamlit
```

# 📌 Versions

## V1 – Basic Data Analysis

Initial version focused on uploading and understanding a dataset.

### Features

- CSV file upload
- Dataset preview
- Row and column count
- Dataset schema
- Data types
- Missing-value information
- Duplicate-row detection
- Basic data profiling

### Technologies

- Python
- Pandas
- Streamlit

---

## V2 – Natural Language → SQL Analysis

V2 introduced LLM-based SQL generation and DuckDB.

### Workflow

```text
User Question
      ↓
     LLM
      ↓
Generate SQL
      ↓
DuckDB
      ↓
Query Result
      ↓
Streamlit
```

### Example

User:

> What is the average price?

The LLM generates:

```sql
SELECT AVG(price) FROM data;
```

DuckDB executes the query and returns the result.

### Features

- Natural-language questions
- LLM-generated SQL
- DuckDB SQL execution
- CSV querying using DuckDB
- SQL error handling

### Technologies

- OpenRouter
- LLM
- DuckDB
- Pandas
- Streamlit

---

# V3 – Autonomous Multi-Agent Data Analyst

V3 introduces an **agentic architecture using LangGraph**.

Instead of using one LLM for every task, specialized agents handle different types of analysis.

### Agents

#### 🧠 Planner Agent

Determines what type of analysis is required and routes the request to the appropriate agent.

#### 🗄️ SQL Agent

Handles questions that are suitable for SQL and uses DuckDB to query the dataset.

#### 🐍 Python Agent

Handles analytical operations using predefined Python/Pandas tools.

Examples:

- Mean
- Median
- Standard deviation
- Correlation
- Outlier detection
- Missing-value analysis
- Statistical analysis

#### 📊 Visualization Agent

Selects appropriate visualization tools and generates charts using Matplotlib.

Examples:

- Histogram
- Boxplot
- Scatter plot
- Bar chart
- Line chart

## 🔄 V3 Workflow

```text
                    User Question
                         ↓
                  Input Validation
                         ↓
                  Planner Agent
                         ↓
                    LangGraph
                         ↓
              ┌──────────┼──────────┐
              ↓          ↓          ↓
          SQL Agent  Python Agent  Viz Agent
              ↓          ↓          ↓
           DuckDB     Pandas     Matplotlib
              ↓          ↓          ↓
              └──────────┼──────────┘
                         ↓
                  Result Validation
                         ↓
                    Final Answer
                         ↓
                     Streamlit
```

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Pandas | Data processing and analysis |
| DuckDB | SQL queries on CSV/DataFrame data |
| LangChain | LLM and tool integration |
| LangGraph | Agent orchestration and workflow |
| OpenRouter | LLM API |
| Matplotlib | Data visualization |
| Streamlit | Web interface |
| Git/GitHub | Version control |

# 📂 Project Structure

```text
Autonomous-Data-Analyst/
│
├── agents/
│   ├── planner_agent.py
│   ├── sql_agent.py
│   ├── python_agent.py
│   └── visualize_agent.py
│
├── analyzer/
│   └── data_profiler.py
│
├── tools/
│   ├── sql_tool.py
│   ├── python_tools.py
│   └── visualization_tools.py
│
├── prompts/
│   ├── planner_prompt.py
│   ├── sql_prompt.py
│   ├── python_prompt.py
│   └── visualize_prompt.py
│
├── graph/
│   ├── state.py
│   ├── router.py
│   └── workflow.py
│
├── llm/
│   └── model.py
│
├── tests/
│
├── app.py
├── requirements.txt
└── README.md
```

# ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd Autonomous-Data-Analyst
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

# 🔑 Environment Variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

The application uses OpenRouter to access the LLM.

**Do not commit your `.env` file to GitHub.**

Add it to `.gitignore`:

```text
.env
venv/
__pycache__/
.pytest_cache/
```

# ▶️ Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

Then upload a CSV file and ask questions such as:

```text
What is the average price?
```

```text
Which city has the highest average price?
```

```text
What is the correlation between price and sqft_living?
```

```text
Show me the distribution of price.
```

```text
Show outliers in price.
```

# 🎯 Current Status

| Version | Status |
|---|---|
| V1 – Data Profiling | ✅ Completed |
| V2 – SQL + DuckDB | ✅ Completed |
| V3 – Multi-Agent System | 🚧 In Progress / Finalizing |
| V4 – Advanced Autonomous Analysis | 🔜 Planned |

# 🔮 Future Improvements – V4

Possible future features:

- Automatic insight discovery
- Multi-step autonomous analysis
- Automatic dashboard generation
- Conversation memory
- Follow-up questions
- Anomaly detection
- Automated EDA
- Downloadable analysis reports
- Advanced visualization
- Agent evaluation and monitoring
- LangSmith integration
- Improved caching and performance



**Siyad S**

Built as a portfolio project to explore **LLMs, AI Agents, LangChain, LangGraph, data analysis, and autonomous AI systems**.
