from pathlib import Path as _Path

import pandas as _pandas

from stock_market.data._ipo import IPO
from stock_market.data._stocks import get_ticker, stock_health
from stock_market.data.reddit.trends import get_reddit_top_posts

# S&P data
SP500 = _pandas.read_csv(_Path(__file__).parent / "_files/sp500.csv")
