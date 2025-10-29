# 💹 Company Financial Health Analyzer

**Company Financial Health Analyzer** is a data-driven **Streamlit web app** that evaluates and visualizes a company’s financial health.  
It helps **investors, analysts, and decision-makers** quickly understand performance trends by combining **financial ratios, market sentiment, and AI-driven insights.**

---

## 🚀 Live Demo
🌐 [Try it on Streamlit Cloud](https://share.streamlit.io/yourusername/Analyst-Company-Financial-Health-Analyzer/main/app.py)

---

## 🧭 Overview

This interactive dashboard provides:

| Feature | Description |
|----------|--------------|
| 📈 **Financial Ratios** | Automatically compute profitability, liquidity, leverage, and efficiency ratios. |
| 💬 **Market Sentiment** | Analyze headline tone using NLTK VADER sentiment scores. |
| 🤖 **AI Summary** | Generate plain-language financial summaries (LLM-ready). |
| 📊 **Visual Insights** | Dynamic KPI cards, ratio trends, and sentiment scatter plots. |
| 📤 **CSV Upload** | Upload your own company financials (up to 200MB) for instant analysis. |

---

## 🏗️ Project Architecture

Analyst-Company-Financial-Health-Analyzer/
├─ app.py # Main Streamlit app
├─ pages/ # Multipage Streamlit sections
│ ├─ 1_📊_Overview.py
│ ├─ 2_📈_Ratios.py
│ ├─ 3_📰_Sentiment.py
│ └─ 4_🤖_AI_Summary.py
├─ src/ # Core data logic
│ ├─ data.py # Data loading (yfinance / CSV / uploads)
│ ├─ ratios.py # Ratio calculations
│ ├─ sentiment.py # VADER sentiment scoring
│ └─ summary.py # Executive/analyst text summary
├─ data/
│ ├─ sample_financials.csv # Example demo data
│ └─ sample_news.csv # Example sentiment data
├─ tests/
│ └─ test_ratios.py # Unit test for ratio calculations
├─ .streamlit/config.toml # Custom dark theme config
├─ requirements.txt # Dependencies
└─ README.md # You are here


🎉

🧩 Uploading Your Own Financial Data

You can upload any CSV file with the following columns (case-insensitive):

Column	Example	Description
date	2024-03-31	Financial period
revenue	390000000000	Total revenue
cogs	224000000000	Cost of goods sold
operating_income	116000000000	EBIT / Operating profit
net_income	101000000000	Net profit
current_assets	150000000000	Total current assets
current_liabilities	135000000000	Total current liabilities
total_assets	370000000000	Total assets
total_liabilities	292000000000	Total liabilities
shareholders_equity	78000000000	Book equity
inventory	7200000000	Inventory balance

💡 The app can process CSVs up to ~200 MB and auto-detects , or ; separators.

🧮 Supported Financial Ratios
Category	Ratios
Profitability	Gross Margin, Operating Margin, Net Margin
Liquidity	Current Ratio, Quick Ratio
Leverage	Debt-to-Equity
Efficiency	Asset Turnover, Inventory Turnover
Returns	ROE, ROA
🧠 Sentiment Analysis

Uses NLTK VADER to score headline sentiment.

Compound scores range from -1 (very negative) to +1 (very positive).

Displays scatter plots and rolling sentiment averages.

🧾 AI-Powered Summary

Generates a concise textual analysis combining:

Recent ratio performance

Trends (improving / worsening / stable)

Market sentiment overview

Example output:

“Gross margin 51.3% (improving), ROE 27.4%, current ratio 1.5 (healthy).
Recent news sentiment appears positive. Watch leverage and input costs.”

☁️ Deploy on Streamlit Cloud

Push this repo to GitHub

Go to https://share.streamlit.io/

New App → Select this repo

Set Main file path = app.py

(Optional) Add OPENAI_API_KEY under Secrets for future LLM integration

Click Deploy

Your app will be live with a public shareable link 🌍

🛠️ Tech Stack
Component	Tool
Frontend / Dashboard	Streamlit

Data Analysis	Pandas
, NumPy

Visualization	Plotly Express

Market Data	yFinance

Sentiment Analysis	NLTK VADER

Language Summaries	Optional OpenAI API
🧰 Future Enhancements

🔌 Live financial API integration (e.g., Financial Modeling Prep, Alpha Vantage)

📤 Export ratio reports (CSV/PDF download)

📈 Peer benchmarking

🧠 GPT-powered executive summaries

📊 Multi-company comparison dashboard

👨‍💻 Author

Chandni Luxe
📷 Instagram: @chandniluxe

💼 GitHub: @mlexpnew-lab
🪪 License

This project is licensed under the MIT License — you’re free to use, modify, and distribute it with attribution.

