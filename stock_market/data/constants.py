from stock_market.data import SP500

# Stock categories (from S&P 500)
STOCK_CATEGORY = [industry.lower() for industry in list(set(SP500.Sector))]


# Analysis
# --------

# Index: WebScrape constants

# SP500
SP500_LINK = "https://www.marketwatch.com/investing/index/spx"
PERFORMANCE_PERIODIC = "performance"
PERFORMANCE_TOP_STOCKS = "ByIndexGainers"
PERFORMERS_BOTTOM_STOCKS = "ByIndexDecliners"
