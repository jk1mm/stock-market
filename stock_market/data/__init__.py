from pathlib import Path as _Path

import pandas as _pandas

from stock_market.data._ipo import IPO
from stock_market.data._stocks import get_ticker

# S&P data
SP500 = _pandas.read_csv(_Path(__file__).parent / "index/sp500.csv")
