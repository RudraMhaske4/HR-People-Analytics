import streamlit as st
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

ATTRITION_DATA_PATH = DATA_DIR / "employee_attrition.csv"
RESUME_SCORES_PATH = REPORTS_DIR / "resume_reports" / "candidate_scores.csv"
EMPLOYEE_REPORTS_FOLDER = REPORTS_DIR / "employee_reports"

# =========================================
# Paths
# =========================================
ATTRITION_DATA_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\data\employee_attrition.csv"
RESUME_SCORES_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\resume_reports\candidate_scores.csv"
EMPLOYEE_REPORTS_FOLDER = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\employee_reports"


# =========================================
# Helper: premium KPI card
# =========================================
def premium_card(title, value, subtitle="", color1="#7C3AED", color2="#2563EB"):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color1}22, {color2}18);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px 20px;
            min-height: 125px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.16);
        ">
            <div style="font-size: 0.95rem; color: #CBD5E1; margin-bottom: 8px;">{title}</div>
            <div style="font-size: 2rem; font-weight: 800; color: #F8FAFC;">{value}</div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 8px; line-height: 1.5;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================
# Helper: premium info box
# =========================================
def info_box(title, body, emoji="📌"):
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 20px;
            min-height: 160px;
        ">
            <div style="font-size: 1.08rem; font-weight: 700; color: #F8FAFC; margin-bottom: 10px;">
                {emoji} {title}
            </div>
            <div style="color: #CBD5E1; line-height: 1.7; font-size: 0.95rem;">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================
# Main page
# =========================================
def show_home():
    # -------------------------------------
    # Load summary numbers
    # -------------------------------------
    total_employees = "—"
    high_risk_employees = "—"
    employee_reports_count = "—"
    candidate_match_score = "—"

    if os.path.exists(ATTRITION_DATA_PATH):
        try:
            df = pd.read_csv(ATTRITION_DATA_PATH)
            total_employees = len(df)

            if "Attrition" in df.columns:
                high_risk_employees = int((df["Attrition"].astype(str).str.lower() == "yes").sum())
        except:
            pass

    if os.path.exists(EMPLOYEE_REPORTS_FOLDER):
        try:
            txt_files = [f for f in os.listdir(EMPLOYEE_REPORTS_FOLDER) if f.endswith(".txt")]
            employee_reports_count = len(txt_files)
        except:
            pass

    if os.path.exists(RESUME_SCORES_PATH):
        try:
            score_df = pd.read_csv(RESUME_SCORES_PATH)
            if not score_df.empty and "Overall Match Score" in score_df.columns:
                candidate_match_score = f"{score_df.iloc[0]['Overall Match Score']}%"
        except:
            pass

    # -------------------------------------
    # Hero Section
    # -------------------------------------
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(124,58,237,0.22), rgba(37,99,235,0.14));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 28px 30px;
        margin-bottom: 22px;
        box-shadow: 0 12px 32px rgba(0,0,0,0.18);
    ">
        <div style="font-size: 2.4rem; font-weight: 800; color: #F8FAFC; margin-bottom: 10px;">
            🧠 HR Analytics AI Dashboard
        </div>
        <div style="font-size: 1.05rem; color: #CBD5E1; line-height: 1.8; max-width: 1050px;">
            <b>LLM-Powered Intelligent Predictive HR System</b> designed to combine
            <b>employee attrition analytics</b>, <b>AI-generated employee risk reports</b>,
            <b>resume screening & candidate evaluation</b>, and an <b>HR copilot chatbot</b>
            into one unified decision-support platform for HR teams and leadership.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------
    # KPI Cards
    # -------------------------------------
    st.markdown("## Dashboard Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        premium_card(
            "Total Employees",
            total_employees,
            "Employee records available in the attrition dataset",
            "#7C3AED",
            "#2563EB"
        )

    with c2:
        premium_card(
            "Attrition Cases",
            high_risk_employees,
            "Employees marked with attrition = Yes in the dataset",
            "#DC2626",
            "#F97316"
        )

    with c3:
        premium_card(
            "Employee AI Reports",
            employee_reports_count,
            "AI-generated individual employee risk reports",
            "#059669",
            "#10B981"
        )

    with c4:
        premium_card(
            "Latest Candidate Match",
            candidate_match_score,
            "Most recent resume screening overall match score",
            "#2563EB",
            "#06B6D4"
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # -------------------------------------
    # Project modules
    # -------------------------------------
    st.markdown("## Core Project Modules")

    col1, col2 = st.columns(2)

    with col1:
        info_box(
            "Attrition Intelligence Engine",
            """
            Predicts employee attrition risk using HR and workforce data.  
            Includes risk-focused analysis to help identify employees who may leave the organization,
            along with insights into possible drivers behind attrition.
            """,
            "📉"
        )

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        info_box(
            "Employee AI Risk Reports",
            """
            Generates individual employee-level HR reports using LLM-based reasoning.  
            These reports summarize the employee profile, highlight key risk factors,
            and suggest possible HR interventions or retention actions.
            """,
            "📝"
        )

    with col2:
        info_box(
            "Resume Screening & Candidate Evaluation",
            """
            Evaluates uploaded resumes against a job description using skill matching,
            experience matching, education scoring, and an AI-generated recruiter report.
            This turns the system into both an internal HR analytics tool and a hiring assistant.
            """,
            "🎯"
        )

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        info_box(
            "HR Copilot Chatbot",
            """
            Conversational HR assistant designed to answer HR-related questions using project outputs,
            employee analytics context, and candidate evaluation insights.  
            It acts as a decision-support interface on top of the analytics system.
            """,
            "🤖"
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # -------------------------------------
    # System workflow
    # -------------------------------------
    st.markdown("## How the System Works")

    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 22px;
        line-height: 1.9;
        color: #CBD5E1;
        font-size: 0.97rem;
    ">
        <b>Step 1 — Data Ingestion:</b> HR employee data and candidate resume data are loaded into the system.<br><br>
        <b>Step 2 — Predictive Analytics:</b> Machine learning models estimate employee attrition risk and candidate-job fit scores.<br><br>
        <b>Step 3 — LLM Interpretation:</b> Gemini/LLM components transform raw analytics outputs into recruiter-style and HR-style natural language reports.<br><br>
        <b>Step 4 — Decision Dashboard:</b> Results are displayed through Streamlit dashboards for HR teams, recruiters, and leadership stakeholders.<br><br>
        <b>Step 5 — Copilot Interaction:</b> The HR chatbot acts as a conversational layer for asking questions about employees, risk trends, and candidate fit.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # -------------------------------------
    # Why this project matters
    # -------------------------------------
    st.markdown("## Business Value of the Project")

    v1, v2, v3 = st.columns(3)

    with v1:
        info_box(
            "Retention Decision Support",
            """
            Helps HR teams spot high-risk employees early and take preventive action
            instead of reacting only after attrition happens.
            """,
            "🛡️"
        )

    with v2:
        info_box(
            "Faster Hiring Evaluation",
            """
            Reduces manual effort in resume screening by automatically checking
            candidate fit against role requirements and generating a recruiter summary.
            """,
            "⚡"
        )

    with v3:
        info_box(
            "AI-Powered HR Insights",
            """
            Combines predictive modeling with LLM-based explanation, making outputs
            easier for non-technical HR stakeholders to understand and act on.
            """,
            "💡"
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    st.caption("Developed by Rudra Sharad Mhaske")