import streamlit as st
import pandas as pd
import plotly.express as px

from src.data import get_price_history, load_financials, load_uploaded_csv
from src.ratios import compute_ratios
from src.sentiment import load_news_and_score
from src.summary import generate_summary


st.set_page_config(page_title="Company Financial Health Analyzer", layout="wide", page_icon="💹")

# ------------ Sidebar: Professional Inputs ------------
st.sidebar.title("⚙️ Settings")

# 1) Data source + file upload (with preview)
source_choice = st.sidebar.radio(
    "Data source",
    ["Use built-in sample data", "Upload my own CSV"],
    index=0,
)

uploaded_file = None
uploaded_preview_df = None

if source_choice == "Upload my own CSV":
    st.sidebar.caption(
        "Upload a CSV with these columns:\n"
        "`date,revenue,cogs,operating_income,net_income,current_assets,current_liabilities,total_assets,total_liabilities,shareholders_equity,inventory`"
    )
    uploaded_file = st.sidebar.file_uploader("Choose CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            uploaded_preview_df = pd.read_csv(uploaded_file, nrows=5)
            st.sidebar.success(f"✅ Loaded: {uploaded_file.name}")
            st.sidebar.caption("Preview (first 5 rows):")
            st.sidebar.dataframe(uploaded_preview_df, use_container_width=True)
            uploaded_file.seek(0)  # reset pointer for full read later
        except Exception as e:
            st.sidebar.error(f"❌ Could not read CSV preview: {e}")

# 2) Ticker picker (with Custom…)
ticker_options = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "IBM", "ORCL", "Custom…"]
ticker_sel = st.sidebar.selectbox("Ticker (for labeling / price lookup)", ticker_options, index=0)
ticker = st.sidebar.text_input("Enter custom ticker", value="AAPL") if ticker_sel == "Custom…" else ticker_sel

# 3) Currency picker (with Custom…)
currency_options = ["USD", "INR", "EUR", "GBP", "JPY", "AUD", "CAD", "AED", "SAR", "SGD", "IDR", "MYR", "Custom…"]
currency_sel = st.sidebar.selectbox("Currency label", currency_options, index=0)
currency = st.sidebar.text_input("Enter custom currency code", value="USD") if currency_sel == "Custom…" else currency_sel

# 4) Price history period
period = st.sidebar.selectbox("Price history period", ["6mo", "1y", "2y", "5y"], index=1)

# 5) Action
run = st.sidebar.button("Analyze", type="primary", use_container_width=True)

# ------------ Header / Hero ------------
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="font-size:42px;">💹</div>
      <div>
        <h1 style="margin:0;">Company Financial Health Analyzer</h1>
        <div style="opacity:.75">Financial ratios • Sentiment • AI summary</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

if source_choice == "Upload my own CSV" and uploaded_file is None:
    st.info("Upload a CSV from the sidebar to see a preview, then click **Analyze**.")

# ------------ Run analysis ------------
if run:
    with st.spinner("Crunching numbers…"):
        try:
            # Data source selection
            if uploaded_file is not None:
                fin_df = load_uploaded_csv(uploaded_file)
            else:
                fin_df = load_financials(ticker)

            # Extra schema guard (friendly message if bad)
            required = {
                "date", "revenue", "cogs", "operating_income", "net_income",
                "current_assets", "current_liabilities", "total_assets",
                "total_liabilities", "shareholders_equity", "inventory"
            }
            missing = [c for c in required if c not in fin_df.columns]
            if missing:
                st.error(f"Your data is missing columns: {missing}")
                st.stop()

            # Compute + fetch
            ratio_df = compute_ratios(fin_df)
            sentiment_df = load_news_and_score(ticker)
            prices = get_price_history(ticker, period)

            # Stash in session state
            st.session_state.update(
                ticker=ticker,
                currency=currency,
                prices=prices,
                fin_df=fin_df,
                ratio_df=ratio_df,
                sentiment_df=sentiment_df,
            )
            st.success("✅ Analysis complete. Explore the dashboard below or use the pages on the left.")
        except Exception as e:
            st.error("⚠️ Something went wrong while processing the data.")
            with st.expander("Show technical details"):
                st.exception(e)
            st.stop()

# ------------ Home summary (shows after first run) ------------
if "ratio_df" in st.session_state and st.session_state["ratio_df"] is not None:
    ratio_df = st.session_state["ratio_df"]
    prices = st.session_state.get("prices")
    tck = st.session_state.get("ticker", "")
    cur = st.session_state.get("currency", "")

    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Ratios", "📰 Sentiment"])

    with tab1:
        st.subheader(f"Snapshot — {tck} ({cur})")

        # KPI cards
        cols = st.columns(3)
        with cols[0]:
            st.metric("Gross Margin", f"{ratio_df['gross_margin'].iloc[-1]*100:.1f}%")
        with cols[1]:
            st.metric("Operating Margin", f"{ratio_df['operating_margin'].iloc[-1]*100:.1f}%")
        with cols[2]:
            st.metric("Net Margin", f"{ratio_df['net_margin'].iloc[-1]*100:.1f}%")

        cols = st.columns(3)
        with cols[0]:
            st.metric("Current Ratio", f"{ratio_df['current_ratio'].iloc[-1]:.2f}")
        with cols[1]:
            st.metric("Debt-to-Equity", f"{ratio_df['debt_to_equity'].iloc[-1]:.2f}")
        with cols[2]:
            st.metric("ROE", f"{ratio_df['roe'].iloc[-1]*100:.1f}%")

        st.markdown("### 📈 Price history")
        if prices is not None and not prices.empty:
            # extra guard: ensure 1-D numeric
            prices = prices.copy()
            prices["Close"] = pd.to_numeric(prices["Close"], errors="coerce")
            fig = px.line(prices.reset_index(), x="Date", y="Close", title=f"{tck} — Closing Prices")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No price data available for this ticker/period.")

    with tab2:
        st.subheader("Selected ratio over time")
        metric = st.selectbox(
            "Pick a ratio",
            ["gross_margin", "operating_margin", "net_margin", "current_ratio",
             "quick_ratio", "debt_to_equity", "asset_turnover", "inventory_turnover", "roe", "roa"],
            index=0
        )
        fig = px.line(ratio_df.reset_index(), x="date", y=metric, markers=True, title=metric)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(ratio_df.tail(12), use_container_width=True)

    with tab3:
        sdf = st.session_state.get("sentiment_df")
        if sdf is None or sdf.empty or "compound" not in sdf.columns:
            st.info("No sentiment data available. Add headlines to `data/sample_news.csv` or integrate a news API.")
        else:
            st.dataframe(sdf[["date", "source", "headline", "compound"]].tail(20), use_container_width=True)
            fig = px.scatter(
                sdf, x="date", y="compound", hover_data=["headline", "source"],
                title="Headline Sentiment (VADER compound)"
            )
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("➜ Pick a data source, choose Ticker & Currency from the sidebar, then click **Analyze**.")
