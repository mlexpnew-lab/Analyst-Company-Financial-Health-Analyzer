from __future__ import annotations
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Lazy VADER loader
_vader = None
def _get_vader():
    global _vader
    if _vader is None:
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            _vader = SentimentIntensityAnalyzer()
        except Exception:
            import nltk
            nltk.download("vader_lexicon")
            from nltk.sentiment import SentimentIntensityAnalyzer
            _vader = SentimentIntensityAnalyzer()
    return _vader

def load_news_and_score(_: str) -> pd.DataFrame:
    """
    Robustly load optional news CSV and compute VADER compound.
    Returns an EMPTY DataFrame if file is missing/empty/unreadable.
    Expected columns (if present): date, source, headline
    """
    news_path = DATA_DIR / "sample_news.csv"

    # If no file, just return empty frame with expected columns.
    if not news_path.exists():
        return pd.DataFrame(columns=["date", "source", "headline", "compound"])

    # Try to read; handle empty or bad CSVs gracefully.
    try:
        df = pd.read_csv(news_path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["date", "source", "headline", "compound"])
    except Exception:
        return pd.DataFrame(columns=["date", "source", "headline", "compound"])

    # Normalize columns
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Ensure required cols exist
    for col in ["date", "source", "headline"]:
        if col not in df.columns:
            df[col] = pd.Series(dtype="object")

    # Parse date (don’t fail if bad)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Compute VADER compound if headlines exist
    if "headline" in df.columns and not df["headline"].empty:
        vader = _get_vader()
        df["compound"] = df["headline"].astype(str).apply(
            lambda x: vader.polarity_scores(x)["compound"] if x.strip() else 0.0
        )
    else:
        df["compound"] = pd.Series(dtype="float")

    # Sort & return
    return df.sort_values("date").reset_index(drop=True)
