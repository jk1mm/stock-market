import pandas as pd

# Stock categories (from S&P 500)
STOCK_CATEGORY = list(set(pd.read_csv("index/sp500.csv").Sector))
