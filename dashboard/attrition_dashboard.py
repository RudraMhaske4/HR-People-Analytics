import streamlit as st
import pandas as pd
import os
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

ATTRITION_DATA_PATH = DATA_DIR / "employee_attrition.csv"
HIGH_RISK_PATH = REPORTS_DIR / "high_risk_employees.csv"

# =========================================
# Paths
# =========================================
ATTRITION_DATA_PATH = r"C:\Users\hp\Desktop\Projects\HR-People-Analytics\data\employee_attrition.csv"
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


def section_box(title, body, emoji="📌"):
    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px 20px;
            min-height: 145px;
        ">
            <div style="font-size: 1.02rem; font-weight: 700; color: #F8FAFC; margin-bottom: 10px;">
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
def show_attrition_dashboard():
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
            📉 Attrition Dashboard
        </div>
        <div style="font-size: 1rem; color: #CBD5E1; line-height: 1.8; max-width: 1100px;">
            Interactive workforce attrition analytics dashboard for monitoring employee risk,
            understanding department-level patterns, and identifying operational signals
            linked to turnover.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------
    # Load data
    # -------------------------------------
    if not os.path.exists(ATTRITION_DATA_PATH):
        st.error("employee_attrition.csv not found in data folder.")
        return

    df = pd.read_csv(ATTRITION_DATA_PATH)

    if df.empty:
        st.warning("Attrition dataset is empty.")
        return

    high_risk_df = None
    if os.path.exists(HIGH_RISK_PATH):
        try:
            high_risk_df = pd.read_csv(HIGH_RISK_PATH)
        except:
            high_risk_df = None

    # -------------------------------------
    # Filters
    # -------------------------------------
    st.markdown("## Dashboard Filters")

    f1, f2, f3 = st.columns(3)

    # Department filter
    departments = ["All"]
    if "Department" in df.columns:
        departments += sorted(df["Department"].dropna().astype(str).unique().tolist())

    with f1:
        selected_department = st.selectbox("Department", departments)

    # Attrition filter
    attrition_options = ["All"]
    if "Attrition" in df.columns:
        attrition_options += sorted(df["Attrition"].dropna().astype(str).unique().tolist())

    with f2:
        selected_attrition = st.selectbox("Attrition", attrition_options)

    # Overtime filter
    overtime_options = ["All"]
    if "OverTime" in df.columns:
        overtime_options += sorted(df["OverTime"].dropna().astype(str).unique().tolist())

    with f3:
        selected_overtime = st.selectbox("OverTime", overtime_options)

    filtered_df = df.copy()

    if selected_department != "All" and "Department" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Department"].astype(str) == selected_department]

    if selected_attrition != "All" and "Attrition" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Attrition"].astype(str) == selected_attrition]

    if selected_overtime != "All" and "OverTime" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["OverTime"].astype(str) == selected_overtime]

    # -------------------------------------
    # KPI calculations
    # -------------------------------------
    total_employees = len(filtered_df)

    attrition_count = None
    if "Attrition" in filtered_df.columns:
        attrition_count = int((filtered_df["Attrition"].astype(str).str.lower() == "yes").sum())

    attrition_rate = None
    if attrition_count is not None and total_employees > 0:
        attrition_rate = round((attrition_count / total_employees) * 100, 2)

    avg_income = None
    if "MonthlyIncome" in filtered_df.columns:
        try:
            avg_income = round(filtered_df["MonthlyIncome"].mean(), 2)
        except:
            avg_income = None

    avg_age = None
    if "Age" in filtered_df.columns:
        try:
            avg_age = round(filtered_df["Age"].mean(), 1)
        except:
            avg_age = None

    # -------------------------------------
    # KPI strip
    # -------------------------------------
    st.markdown("## Workforce Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        premium_card(
            "Employees in View",
            total_employees,
            "Employees after applying dashboard filters",
            "#7C3AED",
            "#2563EB"
        )

    with c2:
        premium_card(
            "Attrition Cases",
            attrition_count if attrition_count is not None else "N/A",
            "Employees marked with attrition = Yes",
            "#DC2626",
            "#F97316"
        )

    with c3:
        premium_card(
            "Attrition Rate",
            f"{attrition_rate}%" if attrition_rate is not None else "N/A",
            "Share of employees in the filtered view with attrition = Yes",
            "#2563EB",
            "#06B6D4"
        )

    with c4:
        premium_card(
            "Average Monthly Income",
            f"{avg_income}" if avg_income is not None else "N/A",
            "Mean monthly income in the filtered employee group",
            "#059669",
            "#10B981"
        )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # -------------------------------------
    # Analytics charts row 1
    # -------------------------------------
    st.markdown("## Attrition Analysis")

    chart1, chart2 = st.columns(2)

    with chart1:
        if "Department" in filtered_df.columns:
            dept_attr = filtered_df.groupby("Department").size().reset_index(name="Count")

            fig1 = px.bar(
                dept_attr,
                x="Department",
                y="Count",
                color="Count",
                color_continuous_scale="purples",
                title="Employees by Department"
            )

            fig1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F8FAFC"),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig1, use_container_width=True)

    with chart2:
        if "JobRole" in filtered_df.columns:
            role_attr = filtered_df.groupby("JobRole").size().reset_index(name="Count")

            fig2 = px.bar(
                role_attr,
                x="JobRole",
                y="Count",
                color="Count",
                color_continuous_scale="blues",
                title="Employees by Job Role"
            )

            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F8FAFC"),
                xaxis_tickangle=-25,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------------
    # Analytics charts row 2
    # -------------------------------------
    chart3, chart4 = st.columns(2)

    with chart3:
        if "OverTime" in filtered_df.columns:
            overtime_counts = filtered_df["OverTime"].value_counts().reset_index()
            overtime_counts.columns = ["OverTime", "Count"]

            fig3 = px.pie(
                overtime_counts,
                names="OverTime",
                values="Count",
                hole=0.45,
                title="OverTime Distribution"
            )

            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F8FAFC"),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig3, use_container_width=True)

    with chart4:
        if "Attrition" in filtered_df.columns:
            attrition_counts = filtered_df["Attrition"].value_counts().reset_index()
            attrition_counts.columns = ["Attrition", "Count"]

            fig4 = px.pie(
                attrition_counts,
                names="Attrition",
                values="Count",
                hole=0.45,
                title="Attrition Distribution"
            )

            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#F8FAFC"),
                margin=dict(l=20, r=20, t=50, b=20)
            )
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # -------------------------------------
    # Insights / interpretation
    # -------------------------------------
    st.markdown("## Attrition Interpretation")

    i1, i2, i3 = st.columns(3)

    with i1:
        section_box(
            "Department Lens",
            """
            Use department-wise employee concentration and attrition patterns to identify
            which business units may require deeper retention review, workload balancing,
            or manager-level intervention.
            """,
            "🏢"
        )

    with i2:
        section_box(
            "Role Lens",
            """
            Job role analysis helps identify whether attrition pressure is concentrated
            in specific functions, specialist roles, or operational positions.
            """,
            "💼"
        )

    with i3:
        section_box(
            "Workload Lens",
            """
            Overtime and attrition together can indicate workload pressure or burnout.
            This can be useful for spotting retention risk linked to work intensity.
            """,
            "⏱️"
        )

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # -------------------------------------
    # High-risk employee table
    # -------------------------------------
    st.markdown("## High-Risk Employee Table")

    if high_risk_df is not None and not high_risk_df.empty:
        display_cols = high_risk_df.columns.tolist()

        # If department filter applied and column exists, filter table too
        hr_filtered = high_risk_df.copy()
        if selected_department != "All" and "Department" in hr_filtered.columns:
            hr_filtered = hr_filtered[hr_filtered["Department"].astype(str) == selected_department]

        st.dataframe(hr_filtered[display_cols], use_container_width=True)

        csv_data = hr_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download High-Risk Employee Table",
            data=csv_data,
            file_name="high_risk_employees_filtered.csv",
            mime="text/csv"
        )
    else:
        st.info("High-risk employee output not found yet.")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.caption("Developed by Rudra Sharad Mhaske")