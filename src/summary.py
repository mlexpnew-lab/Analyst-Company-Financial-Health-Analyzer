from __future__ import annotations
import pandas as pd
import numpy as np
import textwrap

def _fmt_pct(x):
    if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
        return "n/a"
    try:
        return f"{float(x) * 100:.1f}%"
    except Exception:
        return "n/a"

def generate_summary(
    ratio_df: pd.DataFrame,
    sentiment_df: pd.DataField | None,
    ticker: str,
    currency: str,
    style: str = "Executive brief",
) -> str:
    if ratio_df is None or ratio_df.empty:
        return "No ratio data available."

    latest = ratio_df.iloc[0 if len(ratio_df) == 0 else -1]
    trend = ratio_df.tail(4)

    def dir_text(series: pd.Series) -> str:
        s = series.dropna()
        if s.shape[0] < 2:
            return "stable"
        delta = float(s.iloc[-1]) - float(s.iloc[0])
        if   delta >  0.02: return "improving"
        elif delta < -0.02: return "worsening"
        else:               return "stable"

    gross = _fmt_pct(latest.get("gross_margin", np.nan))
    op    = _fmt_pct(latest.get("operating_margin", np.nan))
    net   = _fmt_pct(latest.get("net_margin", np.nan))
    cur   = latest.get("current_ratio", np.nan)
    de    = latest.get("debt_to_equity", np.nan)
    roe   = _fmt_pct(latest.get("roe", np.nan))

    gross_dir = dir_text(trend["gross_margin"])     if "gross_margin"     in trend else "stable"
    net_dir   = dir_text(trend["net_margin"])       if "net_margin"       in trend else "stable"
    de_dir    = dir_text(trend["debt_to_equity"])   if "debt_to_equity"   in trend else "stable"

    sentiment_line = ""
    if sentiment_df is not None and not sentiment_df.empty and "compound" in sentiment_df:
        avg = float(sentiment_df.tail(30)["compound"].mean())
        if   avg >  0.05: bias = "positive"
        elif avg < -0.05: bias = "negative"
        else:             bias = "mixed"
        sentiment_line = f" Recent news sentiment appears **{bias}** (avg VADER {avg:.2f})."

    risk_note = ">1.0 is healthy" if (isinstance(cur, (int, float)) and not np.isnan(cur) and cur >= 1.0) else "<1.0 is a risk"

    body = f"""
**{ticker}** financial health snapshot ({currency} reporting):
- **Profitability:** Gross margin {gross} ({gross_dir}), operating margin {op}, net margin {net} ({net_dir}).
- **Liquidity:** Current ratio {cur:.2f} ({risk_note}); quick ratio on Ratios tab.
- **Leverage:** Debt-to-equity {de:.2f} ({de_dir}).
- **Returns:** ROE {roe}.

**Risks & watchpoints**
- Monitor leverage trend and interest coverage.
- Track margin trajectory vs. peers and input costs.
- If current ratio < 1.0, watch working-capital strain.

**Outlook** —{sentiment_line}
""".strip()

    if style == "Analyst deep-dive":
        body += "\n\n_Methodology:_ Ratios computed from standardized statement lines; sentiment uses NLTK VADER on recent headlines."

    return textwrap.dedent(body)
