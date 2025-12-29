import streamlit as st
import pandas as pd
import mysql.connector
import os
import psycopg2

# =======================
# PAGE CONFIG
# =======================
st.set_page_config(
    page_title="Operational KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# =======================
# GLOBAL STYLES (Creative UI)
# =======================
st.markdown("""
<style>
/* Background */
body {
    background: #e0e7ff;
    font-family: 'Segoe UI', sans-serif;
}

/* Glassmorphism header */
.header-box {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(10px);
    border-radius: 25px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 35px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    margin-bottom: 30px;
}
.header-box h1 {
    font-size: 48px;
    color: #1e3a8a;
    font-weight: 700;
}
.header-box p {
    font-size: 18px;
    color: #1f2937;
}

/* Glass card style */
.card {
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    background: linear-gradient(145deg, rgba(255,255,255,0.8), rgba(255,255,255,0.6));
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: all 0.3s ease-in-out;
}
.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}

/* KPI numbers */
.kpi-number {
    font-size: 32px;
    font-weight: 700;
    color: #1e40af;
}

/* Gradient divider */
.stDivider {
    border-top: 3px solid;
    border-image: linear-gradient(to right, #4f46e5, #3b82f6) 1;
}

/* Footer */
.footer {
    text-align: center;
    color: #1f2937;
    margin-top: 40px;
    font-size: 14px;
}
.footer hr {
    border: none;
    height: 3px;
    background: linear-gradient(to right, #4f46e5, #3b82f6);
    border-radius: 2px;
}
</style>
""", unsafe_allow_html=True)

# =======================
# CARD COMPONENT
# =======================
def card(title, content):
    st.markdown(
        f"""
        <div class="card">
            <h4>{title}</h4>
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

# =======================
# HEADER
# =======================
st.markdown(
    """
    <div class="header-box">
        <h1>📊 Operational KPI Dashboard</h1>
        <p>Automated Reporting & Performance Monitoring System</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# =======================
# MYSQL CONNECTION

# =====================================================
# MYSQL CONNECTION
# =====================================================

if os.getenv("RENDER") == "true":
    # 👉 Render / Production
    conn = psycopg2.connect(
        host="YOUR_SUPABASE_HOST",
        port=5432,
        database="YOUR_SUPABASE_DB",
        user="YOUR_SUPABASE_USER",
        password="YOUR_SUPABASE_PASSWORD"
    )

else:
    # 👉 Local PC
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lalit@282002",
        database="reporting_db"
    )


df = pd.read_sql("SELECT * FROM employee_kpis", conn)
df['date'] = pd.to_datetime(df['date'])

# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.header("🔎 Dashboard Filters")

employees = st.sidebar.multiselect(
    "Select Employee(s)",
    options=sorted(df['employee_id'].unique()),
    default=sorted(df['employee_id'].unique())
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['date'].min(), df['date'].max()]
)

filtered_df = df[
    (df['employee_id'].isin(employees)) &
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1]))
]

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================
card(
    "📌 Executive Summary",
    """
    <p>
    This dashboard provides real-time visibility into operational KPIs such as
    call volumes, escalation trends, and employee performance.
    The data is automatically processed and stored via backend pipelines,
    reducing manual reporting effort by <b>80–90%</b>.
    </p>
    """
    )

# =====================================================
# KPI CARDS
# =====================================================
st.subheader("📊 Key Performance Indicators")
c1, c2, c3, c4 = st.columns(4)

with c1:
    card("📞 Total Calls", f'<p class="kpi-number">{int(filtered_df["calls_handled"].sum())}</p>')

with c2:
    card("⏱ Avg Call Time (min)", f'<p class="kpi-number">{round(filtered_df["avg_call_time"].mean(), 2)}</p>')

with c3:
    card("⚠ Total Escalations", f'<p class="kpi-number">{int(filtered_df["escalation_count"].sum())}</p>')

with c4:
    card("👥 Active Employees", f'<p class="kpi-number">{filtered_df["employee_id"].nunique()}</p>')

st.divider()

# =====================================================
# AUTOMATED INSIGHTS
# =====================================================
if not filtered_df.empty:
    top_employee = filtered_df.groupby("employee_id")["calls_handled"].sum().idxmax()
    peak_day = filtered_df.groupby("date")["calls_handled"].sum().idxmax().date()
    escalation_rate = round((filtered_df['escalation_count'].sum() / filtered_df['calls_handled'].sum()) * 100, 2)

    card(
        "🧠 Automated Insights",
        f"""
        <ul>
            <li><b>Top Performing Employee:</b> {top_employee}</li>
            <li><b>Peak Call Volume Day:</b> {peak_day}</li>
            <li><b>Overall Escalation Rate:</b> {escalation_rate}%</li>
        </ul>
        """
    )

st.divider()

# =====================================================
# CHARTS
# =====================================================
st.subheader("📈 Performance Trends")
col1, col2 = st.columns(2)

with col1:
    card("Calls Handled Over Time", "")
    calls_by_date = filtered_df.groupby('date')['calls_handled'].sum()
    st.line_chart(calls_by_date)

with col2:
    card("Escalations by Employee", "")
    esc_by_emp = filtered_df.groupby('employee_id')['escalation_count'].sum()
    st.bar_chart(esc_by_emp)

st.divider()

# =====================================================
# DATA TABLE
# =====================================================
st.subheader("📋 Detailed KPI Records")
st.dataframe(filtered_df, use_container_width=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div class="footer">
<hr>
Designed & Developed by Lalit • Python Backend & Data Engineering Project
</div>
""", unsafe_allow_html=True)






























# import streamlit as st
# import pandas as pd
# import mysql.connector

# # =====================================================
# # PAGE CONFIG
# # =====================================================
# st.set_page_config(
#     page_title="Operational KPI Dashboard",
#     page_icon="📊",
#     layout="wide"
# )

# # =====================================================
# # GLOBAL STYLES (Corporate UI)
# # =====================================================
# st.markdown("""
# <style>
# body {
#     background-color: #f7f9fc;
# }
# h1, h2, h3, h4 {
#     color: #1f2937;
# }
# </style>
# """, unsafe_allow_html=True)

# # =====================================================
# # CARD COMPONENT (Reusable)
# # =====================================================
# def card(title, content):
#     st.markdown(
#         f"""
#         <div style="
#             border:1px solid #e5e7eb;
#             border-radius:14px;
#             padding:20px;
#             background-color:#ffffff;
#             box-shadow:0 6px 16px rgba(0,0,0,0.06);
#             margin-bottom:20px;">
#             <h4>{title}</h4>
#             {content}
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# # =====================================================
# # HEADER
# # =====================================================
# st.markdown(
#     """
#     <h1 style="text-align:center;">📊 Operational KPI Dashboard</h1>
#     <p style="text-align:center; color: gray;">
#     Automated Reporting & Performance Monitoring System
#     </p>
#     """,
#     unsafe_allow_html=True
# )

# st.divider()

# # =====================================================
# # MYSQL CONNECTION
# # =====================================================
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Lalit@282002",
#     database="reporting_db"
# )

# df = pd.read_sql("SELECT * FROM employee_kpis", conn)
# df['date'] = pd.to_datetime(df['date'])

# # =====================================================
# # SIDEBAR FILTERS
# # =====================================================
# st.sidebar.header("🔎 Dashboard Filters")

# employees = st.sidebar.multiselect(
#     "Select Employee(s)",
#     options=sorted(df['employee_id'].unique()),
#     default=sorted(df['employee_id'].unique())
# )

# date_range = st.sidebar.date_input(
#     "Select Date Range",
#     [df['date'].min(), df['date'].max()]
# )

# filtered_df = df[
#     (df['employee_id'].isin(employees)) &
#     (df['date'] >= pd.to_datetime(date_range[0])) &
#     (df['date'] <= pd.to_datetime(date_range[1]))
# ]

# # =====================================================
# # EXECUTIVE SUMMARY
# # =====================================================
# card(
#     "📌 Executive Summary",
#     """
#     <p>
#     This dashboard provides real-time visibility into operational KPIs such as
#     call volumes, escalation trends, and employee performance.
#     The data is automatically processed and stored via backend pipelines,
#     reducing manual reporting effort by 80–90%.
#     </p>
#     """
# )

# # =====================================================
# # KPI CARDS
# # =====================================================
# st.subheader("📊 Key Performance Indicators")

# c1, c2, c3, c4 = st.columns(4)

# with c1:
#     card("📞 Total Calls", f"<h2>{int(filtered_df['calls_handled'].sum())}</h2>")

# with c2:
#     card("⏱ Avg Call Time (min)", f"<h2>{round(filtered_df['avg_call_time'].mean(), 2)}</h2>")

# with c3:
#     card("⚠ Total Escalations", f"<h2>{int(filtered_df['escalation_count'].sum())}</h2>")

# with c4:
#     card("👥 Active Employees", f"<h2>{filtered_df['employee_id'].nunique()}</h2>")

# st.divider()

# # =====================================================
# # AUTOMATED INSIGHTS (UNIQUE SECTION)
# # =====================================================
# if not filtered_df.empty:
#     top_employee = (
#         filtered_df.groupby("employee_id")["calls_handled"]
#         .sum()
#         .idxmax()
#     )

#     peak_day = (
#         filtered_df.groupby("date")["calls_handled"]
#         .sum()
#         .idxmax()
#         .date()
#     )

#     escalation_rate = round(
#         (filtered_df['escalation_count'].sum() /
#          filtered_df['calls_handled'].sum()) * 100, 2
#     )

#     card(
#         "🧠 Automated Insights",
#         f"""
#         <ul>
#             <li><b>Top Performing Employee:</b> {top_employee}</li>
#             <li><b>Peak Call Volume Day:</b> {peak_day}</li>
#             <li><b>Overall Escalation Rate:</b> {escalation_rate}%</li>
#         </ul>
#         """
#     )

# st.divider()

# # =====================================================
# # CHARTS
# # =====================================================
# st.subheader("📈 Performance Trends")

# col1, col2 = st.columns(2)

# with col1:
#     card(
#         "Calls Handled Over Time",
#         ""
#     )
#     calls_by_date = filtered_df.groupby('date')['calls_handled'].sum()
#     st.line_chart(calls_by_date)

# with col2:
#     card(
#         "Escalations by Employee",
#         ""
#     )
#     esc_by_emp = filtered_df.groupby('employee_id')['escalation_count'].sum()
#     st.bar_chart(esc_by_emp)

# st.divider()

# # =====================================================
# # DATA TABLE
# # =====================================================
# st.subheader("📋 Detailed KPI Records")
# st.dataframe(filtered_df, use_container_width=True)

# # =====================================================
# # FOOTER
# # =====================================================
# st.markdown("""
# <hr>
# <p style="text-align:center; color: gray;">
# Designed & Developed by Lalit • Python Backend & Data Engineering Project
# </p>
# """, unsafe_allow_html=True)
