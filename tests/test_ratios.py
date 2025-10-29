from src.ratios import compute_ratios
import pandas as pd

def test_compute_ratios_basic():
    df = pd.DataFrame([{
        'date':'2024-03-31',
        'revenue':100,
        'cogs':60,
        'operating_income':25,
        'net_income':20,
        'current_assets':50,
        'current_liabilities':25,
        'total_assets':200,
        'total_liabilities':80,
        'shareholders_equity':120,
        'inventory':10
    }])
    out = compute_ratios(df)
    row = out.iloc[0]
    assert round(row['gross_margin'],2) == 0.40
    assert round(row['operating_margin'],2) == 0.25
    assert round(row['net_margin'],2) == 0.20
    assert round(row['current_ratio'],2) == 2.00
    assert round(row['debt_to_equity'],2) == 0.67
