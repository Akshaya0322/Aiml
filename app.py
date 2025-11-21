import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Meeting Cost Analyzer", page_icon="📊", layout="wide")

# -----------------------------
# 1. USER UPLOAD SECTION
# -----------------------------
st.title("📊 AI Meeting Cost Analyzer — Upload Your Dataset")

uploaded = st.file_uploader("📥 Upload your CSV meeting dataset", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)

    st.success("✅ Dataset uploaded successfully!")

    # Show sample
    st.subheader("👀 Sample Data")
    st.dataframe(df.head())

    st.divider()

    # -----------------------------
    # 2. SIDEBAR FILTERS
    # -----------------------------
    st.sidebar.header("🔍 Filters")

    # Only add filters for columns that EXIST
    day = st.sidebar.multiselect("Meeting Day", sorted(df["meeting_day"].unique())) if "meeting_day" in df else None
    mtype = st.sidebar.multiselect("Meeting Type", df["meeting_type"].unique()) if "meeting_type" in df else None
    prod = st.sidebar.selectbox("Productivity", ["All", "Productive (1)", "Not Productive (0)"]) if "productive" in df else None

    # Apply filters
    filtered = df.copy()
    if day: filtered = filtered[filtered["meeting_day"].isin(day)]
    if mtype: filtered = filtered[filtered["meeting_type"].isin(mtype)]
    if prod and prod != "All":
        filtered = filtered[filtered["productive"] == (1 if prod=="Productive (1)" else 0)]

    st.divider()

    # -----------------------------
    # 3. KPI CARDS
    # -----------------------------
    st.subheader("📌 Key Metrics")

    total = len(filtered)
    avg_cost = filtered["cost_inr"].mean() if "cost_inr" in filtered else 0
    avg_dur = filtered["duration_min"].mean() if "duration_min" in filtered else 0
    prod_rate = round(filtered["productive"].mean()*100,2) if "productive" in filtered else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Meetings", total)
    col2.metric("Avg Cost (₹)", round(avg_cost,2))
    col3.metric("Avg Duration (min)", round(avg_dur,2))
    col4.metric("Productivity (%)", prod_rate)

    st.divider()

    # -----------------------------
    # 4. INTERACTIVE ACTION BUTTONS
    # -----------------------------
    c1, c2, c3 = st.columns(3)

    if c1.button("📥 Download Filtered Data"):
        csv = filtered.to_csv(index=False).encode()
        st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")

    if c2.button("👁 Show Raw Data"):
        st.dataframe(filtered)

    if c3.button("📋 Summary Statistics"):
        st.write(filtered.describe())

    st.divider()

    # -----------------------------
    # 5. VISUALIZATIONS
    # -----------------------------

    # Line chart: Cost vs Day
    if "cost_inr" in filtered and "meeting_day" in filtered:
        st.subheader("📈 Cost Trend by Day")
        fig, ax = plt.subplots()
        sns.lineplot(data=filtered, x="meeting_day", y="cost_inr", marker="o", ax=ax)
        st.pyplot(fig)

    # Productivity trend
    if "meeting_day" in filtered and "productive" in filtered:
        st.subheader("📊 Productivity Trend by Day")
        daily = filtered.groupby("meeting_day")["productive"].mean()*100
        fig, ax = plt.subplots()
        sns.lineplot(x=daily.index, y=daily.values, marker="o", ax=ax)
        st.pyplot(fig)

    # Cost distribution
    if "cost_inr" in filtered:
        with st.expander("📌 Cost Distribution"):
            fig, ax = plt.subplots()
            sns.histplot(filtered["cost_inr"], kde=True, ax=ax)
            st.pyplot(fig)

    # Duration vs Cost
    if "duration_min" in filtered and "cost_inr" in filtered:
        with st.expander("⏱️ Duration vs Cost"):
            fig, ax = plt.subplots()
            sns.scatterplot(data=filtered, x="duration_min", y="cost_inr", hue="productive" if "productive" in filtered else None, ax=ax)
            st.pyplot(fig)

    st.success("🎉 Dashboard loaded successfully!")

else:
    st.info("📤 Please upload a CSV file to begin.")

