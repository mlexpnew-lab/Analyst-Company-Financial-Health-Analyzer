from __future__ import annotations
import pandas as pd
import io
from pathlib import Path
import yfinance as yf


# Base data directory
DATA_DIR = Path(__file__).resolve().parents[1] / "data"


# -------------------------------------------------------------------
# ✅ Upload CSV Loader (handles both Streamlit + local open())
# -------------------------------------------------------------------
def load_uploaded_csv(file) -> pd.DataFrame:
    """
    Load a user-uploaded CSV file robustly.
    Supports both Streamlit UploadedFile and normal open() file objects.
    """
    if file is None:
        raise ValueError("No file provided.")

    # Works with both Streamlit UploadedFile and standard file handles
    try:
        if hasattr(file, "getvalue"):
            raw = file.getvalue()
        else:
            raw = file.read()
        if not raw:
            raise ValueError("File is empty.")
        text = raw.decode("utf-8", errors="ignore")
    except Exception as e:
        raise ValueError(f"Unable to read uploaded file: {e}")

    # Detect separator
    sample = text[:2000]
    if sample.count(",") >= sample.count(";") and sample.count(",") >= sample.count("\t"):
        sep = ","
    elif sample.count(";") >= sample.count("\t"):
        sep = ";"
    else:
        sep = "\t"

    try:
        df = pd.read_csv(io.StringIO(text), sep=sep)
    except Exception as e:
        raise ValueError(f"Unable to parse CSV content: {e}")

    if df.empty or df.shape[1] == 0:
        raise ValueError("CSV appears empty or has no readable columns.")

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Validate required columns
    required = [
        "date", "revenue", "cogs", "operating_income", "net_income",
        "current_assets", "current_liabilities", "total_assets",
        "total_liabilities", "shareholders_equity", "inventory"
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    if df["date"].isna().all():
        raise ValueError("Could not parse any valid dates in 'date' column.")

    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return df


# -------------------------------------------------------------------
# ✅ Load Built-in Sample Financials
# -------------------------------------------------------------------
def load_financials(_: str) -> pd.DataFrame:
    """
    Loads bundled sample financial data.
    """
    sample_path = DATA_DIR / "sample_financials.csv"
    if not sample_path.exists():
        raise FileNotFoundError(f"Sample data not found: {sample_path}")

    df = pd.read_csv(sample_path)
    if df.empty:
        raise ValueError(f"Sample financials file is empty: {sample_path}")

    if "date" not in df.columns:
        raise ValueError("Sample CSV missing required 'date' column.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return df


# -------------------------------------------------------------------
# ✅ Get Stock Price History from Yahoo Finance
# -------------------------------------------------------------------
def get_price_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch price history using yfinance and normalize 'Close' column.
    Handles MultiIndex columns and array-like cells.
    """
    try:
        df = yf.download(ticker, period=period, progress=False)
        if not isinstance(df, pd.DataFrame) or df.empty:
            return pd.DataFrame()

        # Handle MultiIndex columns (('Close','AAPL')) or single-level
        if isinstance(df.columns, pd.MultiIndex):
            if ("Close", ticker) in df.columns:
                close = df[("Close", ticker)]
            elif "Close" in df.columns.get_level_values(0):
                close = df["Close"].iloc[:, 0]
            else:
                close = df.select_dtypes("number").iloc[:, 0]
        else:
            close = df["Close"] if "Close" in df.columns else df.select_dtypes("number").iloc[:, 0]

        # Flatten lists/arrays
        import numpy as np
        close = close.apply(lambda v: v[0] if isinstance(v, (list, tuple, np.ndarray)) else v)
        close = pd.to_numeric(close, errors="coerce")

        out = close.rename("Close").to_frame()
        out.index.name = "Date"
        return out
    except Exception:
        return pd.DataFrame()
