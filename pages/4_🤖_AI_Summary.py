import streamlit as st
from src.summary import generate_summary

st.title("🤖 AI Summary")

if 'ratio_df' not in st.session_state or st.session_state['ratio_df'] is None:
    st.warning("No data yet. Go to the main page and run an analysis.")
    st.stop()

ratio_df = st.session_state['ratio_df']
sentiment_df = st.session_state.get('sentiment_df', None)
ticker = st.session_state.get('ticker', 'TICKER')
currency = st.session_state.get('currency', 'USD')

style = st.selectbox("Summary style", ["Executive brief","Analyst deep-dive"], index=0)
summary = generate_summary(ratio_df, sentiment_df, ticker, currency, style=style)

st.subheader("Summary")
st.write(summary)
