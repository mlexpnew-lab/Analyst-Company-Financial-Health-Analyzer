import streamlit as st
import plotly.express as px

st.title("📈 Financial Ratios")

if 'ratio_df' not in st.session_state or st.session_state['ratio_df'] is None:
    st.warning("No data yet. Go to the main page and run an analysis.")
    st.stop()

df = st.session_state['ratio_df']

st.dataframe(df.tail(12), use_container_width=True)

metric = st.selectbox("Select a ratio to chart", [
    "gross_margin","operating_margin","net_margin","current_ratio",
    "quick_ratio","debt_to_equity","asset_turnover","inventory_turnover","roe","roa"
], index=0)

fig = None
try:
    fig = px.line(df.reset_index(), x='date', y=metric, title=f"{metric} over time")
except Exception as e:
    st.error(f"Could not plot: {e}")

if fig:
    st.plotly_chart(fig, use_container_width=True)
