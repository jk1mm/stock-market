from stock_market.data import SP500

# Stock categories (from S&P 500)
STOCK_CATEGORY = [industry.lower() for industry in list(set(SP500.Sector))]
