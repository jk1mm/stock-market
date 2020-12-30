from pathlib import Path as _Path

import pandas as _pandas

from ._ipo import IPO
from ._stocks import get_ticker

# S&P data
SP500 = _pandas.read_csv(_Path(__file__).parent / "index/sp500.csv")
