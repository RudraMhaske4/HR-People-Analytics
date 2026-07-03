import streamlit as st

from dashboard.home import show_home
from dashboard.executive_summary import show_executive_summary
from dashboard.attrition_dashboard import show_attrition_dashboard
from dashboard.employee_reports import show_employee_reports
from dashboard.resume_screening import show_resume_screening
from dashboard.chatbot_page import show_chatbot_page
from dashboard.statistics import show_project_statistics

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

ATTRITION_DATA_PATH = DATA_DIR / "employee_attrition.csv"
HIGH_RISK_PATH = REPORTS_DIR / "high_risk_employees.csv"

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="HR Analytics AI Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# GLOBAL PREMIUM CSS
# =========================================================
st.markdown("""
<style>
/* ========== Main App Background ========== */
.stApp {
    background: linear-gradient(180deg, #0B1220 0%, #0F172A 100%);
    color: #F8FAFC;
}

/* ========== Main Block Spacing ========== */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    max-width: 1500px;
}

/* ========== Sidebar ========== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1E293B 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Sidebar radio labels */
div[role="radiogroup"] label {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px 12px;
    margin-bottom: 8px;
    transition: 0.2s ease;
}

div[role="radiogroup"] label:hover {
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(124,58,237,0.25);
}

/* ========== Titles / Headings ========== */
h1, h2, h3 {
    color: #F8FAFC !important;
    letter-spacing: -0.02em;
}

h1 {
    font-weight: 800 !important;
}

h2 {
    font-weight: 750 !important;
}

h3 {
    font-weight: 700 !important;
}

/* ========== Text Inputs / Text Areas / Selects ========== */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    background-color: #111827 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    color: #F8FAFC !important;
}

textarea, input {
    color: #F8FAFC !important;
}

/* ========== File uploader ========== */
section[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02);
    border: 1px dashed rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 12px;
}

/* ========== Buttons ========== */
.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    background: linear-gradient(135deg, #7C3AED, #2563EB);
    color: white;
    font-weight: 700;
    padding: 0.75rem 1rem;
    box-shadow: 0 8px 24px rgba(124,58,237,0.28);
    transition: 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 28px rgba(124,58,237,0.35);
}

/* ========== Dataframe / table area ========== */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    overflow: hidden;
}

/* ========== Metric cards ========== */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.16), rgba(37,99,235,0.10));
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.16);
}

/* ========== Expanders ========== */
details {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 6px 10px;
}

/* ========== Divider ========== */
hr {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 1.5rem 0;
}

/* ========== Small caption text ========== */
.caption, small {
    color: #94A3B8 !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(37,99,235,0.10));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px 16px;
        margin-bottom: 18px;
        text-align: center;
    ">
        <div style="font-size: 1.9rem; font-weight: 800; color: #F8FAFC;">
            🧠 HR Analytics AI
        </div>
        <div style="font-size: 0.95rem; color: #CBD5E1; margin-top: 8px; line-height: 1.6;">
            LLM-Powered Intelligent Predictive HR System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation")

    page = st.radio(
        "",
        [
            "Home",
            "Executive Summary",
            "Attrition Dashboard",
            "Employee Reports",
            "Resume Screening",
            "HR Copilot Chatbot",
            "Project Statistics"
        ]
    )

    st.markdown("---")
    st.caption("Developed by Rudra Sharad Mhaske")


# =========================================================
# PAGE ROUTING
# =========================================================
if page == "Home":
    show_home()

elif page == "Executive Summary":
    show_executive_summary()

elif page == "Attrition Dashboard":
    show_attrition_dashboard()

elif page == "Employee Reports":
    show_employee_reports()

elif page == "Resume Screening":
    show_resume_screening()

elif page == "HR Copilot Chatbot":
    show_chatbot_page()

elif page == "Project Statistics":
    show_project_statistics()