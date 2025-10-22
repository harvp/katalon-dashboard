import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------
# 🚀 CONFIGURATION
# ---------------------------
st.set_page_config(
    page_title="Katalon Test Dashboard",
    page_icon="🧪",
    layout="wide",
)

DATA_PATH = os.path.join("data", "processed", "katalon_results.csv")

# ---------------------------
# 📦 LOAD DATA
# ---------------------------
@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        st.error(f"❌ File not found: {path}")
        st.stop()
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", format="%d-%m-%Y")
    return df

df = load_data(DATA_PATH)

st.title("🧪 Katalon Test Results Dashboard")
st.markdown("Visual summary of nightly automation runs")

# ---------------------------
# 🔍 FILTERS
# ---------------------------
col1, col2 = st.columns([2, 3])

with col1:
    suites = st.multiselect(
        "Select Suite(s)",
        sorted(df["Suite"].unique()),
        default=sorted(df["Suite"].unique())
    )

with col2:
    min_date, max_date = df["Date"].min(), df["Date"].max()
    dates = st.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

filtered = df[
    (df["Suite"].isin(suites))
    & (df["Date"].between(pd.to_datetime(dates[0]), pd.to_datetime(dates[1])))
]

# ---------------------------
# 📊 KPI METRICS
# ---------------------------
total_tests = len(filtered)
failed_tests = len(filtered[filtered["Status"] == "FAILED"])
passed_tests = len(filtered[filtered["Status"] == "PASSED"])
failure_rate = (failed_tests / total_tests * 100) if total_tests else 0
avg_duration = filtered["Duration (s)"].mean() if not filtered.empty else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Tests", total_tests)
c2.metric("Passed", passed_tests)
c3.metric("Failed", failed_tests)
c4.metric("Failure Rate", f"{failure_rate:.1f}%")

st.markdown("---")

# ---------------------------
# 📈 CHARTS
# ---------------------------

# Failures over time
if not filtered.empty:
    daily_summary = (
        filtered.groupby(["Date", "Status"]).size().reset_index(name="Count")
    )
    fig = px.bar(
        daily_summary,
        x="Date",
        y="Count",
        color="Status",
        title="📅 Test Outcomes Over Time",
        barmode="group",
    )
    st.plotly_chart(fig, use_container_width=True)

    # Average duration per suite
    fig2 = px.bar(
        filtered.groupby("Suite", as_index=False)["Duration (s)"].mean(),
        x="Suite",
        y="Duration (s)",
        title="⏱️ Average Test Duration per Suite",
    )
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("No data available for selected filters.")

# ---------------------------
# 🧾 DETAILED VIEW
# ---------------------------
st.markdown("### 🧾 Test Case Details")
st.dataframe(
    filtered[["Date", "Suite", "Test Case", "Status", "Duration (s)", "Error Message"]],
    use_container_width=True,
    hide_index=True,
)

# ---------------------------
# 🧠 (OPTIONAL) AI SUMMARY PLACEHOLDER
# ---------------------------
st.markdown("---")
st.markdown("#### 🧠 AI Summary (coming soon)")
st.caption("This will generate natural-language summaries of failures using GPT.")


st.markdown("---")
st.caption("Katalon Dashboard • built with Streamlit & Plotly")
