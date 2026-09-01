import streamlit as st
import pandas as pd

from analyzer.data_profiler import DataProfiler
from llm.model import get_llm
from prompts.sql_prompt import get_sql_prompt
from prompts.explanation_prompt import get_explanation_prompt
from tools.sql_tool import SQLTool

from graph.workflow import graph

st.set_page_config(
    page_title="Autonomous AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #0e1117 0%, #161a25 100%);
    }

    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #7F5AF0, #2CB67D) !important;
        background-clip: text !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        color: transparent !important;
        margin-bottom: 0px !important;
        line-height: 1.2 !important;
    }

    .subtitle {
        color: #9CA3AF;
        font-size: 2rem !important;
        margin-bottom: 1.5rem;
    }

    .section-header {
        font-size: 1.3rem !important;
        font-weight: 700;
        color: #E5E7EB;
        border-left: 4px solid #7F5AF0;
        padding-left: 10px;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
    }

    div[data-testid="stMetric"] {
        background-color: #1E2130;
        border: 1px solid #2A2E3F;
        border-radius: 12px;
        padding: 12px 8px;
    }

    div[data-testid="stMetricValue"] {
        color: #2CB67D;
    }

    .stButton>button {
        background: linear-gradient(90deg, #7F5AF0, #6246EA);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 26px;
        font-weight: 600;
        transition: 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 12px rgba(127, 90, 240, 0.5);
    }

    div[data-testid="stFileUploader"] {
        border: 1px dashed #7F5AF0;
        border-radius: 12px;
        padding: 10px;
    }

    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown('<p class="main-title">Autonomous AI Data Analyst</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload a CSV, ask a questions, and let the agent analyze it for you.</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📁 Upload your CSV file",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.markdown('<p class="section-header">📄 Dataset Preview</p>', unsafe_allow_html=True)
    st.dataframe(df.head())

    profiler = DataProfiler(df)

    profile = profiler.get_profile()

    # Basic Information
    st.markdown('<p class="section-header">📊 Basic Information</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows",
            profile["rows"]
        )
    with col2:
        st.metric(
            "Columns",
            profile["columns"]
        )
    with col3:
        st.metric(
            "Duplicates",
            profile["duplicate_rows"]
        )

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.markdown('<p class="section-header">🧬 Dataset Schema</p>', unsafe_allow_html=True)

        schema_df = pd.DataFrame({

            "Column": df.columns,

            "Data Type": [
                str(dtype)
                for dtype in df.dtypes
            ]

        })

        st.dataframe(
            schema_df,
            width="stretch"
        )

    with exp_col2:
        st.markdown('<p class="section-header">🕳️ Missing Values</p>', unsafe_allow_html=True)

        missing_df = pd.DataFrame({
            "Columns":  df.columns,
            "Missing values": [
                int(value)
                for value in df.isnull().sum()
            ]
        })

        st.dataframe(
            missing_df,
            width="stretch"
        )

    st.markdown('<p class="section-header">💬 Ask a question</p>', unsafe_allow_html=True)

    question = st.text_input(
        "Enter a question.",
    )

    analyze_button = st.button(
        "🚀 Analyze"
    )

    schema = "\n".join(
        f"- {column}: {dtype}"
        for column, dtype in df.dtypes.items()
    )

    if analyze_button:
        if not question:
            st.warning("Please enter a question!")
            st.stop()

        else:
            initial_state = {
                "df": df,
                "question": question,
                "schema": schema
            }

            with st.spinner(
                "Analyzing the data..." 
            ):
                try:

                    with st.expander("🧠 Show agent workflow"):
                        for event in graph.stream(initial_state):
                            st.write(event)

                    result = graph.invoke(initial_state)

                    st.markdown('<p class="section-header">✨ AI Analysis</p>', unsafe_allow_html=True)

                    st.write(result.get("result", "no answer generated."))

                    st.write(result.get("explanation", "no explanation found."))

                    if result.get("chart") is not None:
                    
                        st.markdown('<p class="section-header">📈 Visualization</p>', unsafe_allow_html=True)
                    
                        st.pyplot(result["chart"], width=1000)
                    

                except Exception as e:
                    st.error(
                        f"Analysis falied: {str(e)}"
                    )