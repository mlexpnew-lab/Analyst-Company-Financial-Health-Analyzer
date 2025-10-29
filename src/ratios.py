from __future__ import annotations
import pandas as pd
import numpy as np

def compute_ratios(fin_df: pd.DataFrame) -> pd.DataFrame:
    df = fin_df.copy()
    df['gross_profit'] = df['revenue'] - df['cogs']
    df['gross_margin'] = df['gross_profit'] / df['revenue'].replace(0, np.nan)
    df['operating_margin'] = df['operating_income'] / df['revenue'].replace(0, np.nan)
    df['net_margin'] = df['net_income'] / df['revenue'].replace(0, np.nan)

    df['current_ratio'] = df['current_assets'] / df['current_liabilities'].replace(0, np.nan)
    df['quick_ratio'] = (df['current_assets'] - df.get('inventory', 0)) / df['current_liabilities'].replace(0, np.nan)

    df['debt_to_equity'] = df['total_liabilities'] / df['shareholders_equity'].replace(0, np.nan)

    df['asset_turnover'] = df['revenue'] / df['total_assets'].replace(0, np.nan)
    df['inventory_turnover'] = df['cogs'] / df.get('inventory', np.nan).replace(0, np.nan)
    df['roe'] = df['net_income'] / df['shareholders_equity'].replace(0, np.nan)
    df['roa'] = df['net_income'] / df['total_assets'].replace(0, np.nan)

    cols = ['date','revenue','net_income','gross_margin','operating_margin','net_margin',
            'current_ratio','quick_ratio','debt_to_equity','asset_turnover','inventory_turnover','roe','roa']
    keep = [c for c in cols if c in df.columns]
    out = df[keep].copy()
    return out
