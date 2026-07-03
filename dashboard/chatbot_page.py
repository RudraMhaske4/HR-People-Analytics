import streamlit as st
import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

ATTRITION_DATA_PATH = DATA_DIR / "employee_attrition.csv"
HIGH_RISK_PATH = REPORTS_DIR / "high_risk_employees.csv"
CANDIDATE_SCORES_PATH = REPORTS_DIR / "resume_reports" / "candidate_scores.csv"
CANDIDATE_REPORT_PATH = REPORTS_DIR / "resume_reports" / "candidate_report_advanced.txt"

# =========================================================
# PATHS
# =========================================================
ATTRITION_DATA_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\data\employee_attrition.csv"
HIGH_RISK_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\high_risk_employees.csv"
CANDIDATE_SCORES_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\resume_reports\candidate_scores.csv"
CANDIDATE_REPORT_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\resume_reports\candidate_report_advanced.txt"


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
        return genai.GenerativeModel("gemini-2.5-flash")
    except Exception:
        return None


# =========================================================
# LOAD PROJECT CONTEXT
# =========================================================
def load_project_context():
    context_parts = []

    # Attrition dataset summary
    if os.path.exists(ATTRITION_DATA_PATH):
        try:
            df = pd.read_csv(ATTRITION_DATA_PATH)
            context_parts.append(
                f"Employee attrition dataset loaded with {len(df)} rows and columns: {', '.join(df.columns[:20])}."
            )
        except Exception:
            pass

    # High-risk employee summary
    if os.path.exists(HIGH_RISK_PATH):
        try:
            risk_df = pd.read_csv(HIGH_RISK_PATH)
            context_parts.append(
                f"High-risk employee dataset loaded with {len(risk_df)} employees."
            )

            if "Department" in risk_df.columns:
                top_depts = risk_df["Department"].value_counts().head(5).to_dict()
                context_parts.append(f"Top high-risk departments: {top_depts}")

            if "Risk Level" in risk_df.columns:
                risk_levels = risk_df["Risk Level"].value_counts().to_dict()
                context_parts.append(f"Risk level distribution: {risk_levels}")
        except Exception:
            pass

    # Candidate score summary
    if os.path.exists(CANDIDATE_SCORES_PATH):
        try:
            cand_df = pd.read_csv(CANDIDATE_SCORES_PATH)
            if not cand_df.empty:
                row = cand_df.iloc[0].to_dict()
                context_parts.append(f"Latest candidate score summary: {row}")
        except Exception:
            pass

    # Candidate recruiter report
    if os.path.exists(CANDIDATE_REPORT_PATH):
        try:
            with open(CANDIDATE_REPORT_PATH, "r", encoding="utf-8") as f:
                candidate_report = f.read()
            context_parts.append(
                f"Latest candidate recruiter report:\n{candidate_report[:3000]}"
            )
        except Exception:
            pass

    if not context_parts:
        return "No project context files were found."

    return "\n\n".join(context_parts)


# =========================================================
# QUICK PROMPTS
# =========================================================
QUICK_PROMPTS = [
    "Summarize the current attrition risk situation in the company.",
    "Which departments appear to have the highest attrition risk and why?",
    "What HR actions would you recommend for high-risk employees?",
    "Summarize the latest candidate evaluation report.",
    "How can HR use this dashboard for retention and hiring decisions?"
]


# =========================================================
# PREMIUM CHAT UI HELPERS
# =========================================================
def render_user_message(message):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(124,58,237,0.20), rgba(37,99,235,0.12));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 14px 16px;
            margin-bottom: 12px;
            margin-left: 80px;
            color: #F8FAFC;
            line-height: 1.7;
        ">
            <b>You</b><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_bot_message(message):
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 16px 18px;
            margin-bottom: 14px;
            margin-right: 40px;
            color: #E2E8F0;
            line-height: 1.8;
            box-shadow: 0 10px 24px rgba(0,0,0,0.12);
        ">
            <b>HR Copilot</b><br>
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MAIN PAGE FUNCTION
# =========================================================
def show_chatbot_page():
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
            🤖 HR Copilot Chatbot
        </div>
        <div style="font-size: 1rem; color: #CBD5E1; line-height: 1.8; max-width: 1100px;">
            Ask questions about employee attrition risk, department-level workforce patterns,
            candidate evaluation results, and HR decision support insights from your dashboard.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # Session state for chat history
    # -----------------------------------------------------
    if "hr_chat_history" not in st.session_state:
        st.session_state.hr_chat_history = []

    # -----------------------------------------------------
    # Quick prompt buttons
    # -----------------------------------------------------
    st.markdown("## Quick HR Questions")
    q1, q2, q3, q4, q5 = st.columns(5)

    quick_prompt_clicked = None

    with q1:
        if st.button("Attrition Summary"):
            quick_prompt_clicked = QUICK_PROMPTS[0]

    with q2:
        if st.button("Risky Departments"):
            quick_prompt_clicked = QUICK_PROMPTS[1]

    with q3:
        if st.button("HR Actions"):
            quick_prompt_clicked = QUICK_PROMPTS[2]

    with q4:
        if st.button("Candidate Report"):
            quick_prompt_clicked = QUICK_PROMPTS[3]

    with q5:
        if st.button("Dashboard Use"):
            quick_prompt_clicked = QUICK_PROMPTS[4]

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -----------------------------------------------------
    # User input
    # -----------------------------------------------------
    st.markdown("## Ask HR Copilot")
    user_query = st.text_area(
        "Ask anything about employee attrition, candidate evaluation, HR actions, or dashboard insights",
        height=120,
        placeholder="Example: Which department seems to have the highest attrition risk and what should HR do next?"
    )

    ask_clicked = st.button("Ask HR Copilot", use_container_width=True)

    if quick_prompt_clicked:
        user_query = quick_prompt_clicked
        ask_clicked = True

    # -----------------------------------------------------
    # Generate answer
    # -----------------------------------------------------
    if ask_clicked:
        if not user_query.strip():
            st.warning("Please enter a question first.")
        else:
            model = load_gemini_model()

            if model is None:
                st.error("Gemini API key not found. Please check your .env file.")
            else:
                project_context = load_project_context()

                prompt = f"""
You are an expert HR Strategy Copilot working inside an LLM-Powered Predictive HR Analytics dashboard.

Your role:
- answer HR leadership and recruiter questions
- explain attrition risk patterns
- summarize candidate evaluation insights
- suggest practical HR actions
- answer in a professional, structured, business-friendly way

Use the project context below as your source of truth.

================ PROJECT CONTEXT ================
{project_context}
================================================

User Question:
{user_query}

Instructions:
- Give a clear HR-focused answer
- Use headings or bullet points when useful
- If the user asks for recommendations, give practical HR action steps
- If the data is insufficient, say what additional data would help
- Keep the tone professional and analytical
"""

                with st.spinner("HR Copilot is thinking..."):
                    try:
                        response = model.generate_content(prompt)
                        answer = response.text.strip()
                    except Exception as e:
                        answer = f"Error generating response: {str(e)}"

                st.session_state.hr_chat_history.append(("user", user_query))
                st.session_state.hr_chat_history.append(("bot", answer))

    # -----------------------------------------------------
    # Chat history
    # -----------------------------------------------------
    st.markdown("## Conversation")

    if not st.session_state.hr_chat_history:
        st.info("No conversation yet. Ask a question or use one of the quick HR prompts above.")
    else:
        for role, message in st.session_state.hr_chat_history:
            if role == "user":
                render_user_message(message)
            else:
                render_bot_message(message)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.caption("Developed by Rudra Sharad Mhaske")