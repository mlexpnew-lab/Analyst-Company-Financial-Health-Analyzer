import streamlit as st
import plotly.express as px

st.title("📊 Overview")

session = st.session_state
if 'ratio_df' not in session or session['ratio_df'] is None:
    st.warning("No data yet. Go to the main page and run an analysis.")
    st.stop()

ratio_df = session['ratio_df']
ticker = session['ticker']
prices = session['prices']

kpis = {}
try:
    kpis = {
        "Gross Margin": float(ratio_df['gross_margin'].iloc[-1]),
        "Operating Margin": float(ratio_df['operating_margin'].iloc[-1]),
        "Net Margin": float(ratio_df['net_margin'].iloc[-1]),
        "Current Ratio": float(ratio_df['current_ratio'].iloc[-1]),
        "Debt-to-Equity": float(ratio_df['debt_to_equity'].iloc[-1]),
        "ROE": float(ratio_df['roe'].iloc[-1]),
    }
except Exception:
    pass

cols = st.columns(3)
items = list(kpis.items())
for i, (name, val) in enumerate(items):
    with cols[i % 3]:
        st.metric(name, f"{val:.2f}")

st.subheader(f"{ticker} Price History")
if prices is not None and not prices.empty:
    fig = px.line(prices.reset_index(), x='Date', y='Close', title=f"{ticker} Closing Prices")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Price history not available.")
