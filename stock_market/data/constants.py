import pandas as pd

# Stock categories (from S&P 500)
STOCK_CATEGORY = [
    industry.lower() for industry in list(set(pd.read_csv("index/sp500.csv").Sector))
]
