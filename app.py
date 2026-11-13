import streamlit as st
import pandas as pd
import webbrowser
import io
import hashlib

from analyzer.data_profiler import DataProfiler
from graph.workflow import graph

from analyzer.data_quality import DataQualityAnalyzer
from agents.data_quality_analyzer_agent import data_quality_analyzer_agent

from guardrails.input_guardrails import validate_input
from guardrails.output_guardrails import validate_output

from report.eda_report import generate_eda_report


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Autonomous AI Data Analyst",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg, #0e1117 0%, #161a25 100%);
}

.main-title {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #7F5AF0, #2CB67D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px !important;
}

.subtitle {
    color: #9CA3AF;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

.section-header {
    font-size: 1.15rem !important;
    font-weight: 700;
    color: #E5E7EB;
    border-left: 4px solid #7F5AF0;
    padding-left: 10px;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

/* Metrics */

div[data-testid="stMetric"] {
    background-color: #1E2130;
    border: 1px solid #2A2E3F;
    border-radius: 12px;
    padding: 12px;
}

div[data-testid="stMetricValue"] {
    color: #2CB67D;
}

/* Buttons */

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(90deg, #7F5AF0, #6246EA);
    color: white;
    border-radius: 9px;
    border: none;
    padding: 9px 18px;
    font-weight: 600;
    transition: 0.2s ease-in-out;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 12px rgba(127, 90, 240, 0.5);
    border: none;
}

/* File uploader */

div[data-testid="stFileUploader"] {
    border: 1px dashed #7F5AF0;
    border-radius: 12px;
    padding: 10px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #11131d 0%, #191c2b 100%);
    border-right: 1px solid #2A2E3F;
}

section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem;
}

.sidebar-brand {
    font-size: 1.4rem;
    font-weight: 800;
    background: linear-gradient(90deg, #7F5AF0, #2CB67D);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sidebar-caption {
    font-size: 0.85rem;
    color: #9CA3AF;
}

/* Chat messages */

div[data-testid="stChatMessage"] {
    background: #1E2130;
    border: 1px solid #2A2E3F;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
}

/* Containers */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #2A2E3F;
    border-radius: 12px;
}

/* Inputs */

.stTextInput input,
.stTextArea textarea {
    background-color: #1E2130;
    color: #E5E7EB;
    border: 1px solid #383C50;
    border-radius: 8px;
}

/* Expanders */

div[data-testid="stExpander"] {
    background: #191c2b;
    border: 1px solid #2A2E3F;
    border-radius: 10px;
}

hr {
    border-color: #2A2E3F;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "dataset_key" not in st.session_state:
    st.session_state.dataset_key = None

if "last_workflow" not in st.session_state:
    st.session_state.last_workflow = []


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">🤖 AI Data Analyst</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-caption">'
        'Your intelligent data workspace'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 💬 AI Assistant")

    st.caption(
        "Ask questions and explore your dataset "
        "using natural language."
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        width='stretch'
    ):

        st.session_state.chat_history = []
        st.session_state.last_workflow = []

        st.rerun()

    st.markdown(
    '<div style="background:#1E2130;'
    'border:1px solid #2A2E3F;'
    'border-radius:10px;'
    'padding:15px;'
    'margin-top:20px;'
    'color:#9CA3AF;'
    'font-size:13px;">'

    '<b style="color:#2CB67D;">AI Capabilities</b>'
    '<ul style="padding-left:20px;line-height:2;">'
    '<li>Data Analysis</li>'
    '<li>SQL Queries</li>'
    '<li>Python Analysis</li>'
    '<li>Data Visualization</li>'
    '<li>AI Insights</li>'
    '<li>Data Quality Analysis</li>'
    '</ul>'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<p class="main-title">Autonomous AI Data Analyst</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">'
    'Upload your dataset, ask questions and discover '
    'meaningful insights using Agentic AI.'
    '</p>',
    unsafe_allow_html=True
)


# ==================================================
# FILE UPLOADER
# ==================================================

uploaded_file = st.file_uploader(
    "📁 Upload your dataset",
    type=["csv"],
    help="Upload a CSV file to start analyzing your data."
)


if uploaded_file is None:

    st.info(
        "👋 Welcome! Upload a CSV dataset to start "
        "chatting with your AI Data Analyst."
    )

    st.markdown("""
    ### What can you do?

    - Ask questions about your dataset.
    - Generate SQL and Python-based analysis.
    - Discover patterns and relationships.
    - Generate visualizations.
    - Identify data quality issues.
    - Generate an EDA report.
    """)

else:

    # --------------------------------------------------
    # READ DATASET
    # --------------------------------------------------

    file_bytes = uploaded_file.getvalue()

    df = pd.read_csv(
        io.BytesIO(file_bytes)
    )

    # Store dataset
    st.session_state["uploaded_df"] = df.copy()

    # Detect dataset changes
    current_dataset_key = hashlib.sha256(
        file_bytes
    ).hexdigest()

    if st.session_state.dataset_key != current_dataset_key:

        st.session_state.dataset_key = current_dataset_key
        st.session_state.chat_history = []
        st.session_state.last_workflow = []

    # --------------------------------------------------
    # DATA PROFILING
    # --------------------------------------------------

    profiler = DataProfiler(df)

    profile = profiler.get_profile()

    quality_analyzer = DataQualityAnalyzer(df)

    quality_report = quality_analyzer.get_data_quality_report()

    schema = "\n".join(
        f"- {column}: {dtype}"
        for column, dtype in df.dtypes.items()
    )


    # ==================================================
    # MAIN TWO COLUMN LAYOUT
    # ==================================================

    chat_col, data_col = st.columns(
        [0.42, 0.58],
        gap="large"
    )


    # ==================================================
    # LEFT COLUMN
    # CHAT + WORKFLOW + DATA QUALITY + EDA
    # ==================================================

    with chat_col:

        # ----------------------------------------------
        # CHAT SECTION
        # ----------------------------------------------

        st.markdown(
            '<p class="section-header">'
            '💬 Chat with your Dataset'
            '</p>',
            unsafe_allow_html=True
        )

        st.caption(
            "Ask anything about your uploaded dataset."
        )

        # Chat history container

        with st.container(
            height=420,
            border=True
        ):

            if not st.session_state.chat_history:

                with st.chat_message("assistant"):

                    st.markdown("""
                    Hello! 👋

                    I'm your AI Data Analyst.

                    I've received your dataset. You can ask me:

                    - What are the important insights?
                    - Find the correlation between columns.
                    - Show the distribution of numerical features.
                    - Identify unusual patterns.
                    - Visualize the relationship between columns.

                    What would you like to explore?
                    """)

            # Display previous messages

            for message in st.session_state.chat_history:

                with st.chat_message(message["role"]):

                    if message.get("error"):

                        st.error(message["content"])

                    else:

                        st.markdown(message["content"])

                    # Display result

                    if message["role"] == "assistant":

                        result_value = message.get("result")

                        if result_value is not None:

                            with st.expander(
                                "📋 View Analysis Result"
                            ):

                                if isinstance(
                                    result_value,
                                    pd.DataFrame
                                ):

                                    st.dataframe(
                                        result_value,
                                        width='stretch'
                                    )

                                else:

                                    st.write(result_value)

                        # Display chart

                        chart = message.get("chart")

                        if chart is not None:

                            st.markdown("📈 **Visualization**")

                            st.pyplot(
                                chart,
                                width='stretch'
                            )


        # ----------------------------------------------
        # CHAT INPUT
        # ----------------------------------------------

        with st.form(
            "chat_form",
            clear_on_submit=True
        ):

            question = st.text_input(
                "Ask your question",
                placeholder="Example: What is the average value?",
                label_visibility="collapsed"
            )

            submitted = st.form_submit_button(
                "➤ Send Message",
                width='stretch'
            )


        # ----------------------------------------------
        # PROCESS USER QUESTION
        # ----------------------------------------------

        if submitted:

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                try:

                    # Input guardrail
                    validate_input(question)

                    # Prepare conversation context
                    previous_history = (
                        st.session_state.chat_history[-8:]
                    )

                    conversation_context = "\n".join(
                        f"{message['role'].upper()}: "
                        f"{message['content']}"
                        for message in previous_history
                    )

                    if conversation_context:

                        contextual_question = f"""
Previous conversation:
{conversation_context}

Current user question:
{question}
"""

                    else:

                        contextual_question = question

                    # Save user message
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": question
                    })

                    # Initial LangGraph state
                    initial_state = {
                        "df": df,
                        "question": contextual_question,
                        "schema": schema
                    }

                    # Capture final state and workflow events
                    final_state = dict(initial_state)

                    workflow_events = []

                    with st.spinner(
                        "🤖 AI agents are analyzing your dataset..."
                    ):

                        # Execute the graph ONCE
                        for event in graph.stream(
                            initial_state,
                            stream_mode="updates"
                        ):

                            workflow_events.append(event)

                            # Collect node outputs
                            for node_name, node_update in event.items():

                                if isinstance(node_update, dict):

                                    final_state.update(
                                        node_update
                                    )

                    # Save workflow for display after rerun
                    st.session_state.last_workflow = (
                        workflow_events
                    )

                    result = final_state

                    # Extract AI response
                    answer = str(
                        result.get(
                            "explanation",
                            "No explanation found."
                        )
                    )

                    # Output guardrail
                    is_valid, safe_answer = validate_output(
                        answer
                    )

                    if is_valid:

                        assistant_message = {
                            "role": "assistant",
                            "content": safe_answer,
                            "result": result.get("result"),
                            "chart": result.get("chart"),
                            "error": False
                        }

                    else:

                        assistant_message = {
                            "role": "assistant",
                            "content": (
                                "The generated response could not "
                                "pass output safety validation."
                            ),
                            "error": True
                        }

                    st.session_state.chat_history.append(
                        assistant_message
                    )

                    st.rerun()

                except Exception as e:

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Analysis failed: {str(e)}",
                        "error": True
                    })

                    st.rerun()


        # ----------------------------------------------
        # AGENT WORKFLOW SECTION
        # ----------------------------------------------
        st.write('🧠 Agent Workflow')

        st.caption(
            "Track how your AI agents process the question."
        )

        with st.expander(
            "Show agent execution details",
            expanded=False
        ):

            if st.session_state.last_workflow:

                for index, event in enumerate(
                    st.session_state.last_workflow,
                    start=1
                ):

                    for node_name, node_output in event.items():

                        st.markdown(
                            f"**{index}. "
                            f"{node_name.replace('_', ' ').title()}**"
                        )

                        st.write(node_output)

                        st.divider()

            else:

                st.info(
                    "Agent execution details will appear "
                    "here after you ask a question."
                )


        # ----------------------------------------------
        # DATA QUALITY ANALYSIS
        # ----------------------------------------------

        st.divider()

        st.markdown(
            '<p class="section-header">'
            '🛡️ Data Quality Analysis'
            '</p>',
            unsafe_allow_html=True
        )

        if st.button(
            "Analyze Data Quality",
            width='stretch'
        ):

            with st.spinner(
                "Analyzing data quality..."
            ):

                quality_analysis = (
                    data_quality_analyzer_agent(
                        quality_report
                    )
                )

                with st.container(
                    border=True
                ):

                    st.write_stream(
                        quality_analysis
                    )


        # ----------------------------------------------
        # EDA REPORT GENERATION
        # ----------------------------------------------

        st.divider()

        st.markdown(
            '<p class="section-header">'
            '📑 EDA Report Generation'
            '</p>',
            unsafe_allow_html=True
        )

        st.caption(
            "Generate a detailed Exploratory Data Analysis report."
        )

        if st.button(
            "Generate EDA Report",
            width='stretch'
        ):

            with st.spinner(
                "Generating EDA report..."
            ):

                report_path = generate_eda_report(df)

                st.success(
                    "EDA report generated successfully!"
                )

                webbrowser.open_new_tab(
                    report_path.resolve().as_uri()
                )


    # ==================================================
    # RIGHT COLUMN
    # DATASET OVERVIEW
    # ==================================================

    with data_col:

        st.markdown(
            '<p class="section-header">'
            '📊 Dataset Overview'
            '</p>',
            unsafe_allow_html=True
        )

        # ----------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Rows",
                f"{profile['rows']:,}"
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


        with col4:

            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )


        # ----------------------------------------------
        # DATASET PREVIEW
        # ----------------------------------------------

        with st.container(border=True):

            st.markdown("#### 📄 Dataset Preview")

            st.dataframe(
                df.head(10),
                width='stretch',
                height=250
            )


        # ----------------------------------------------
        # DATASET SCHEMA
        # ----------------------------------------------

        with st.expander(
            "🧬 Dataset Schema",
            expanded=True
        ):

            schema_df = pd.DataFrame({
                "Column": df.columns,
                "Data Type": [
                    str(dtype)
                    for dtype in df.dtypes
                ],
                "Unique Values": [
                    int(df[col].nunique())
                    for col in df.columns
                ]
            })

            st.dataframe(
                schema_df,
                width='stretch'
            )


        # ----------------------------------------------
        # MISSING VALUES
        # ----------------------------------------------

        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander(
                "🕳️ Missing Values",
                expanded=False
            ):

                missing_df = pd.DataFrame({
                    "Column": df.columns,
                    "Missing Values": [
                        int(value)
                        for value in df.isnull().sum()
                    ]
                })

                st.dataframe(
                    missing_df,
                    width='stretch',
                    height=300
                )


        # ----------------------------------------------
        # OUTLIER ANALYSIS
        # ----------------------------------------------
        with col2:
            with st.expander(
                "🧩 Outlier Analysis",
                expanded=False
            ):

                outlier_df = pd.DataFrame(
                    quality_report["outliers"].items(),
                    columns=[
                        "Column",
                        "Outlier Count"
                    ]
                )

                st.dataframe(
                    outlier_df,
                    width='stretch',
                    height=300
                )


        # ----------------------------------------------
        # NUMERICAL SUMMARY
        # ----------------------------------------------

        if quality_report["numerical_summary"]:

            with st.expander(
                "📈 Numerical Summary",
                expanded=False
            ):

                numerical_summary_df = pd.DataFrame(
                    quality_report["numerical_summary"]
                ).T

                st.dataframe(
                    numerical_summary_df,
                    width='stretch'
                )


# ==================================================
# END
# ==================================================
