import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64

st.set_page_config(page_title="AI Meeting Cost Dashboard", page_icon="📊", layout="wide")

df = pd.read_csv("meeting_cost_dataset_inr.csv")

# Trend helper
def trend_arrow(value):
    return "⬆️" if value > 0 else "⬇️"

# Custom CSS
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(to right, #4B7BE5, #7FA6FF);
    padding: 16px;
    border-radius: 18px;
    color: white;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.2);
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("✨ AI Meeting Cost Dashboard — Interactive Edition")

# -----------------------------------
# SIDEBAR FILTERS
with st.sidebar:
    st.header("🔍 Filters")
    day = st.multiselect("Meeting Day", sorted(df["meeting_day"].unique()))
    mtype = st.multiselect("Meeting Type", df["meeting_type"].unique())
    prod = st.selectbox("Productivity", ["All", "Productive (1)", "Not Productive (0)"])

# apply filters
filtered = df.copy()
if day: filtered = filtered[filtered["meeting_day"].isin(day)]
if mtype: filtered = filtered[filtered["meeting_type"].isin(mtype)]
if prod != "All":
    filtered = filtered[filtered["productive"] == (1 if prod=="Productive (1)" else 0)]

# -----------------------------------
# KPI
total = len(filtered)
avg_cost = filtered.cost_inr.mean()
avg_dur = filtered.duration_min.mean()
prod_rate = round(filtered.productive.mean()*100,2)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='metric-card'>Meetings<br><h2>{total}</h2></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='metric-card'>Avg Cost<br><h2>₹{avg_cost:.2f}</h2></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='metric-card'>Avg Duration<br><h2>{avg_dur:.1f} min</h2></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='metric-card'>Productivity<br><h2>{prod_rate}%</h2></div>", unsafe_allow_html=True)

st.divider()

# -----------------------------------
# INTERACTIVE BUTTONS

colA, colB, colC = st.columns(3)

if colA.button("📥 Download Filtered Data"):
    csv = filtered.to_csv(index=False).encode()
    st.download_button("Download CSV", csv, "filtered_meetings.csv", "text/csv")

if colB.button("👁 Show Raw Data"):
    st.dataframe(filtered)

if colC.button("🧮 Show Summary Table"):
    st.write(filtered.describe())

st.divider()

# -----------------------------------
# OVER-TIME TRENDS
st.subheader("📈 Cost Trend by Day")

fig, ax = plt.subplots()
sns.lineplot(x="meeting_day", y="cost_inr", data=filtered, marker="o", ax=ax)
st.pyplot(fig)

# -----------------------------------
# Productivity Trend
st.subheader("📊 Productivity Trend (Day-wise)")

daily = filtered.groupby("meeting_day")["productive"].mean()*100

fig, ax = plt.subplots()
sns.lineplot(x=daily.index, y=daily.values, marker="o", ax=ax)
st.pyplot(fig)

st.write(f"Trend change: **{(daily.iloc[-1]-daily.iloc[0]):.2f}%** {trend_arrow(daily.iloc[-1]-daily.iloc[0])}")

st.divider()

# -----------------------------------
# HIDE / SHOW SECTION
with st.expander("📌 Show Cost Distribution Chart"):
    fig, ax = plt.subplots()
    sns.histplot(filtered.cost_inr, kde=True, ax=ax)
    st.pyplot(fig)

# -----------------------------------
# Duration vs Cost
with st.expander("⏱️ Duration vs Cost Relationship"):
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered, x="duration_min", y="cost_inr", hue="productive", ax=ax)
    st.pyplot(fig)

# -----------------------------------
st.success("✅ Interactive Dashboard Loaded Successfully!")
