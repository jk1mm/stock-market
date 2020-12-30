from pathlib import Path as _Path

import pandas as _pandas

# S&P data
SP500 = _pandas.read_csv(_Path(__file__).parent / "index/sp500.csv")
