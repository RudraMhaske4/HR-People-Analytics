import streamlit as st
import pandas as pd
import os
import plotly.express as px

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"

HIGH_RISK_PATH = REPORTS_DIR / "high_risk_employees.csv"

# =========================================
# Paths
# =========================================
HIGH_RISK_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\reports\high_risk_employees.csv"


# =========================================
# UI Helpers
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


def insight_box(title, body, emoji="📌", bg="rgba(255,255,255,0.03)", border="rgba(255,255,255,0.08)"):
    st.markdown(
        f"""
        <div style="
            background: {bg};
            border: 1px solid {border};
            border-radius: 18px;
            padding: 20px;
            min-height: 165px;
        ">
            <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin-bottom: 10px;">
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
# Main Page
# =========================================
def show_executive_summary():
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
            📊 Executive Summary
        </div>
        <div style="font-size: 1rem; color: #CBD5E1; line-height: 1.8; max-width: 1050px;">
            Leadership-focused overview of employee attrition risk signals, department concentration,
            workforce stability indicators, and recommended intervention priorities.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------
    # Load data
    # -------------------------------------
    if not os.path.exists(HIGH_RISK_PATH):
        st.error("High-risk employee file not found. Please generate the attrition outputs first.")
        return

    df = pd.read_csv(HIGH_RISK_PATH)

    if df.empty:
        st.warning("High-risk employee dataset is empty.")
        return

    # -------------------------------------
    # Safe column handling
    # -------------------------------------
    total_high_risk = len(df)

    avg_risk = None
    if "Risk Probability" in df.columns:
        try:
            avg_risk = round(df["Risk Probability"].mean() * 100, 2)
        except:
            avg_risk = None

    top_department = "N/A"
    if "Department" in df.columns and not df["Department"].dropna().empty:
        top_department = df["Department"].mode()[0]

    top_risk_level = "N/A"
    if "Risk Level" in df.columns and not df["Risk Level"].dropna().empty:
        top_risk_level = df["Risk Level"].mode()[0]

    overtime_pct = None
    if "OverTime" in df.columns:
        try:
            overtime_yes = (df["OverTime"].astype(str).str.lower() == "yes").sum()
            overtime_pct = round((overtime_yes / len(df)) * 100, 2)
        except:
            overtime_pct = None

    # -------------------------------------
    # KPI Cards
    # -------------------------------------
    st.markdown("## Leadership Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        premium_card(
            "High-Risk Employees",
            total_high_risk,
            "Employees currently present in the high-risk attrition output",
            "#DC2626",
            "#F97316"
        )

    with c2:
        premium_card(
            "Average Attrition Risk",
            f"{avg_risk}%" if avg_risk is not None else "N/A",
            "Mean predicted risk across high-risk employee group",
            "#7C3AED",
            "#2563EB"
        )

    with c3:
        premium_card(
            "Top Risk Department",
            top_department,
            "Department with the highest concentration in the high-risk group",
            "#2563EB",
            "#06B6D4"
        )

    with c4:
        premium_card(
            "Overtime Exposure",
            f"{overtime_pct}%" if overtime_pct is not None else "N/A",
            "Share of high-risk employees currently working overtime",
            "#059669",
            "#10B981"
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # -------------------------------------
    # Executive narrative
    # -------------------------------------
    st.markdown("## Executive Interpretation")

    narrative_col1, narrative_col2 = st.columns([1.25, 1])

    with narrative_col1:
        st.markdown(
            f"""
            <div style="
                background: rgba(255,255,255,0.03);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 20px;
                padding: 22px;
                line-height: 1.85;
                color: #CBD5E1;
                font-size: 0.98rem;
                min-height: 320px;
            ">
                The current attrition-risk pipeline has identified <b>{total_high_risk}</b> employees in the high-risk cohort.
                {"The average predicted attrition risk across this group is <b>" + str(avg_risk) + "%</b>." if avg_risk is not None else ""}
                <br><br>
                The concentration of risk appears strongest in <b>{top_department}</b>, suggesting that this department may require
                closer managerial review, retention-focused intervention, or workforce policy adjustments.
                <br><br>
                {"Additionally, <b>" + str(overtime_pct) + "%</b> of the high-risk group is currently associated with overtime exposure, which may indicate workload pressure or work-life balance stress." if overtime_pct is not None else ""}
                <br><br>
                From a leadership perspective, this page should be read as an <b>early warning layer</b> rather than a final HR decision engine.
                The goal is to identify where targeted HR action, manager conversations, compensation review, or engagement efforts
                may produce the strongest retention impact.
            </div>
            """,
            unsafe_allow_html=True
        )

    with narrative_col2:
        insight_box(
            "Top Risk Signals",
            f"""
            • High-risk employee count is currently <b>{total_high_risk}</b>.<br><br>
            • Dominant risk concentration appears in <b>{top_department}</b>.<br><br>
            • Most common risk level observed: <b>{top_risk_level}</b>.<br><br>
            • {"Overtime is present in <b>" + str(overtime_pct) + "%</b> of high-risk cases." if overtime_pct is not None else "Overtime signal not available in the current file."}
            """,
            emoji="🚨",
            bg="rgba(239,68,68,0.10)",
            border="rgba(239,68,68,0.20)"
        )

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

        insight_box(
            "Leadership Priority",
            """
            Focus first on <b>department-level hotspots</b>, then validate the underlying causes through
            manager review, employee engagement patterns, overtime pressure, role-specific dissatisfaction,
            and compensation or progression concerns.
            """,
            emoji="🎯",
            bg="rgba(59,130,246,0.10)",
            border="rgba(59,130,246,0.20)"
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # -------------------------------------
    # Department concentration chart
    # -------------------------------------
    if "Department" in df.columns and not df["Department"].dropna().empty:
        st.markdown("## Department Risk Concentration")

        dept_counts = df["Department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Count"]

        fig = px.bar(
            dept_counts,
            x="Department",
            y="Count",
            text="Count",
            color="Count",
            color_continuous_scale="purples",
            title="High-Risk Employee Count by Department"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"),
            title_font=dict(size=18),
            xaxis_title="Department",
            yaxis_title="High-Risk Employees",
            margin=dict(l=20, r=20, t=50, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------
    # Risk level distribution
    # -------------------------------------
    if "Risk Level" in df.columns and not df["Risk Level"].dropna().empty:
        st.markdown("## Risk Level Distribution")

        risk_counts = df["Risk Level"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Count"]

        fig2 = px.pie(
            risk_counts,
            names="Risk Level",
            values="Count",
            title="Distribution of High-Risk Employees by Risk Level",
            hole=0.45
        )

        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"),
            margin=dict(l=20, r=20, t=50, b=20)
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # -------------------------------------
    # Action recommendations
    # -------------------------------------
    st.markdown("## Recommended Executive Actions")

    a1, a2, a3 = st.columns(3)

    with a1:
        insight_box(
            "Prioritize Department Review",
            """
            Start with the department showing the highest high-risk concentration.
            Review role structures, manager load, workload intensity, and turnover history.
            """,
            emoji="🏢",
            bg="rgba(124,58,237,0.10)",
            border="rgba(124,58,237,0.22)"
        )

    with a2:
        insight_box(
            "Investigate Overtime Pressure",
            """
            If overtime exposure is common in the high-risk group, assess whether workload imbalance,
            burnout, or schedule pressure may be driving disengagement.
            """,
            emoji="⏱️",
            bg="rgba(245,158,11,0.10)",
            border="rgba(245,158,11,0.22)"
        )

    with a3:
        insight_box(
            "Use AI Reports for Intervention",
            """
            Move from department-level summary to employee-level AI reports to identify
            which specific individuals require immediate retention action or HR follow-up.
            """,
            emoji="🤖",
            bg="rgba(16,185,129,0.10)",
            border="rgba(16,185,129,0.22)"
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.caption("Developed by Rudra Sharad Mhaske")