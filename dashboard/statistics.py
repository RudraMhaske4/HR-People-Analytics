import streamlit as st
import pandas as pd
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

ATTRITION_DATA_PATH = DATA_DIR / "employee_attrition.csv"
HIGH_RISK_PATH = REPORTS_DIR / "high_risk_employees.csv"
EMPLOYEE_REPORTS_FOLDER = REPORTS_DIR / "employee_reports"
RESUME_REPORTS_FOLDER = REPORTS_DIR / "resume_reports"
CANDIDATE_SCORES_PATH = RESUME_REPORTS_FOLDER / "candidate_scores.csv"
CANDIDATE_REPORT_PATH = RESUME_REPORTS_FOLDER / "candidate_report_advanced.txt"

# =========================================================
# PATHS
# =========================================================
ATTRITION_DATA_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\data\employee_attrition.csv"
HIGH_RISK_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\high_risk_employees.csv"
EMPLOYEE_REPORTS_FOLDER = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\employee_reports"
RESUME_REPORTS_FOLDER = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\resume_reports"
CANDIDATE_SCORES_PATH = os.path.join(RESUME_REPORTS_FOLDER, "candidate_scores.csv")
CANDIDATE_REPORT_PATH = os.path.join(RESUME_REPORTS_FOLDER, "candidate_report_advanced.txt")


# =========================================================
# UI HELPERS
# =========================================================
def premium_card(title, value, subtitle="", color1="#7C3AED", color2="#2563EB"):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color1}22, {color2}18);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px 20px;
            min-height: 120px;
            box-shadow: 0 10px 24px rgba(0,0,0,0.16);
        ">
            <div style="font-size: 0.95rem; color: #CBD5E1; margin-bottom: 8px;">{title}</div>
            <div style="font-size: 2rem; font-weight: 800; color: #F8FAFC;">{value}</div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 8px; line-height: 1.5;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def info_panel(title, body, emoji="📌", bg="rgba(255,255,255,0.03)", border="rgba(255,255,255,0.08)"):
    st.markdown(
        f"""
        <div style="
            background: {bg};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 18px;
            min-height: 155px;
        ">
            <div style="font-size: 1rem; font-weight: 700; color: #F8FAFC; margin-bottom: 10px;">
                {emoji} {title}
            </div>
            <div style="color: #CBD5E1; line-height: 1.7; font-size: 0.95rem;">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HELPERS
# =========================================================
def count_txt_files(folder_path):
    if not os.path.exists(folder_path):
        return 0
    return len([f for f in os.listdir(folder_path) if f.endswith(".txt")])


def file_exists(path):
    return "Yes" if os.path.exists(path) else "No"


# =========================================================
# MAIN PAGE
# =========================================================
def show_project_statistics():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(124,58,237,0.20), rgba(37,99,235,0.12));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 26px 28px;
        margin-bottom: 22px;
        box-shadow: 0 12px 32px rgba(0,0,0,0.18);
    ">
        <div style="font-size: 2.2rem; font-weight: 800; color: #F8FAFC; margin-bottom: 10px;">
            📈 Project Statistics
        </div>
        <div style="font-size: 1rem; color: #CBD5E1; line-height: 1.8; max-width: 1100px;">
            Technical and operational overview of the HR Analytics AI project including
            dataset scale, generated reports, candidate evaluation outputs, and project module coverage.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # Load dataset stats
    # -----------------------------------------------------
    total_employees = "N/A"
    total_columns = "N/A"
    attrition_yes_count = "N/A"

    if os.path.exists(ATTRITION_DATA_PATH):
        try:
            df = pd.read_csv(ATTRITION_DATA_PATH)
            total_employees = len(df)
            total_columns = len(df.columns)

            if "Attrition" in df.columns:
                attrition_yes_count = int((df["Attrition"].astype(str).str.lower() == "yes").sum())
        except:
            pass

    high_risk_count = "N/A"
    if os.path.exists(HIGH_RISK_PATH):
        try:
            risk_df = pd.read_csv(HIGH_RISK_PATH)
            high_risk_count = len(risk_df)
        except:
            pass

    employee_report_count = count_txt_files(EMPLOYEE_REPORTS_FOLDER)
    resume_report_count = count_txt_files(RESUME_REPORTS_FOLDER)

    candidate_match_score = "N/A"
    if os.path.exists(CANDIDATE_SCORES_PATH):
        try:
            cand_df = pd.read_csv(CANDIDATE_SCORES_PATH)
            if not cand_df.empty and "Overall Match Score" in cand_df.columns:
                candidate_match_score = f"{cand_df.iloc[0]['Overall Match Score']}%"
        except:
            pass

    # -----------------------------------------------------
    # KPI STRIP
    # -----------------------------------------------------
    st.markdown("## Project Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        premium_card(
            "Employee Records",
            total_employees,
            "Total employee rows available in the attrition dataset",
            "#7C3AED",
            "#2563EB"
        )

    with c2:
        premium_card(
            "High-Risk Employees",
            high_risk_count,
            "Employees present in the generated high-risk attrition output",
            "#DC2626",
            "#F97316"
        )

    with c3:
        premium_card(
            "Employee AI Reports",
            employee_report_count,
            "Individual employee risk reports generated by the LLM layer",
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

    # -----------------------------------------------------
    # DATASET + OUTPUT OVERVIEW
    # -----------------------------------------------------
    st.markdown("## Dataset & Output Overview")

    d1, d2, d3 = st.columns(3)

    with d1:
        info_panel(
            "Employee Attrition Dataset",
            f"""
            <b>Dataset File Present:</b> {file_exists(ATTRITION_DATA_PATH)}<br>
            <b>Total Employee Rows:</b> {total_employees}<br>
            <b>Total Columns:</b> {total_columns}<br>
            <b>Attrition = Yes Count:</b> {attrition_yes_count}
            """,
            emoji="🗂️",
            bg="rgba(59,130,246,0.10)",
            border="rgba(59,130,246,0.22)"
        )

    with d2:
        info_panel(
            "Generated Attrition Outputs",
            f"""
            <b>High-Risk File Present:</b> {file_exists(HIGH_RISK_PATH)}<br>
            <b>High-Risk Employee Count:</b> {high_risk_count}<br>
            <b>Employee Report Files:</b> {employee_report_count}
            """,
            emoji="📉",
            bg="rgba(239,68,68,0.10)",
            border="rgba(239,68,68,0.22)"
        )

    with d3:
        info_panel(
            "Resume Screening Outputs",
            f"""
            <b>Candidate Scores File Present:</b> {file_exists(CANDIDATE_SCORES_PATH)}<br>
            <b>Candidate Recruiter Report Present:</b> {file_exists(CANDIDATE_REPORT_PATH)}<br>
            <b>Resume Report Text Files:</b> {resume_report_count}<br>
            <b>Latest Candidate Match Score:</b> {candidate_match_score}
            """,
            emoji="🎯",
            bg="rgba(16,185,129,0.10)",
            border="rgba(16,185,129,0.22)"
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # MODULE COVERAGE
    # -----------------------------------------------------
    st.markdown("## Project Module Coverage")

    m1, m2 = st.columns(2)

    with m1:
        info_panel(
            "Core Functional Modules",
            """
            <b>1. Attrition Dashboard</b> — workforce attrition analytics, filters, charts, and high-risk views.<br><br>
            <b>2. Executive Summary</b> — leadership-facing risk summary and department concentration analysis.<br><br>
            <b>3. Employee Reports</b> — employee-level AI-generated HR risk reports and metadata review.
            """,
            emoji="🧠",
            bg="rgba(124,58,237,0.10)",
            border="rgba(124,58,237,0.22)"
        )

    with m2:
        info_panel(
            "AI & Hiring Modules",
            """
            <b>4. Resume Screening</b> — candidate-job fit scoring using skill, experience, and education matching.<br><br>
            <b>5. HR Copilot Chatbot</b> — Gemini-powered HR assistant for analytics interpretation and decision support.<br><br>
            <b>6. Project Statistics</b> — technical and operational overview of project assets, outputs, and system coverage.
            """,
            emoji="🤖",
            bg="rgba(37,99,235,0.10)",
            border="rgba(37,99,235,0.22)"
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # TECH STACK
    # -----------------------------------------------------
    st.markdown("## Technical Stack Overview")

    t1, t2, t3 = st.columns(3)

    with t1:
        info_panel(
            "Data & Analytics Stack",
            """
            • Python<br>
            • Pandas<br>
            • NumPy<br>
            • Plotly<br>
            • Streamlit
            """,
            emoji="📊",
            bg="rgba(255,255,255,0.03)",
            border="rgba(255,255,255,0.08)"
        )

    with t2:
        info_panel(
            "Machine Learning & Prediction",
            """
            • Attrition risk modeling<br>
            • Employee-level risk segmentation<br>
            • Candidate-job fit scoring logic<br>
            • Predictive HR analytics workflow
            """,
            emoji="⚙️",
            bg="rgba(255,255,255,0.03)",
            border="rgba(255,255,255,0.08)"
        )

    with t3:
        info_panel(
            "LLM / AI Layer",
            """
            • Gemini API<br>
            • AI-generated employee reports<br>
            • AI recruiter-style candidate reports<br>
            • HR Copilot chatbot for decision support
            """,
            emoji="✨",
            bg="rgba(255,255,255,0.03)",
            border="rgba(255,255,255,0.08)"
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # PROJECT HEALTH / COMPLETION VIEW
    # -----------------------------------------------------
    st.markdown("## Project Health Overview")

    h1, h2, h3 = st.columns(3)

    with h1:
        info_panel(
            "Data Layer Status",
            f"""
            <b>Employee Dataset:</b> {file_exists(ATTRITION_DATA_PATH)}<br>
            <b>High-Risk Output:</b> {file_exists(HIGH_RISK_PATH)}<br>
            <b>Dataset Columns Tracked:</b> {total_columns}
            """,
            emoji="🗃️",
            bg="rgba(59,130,246,0.10)",
            border="rgba(59,130,246,0.22)"
        )

    with h2:
        info_panel(
            "AI Output Status",
            f"""
            <b>Employee Reports Generated:</b> {employee_report_count}<br>
            <b>Candidate Score File:</b> {file_exists(CANDIDATE_SCORES_PATH)}<br>
            <b>Candidate Recruiter Report:</b> {file_exists(CANDIDATE_REPORT_PATH)}
            """,
            emoji="📝",
            bg="rgba(16,185,129,0.10)",
            border="rgba(16,185,129,0.22)"
        )

    with h3:
        info_panel(
            "Dashboard Readiness",
            """
            <b>Implemented Pages:</b> Home, Executive Summary, Attrition Dashboard,
            Employee Reports, Resume Screening, HR Copilot Chatbot, Project Statistics.<br><br>
            <b>Status:</b> Premium multi-page HR Analytics AI dashboard completed.
            """,
            emoji="🚀",
            bg="rgba(124,58,237,0.10)",
            border="rgba(124,58,237,0.22)"
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.caption("Developed by Rudra Sharad Mhaske")