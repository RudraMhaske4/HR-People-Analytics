import streamlit as st
import pandas as pd
import os
import tempfile
import plotly.graph_objects as go
import google.generativeai as genai
from dotenv import load_dotenv

from src.resume_backend import (
    score_candidate,
    build_candidate_score_dataframe,
    generate_candidate_report
)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_FOLDER = BASE_DIR / "reports" / "resume_reports"

CANDIDATE_SCORES_PATH = REPORTS_FOLDER / "candidate_scores.csv"
CANDIDATE_REPORT_PATH = REPORTS_FOLDER / "candidate_report_advanced.txt"

# =========================================================
# PATHS
# =========================================================
REPORTS_FOLDER = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\resume_reports"
CANDIDATE_SCORES_PATH = os.path.join(REPORTS_FOLDER, "candidate_scores.csv")
CANDIDATE_REPORT_PATH = os.path.join(REPORTS_FOLDER, "candidate_report_advanced.txt")


# =========================================================
# DEFAULT JD + SKILLS
# =========================================================
DEFAULT_JOB_DESCRIPTION = """
We are hiring an AI/ML Engineer with strong knowledge of Python, machine learning, deep learning,
data analysis, NLP, scikit-learn, pandas, numpy, SQL, and model deployment.
Candidates with project experience in predictive analytics, dashboards, Streamlit, LLMs,
and business problem solving will be preferred.
Minimum education: Bachelor's degree in Computer Science, Artificial Intelligence, Data Science,
or a related field.
"""

DEFAULT_SKILL_LIST = [
    "python",
    "machine learning",
    "deep learning",
    "data analysis",
    "nlp",
    "natural language processing",
    "scikit-learn",
    "pandas",
    "numpy",
    "sql",
    "streamlit",
    "llm",
    "transformers",
    "tensorflow",
    "pytorch",
    "power bi",
    "excel",
    "data visualization",
    "predictive analytics",
    "model deployment",
    "dashboard",
    "statistics",
    "eda",
    "feature engineering"
]


# =========================================================
# FILE READING HELPERS
# =========================================================
def extract_text_from_pdf(pdf_path):
    try:
        import PyPDF2
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"PDF_READ_ERROR: {str(e)}"


def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception as e:
        return f"TXT_READ_ERROR: {str(e)}"


def upload_new_resume():
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF or TXT)",
        type=["pdf", "txt"],
        key="premium_resume_upload"
    )

    if uploaded_file is None:
        return None, None

    suffix = os.path.splitext(uploaded_file.name)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        temp_path = tmp_file.name

    if suffix == ".pdf":
        resume_text = extract_text_from_pdf(temp_path)
    elif suffix == ".txt":
        resume_text = extract_text_from_txt(temp_path)
    else:
        return None, None

    if resume_text.startswith("PDF_READ_ERROR") or resume_text.startswith("TXT_READ_ERROR"):
        st.error(f"Could not read uploaded resume.\n\n{resume_text}")
        return None, None

    if not resume_text.strip():
        st.error("Uploaded resume is empty after extraction.")
        return None, None

    return resume_text, uploaded_file.name


# =========================================================
# GEMINI LOADER
# =========================================================
def load_gemini_model():
    try:
        load_dotenv(r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\.env")
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return None

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        return model
    except Exception:
        return None


# =========================================================
# PREMIUM UI HELPERS
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
            min-height: 145px;
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


def render_gauge(score):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Overall Match Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#7C3AED"},
                "steps": [
                    {"range": [0, 40], "color": "#3f1d1d"},
                    {"range": [40, 70], "color": "#3d2c12"},
                    {"range": [70, 100], "color": "#123524"},
                ],
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F8FAFC"},
        margin=dict(l=10, r=10, t=40, b=10),
        height=340,
    )

    st.plotly_chart(fig, use_container_width=True, key="premium_resume_gauge")


# =========================================================
# RESULTS RENDERER
# =========================================================
def render_candidate_results(candidate_scores_df, candidate_report):
    if candidate_scores_df.empty:
        st.warning("Candidate score data is empty.")
        return

    row = candidate_scores_df.iloc[0]

    st.markdown("## Candidate Match Intelligence")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        premium_card(
            "Skill Match",
            f"{row['Skill Match Score']}%",
            "Match between resume skills and JD skills",
            "#7C3AED",
            "#2563EB"
        )

    with c2:
        premium_card(
            "Experience Match",
            f"{row['Experience Match Score']}%",
            "Resume experience vs JD expectation",
            "#2563EB",
            "#06B6D4"
        )

    with c3:
        premium_card(
            "Education Match",
            f"{row['Education Match Score']}%",
            "Education fit for the target role",
            "#059669",
            "#10B981"
        )

    with c4:
        premium_card(
            "Overall Match",
            f"{row['Overall Match Score']}%",
            "Weighted candidate suitability score",
            "#DC2626",
            "#F97316"
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown("### Match Score Overview")
        render_gauge(float(row["Overall Match Score"]))

    with right:
        info_panel(
            "Matched Skills",
            row["Matched Skills"] if str(row["Matched Skills"]).strip() else "No matched skills found.",
            emoji="✅",
            bg="rgba(16,185,129,0.10)",
            border="rgba(16,185,129,0.22)"
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        info_panel(
            "Missing Skills",
            row["Missing Skills"] if str(row["Missing Skills"]).strip() else "No missing skills found.",
            emoji="⚠️",
            bg="rgba(239,68,68,0.10)",
            border="rgba(239,68,68,0.22)"
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        info_panel(
            "Candidate Profile",
            f"""
            <b>Experience:</b> {row['Candidate Experience']} years<br>
            <b>Education:</b> {row['Candidate Education']}
            """,
            emoji="👤",
            bg="rgba(59,130,246,0.10)",
            border="rgba(59,130,246,0.22)"
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    st.markdown("## Candidate Score Breakdown")
    ranked_df = candidate_scores_df.copy().sort_values("Overall Match Score", ascending=False)
    ranked_df["Rank"] = range(1, len(ranked_df) + 1)
    st.dataframe(ranked_df, use_container_width=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    st.markdown("## AI Recruiter Report")
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 22px;
            line-height: 1.8;
            color: #E2E8F0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        ">
            {candidate_report}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.download_button(
        label="Download Candidate Report",
        data=candidate_report,
        file_name="candidate_report.txt",
        mime="text/plain"
    )


# =========================================================
# MAIN PAGE
# =========================================================
def show_resume_screening():
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
            🎯 Resume Screening & Candidate Evaluation
        </div>
        <div style="font-size: 1rem; color: #CBD5E1; line-height: 1.8; max-width: 1100px;">
            Upload a resume, compare it against a job description, evaluate skill / experience / education fit,
            and generate an AI recruiter-style candidate assessment report.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # Upload + JD configuration
    # -----------------------------------------------------
    st.markdown("## Upload & Configure Candidate Evaluation")

    left, right = st.columns([1, 1.25])

    with left:
        st.markdown("### Resume Upload")
        resume_text, uploaded_filename = upload_new_resume()

        candidate_name = st.text_input("Candidate Name", value="Candidate")

        if uploaded_filename:
            st.success(f"Uploaded: {uploaded_filename}")

        st.caption(
            "Supported formats: PDF and TXT. "
            "The uploaded resume will be parsed and matched against the job description."
        )

    with right:
        st.markdown("### Job Configuration")

        job_description = st.text_area(
            "Job Description",
            value=DEFAULT_JOB_DESCRIPTION,
            height=220
        )

        use_default_skills = st.checkbox(
            "Use default AI/ML skill list",
            value=True
        )

        custom_skill_input = ""
        if not use_default_skills:
            custom_skill_input = st.text_area(
                "Enter comma-separated skills",
                value="python, machine learning, sql, pandas, numpy, streamlit"
            )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    action_col1, action_col2 = st.columns([0.28, 0.72])
    with action_col1:
        analyze_clicked = st.button("Analyze Resume", use_container_width=True)

    # -----------------------------------------------------
    # Analyze uploaded resume
    # -----------------------------------------------------
    if analyze_clicked:
        if resume_text is None:
            st.warning("Please upload a resume first.")
        else:
            if use_default_skills:
                skill_list = DEFAULT_SKILL_LIST
            else:
                skill_list = [s.strip() for s in custom_skill_input.split(",") if s.strip()]

            with st.spinner("Analyzing resume and generating recruiter insights..."):
                model = load_gemini_model()

                score_result = score_candidate(
                    resume_text=resume_text,
                    job_description=job_description,
                    skill_list=skill_list
                )

                candidate_scores_df = build_candidate_score_dataframe(score_result)

                candidate_report = generate_candidate_report(
                    candidate_name=candidate_name,
                    resume_text=resume_text,
                    job_description=job_description,
                    score_result=score_result,
                    model=model
                )

                os.makedirs(REPORTS_FOLDER, exist_ok=True)
                candidate_scores_df.to_csv(CANDIDATE_SCORES_PATH, index=False)

                with open(CANDIDATE_REPORT_PATH, "w", encoding="utf-8") as f:
                    f.write(candidate_report)

            st.success("Resume analyzed successfully. Candidate evaluation updated.")
            st.rerun()

    # -----------------------------------------------------
    # Latest saved evaluation
    # -----------------------------------------------------
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("## Latest Saved Candidate Evaluation")

    if os.path.exists(CANDIDATE_SCORES_PATH) and os.path.exists(CANDIDATE_REPORT_PATH):
        candidate_scores_df = pd.read_csv(CANDIDATE_SCORES_PATH)

        with open(CANDIDATE_REPORT_PATH, "r", encoding="utf-8") as f:
            candidate_report = f.read()

        render_candidate_results(candidate_scores_df, candidate_report)
    else:
        st.info("No saved candidate evaluation found yet. Upload a resume above to generate one.")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.caption("Developed by Rudra Sharad Mhaske")