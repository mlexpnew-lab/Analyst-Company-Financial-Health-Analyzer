import streamlit as st
import plotly.express as px

st.title("📰 Market Sentiment")

if 'sentiment_df' not in st.session_state or st.session_state['sentiment_df'] is None:
    st.warning("No data yet. Go to the main page and run an analysis.")
    st.stop()

sdf = st.session_state['sentiment_df']
if 'compound' not in sdf.columns or sdf.empty:
    st.info("No sentiment data available. Add news to data/sample_news.csv")
else:
    st.dataframe(sdf[['date','source','headline','compound']].tail(20), use_container_width=True)
    fig = px.scatter(sdf, x='date', y='compound', hover_data=['headline','source'],
                     title="Headline Sentiment (VADER compound)")
    st.plotly_chart(fig, use_container_width=True)
