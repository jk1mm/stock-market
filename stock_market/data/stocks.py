from typing import Optional

import numpy as np
import pandas as pd
from pandas_datareader import data


# Reference:
# https://towardsdatascience.com/how-to-get-market-data-from-the-nyse-in-less-than-3-lines-python-41791212709c
def get_ticker(
    ticker: str,
    start_date: str,
    end_date: str = None,
) -> Optional[pd.DataFrame]:
    """
    Extracts stock prices over a date period from Yahoo Finance.

    Parameters
    ----------
    ticker: str
        Stock ticker symbol.

    start_date: str
        Start date of stock information. (e.g. 2020-01-01, 2020/01/01, January 1 2020)

    end_date: str, default None
        End date of stock information. If None, use current date.

    Returns
    -------
    stock_data: Optional[pd.DataFrame]
        Stock information, extracted from Yahoo Finance.

    """
    # Convert string dates to DateTime
    start_date = pd.to_datetime(start_date)
    if end_date:
        end_date = pd.to_datetime(end_date)
    else:
        end_date = pd.to_datetime("today")

    # Extract stock data using DataReader
    try:
        stock_data = data.DataReader(ticker, "yahoo", start_date, end_date)
    except KeyError:
        stock_data = None

    # Adding new metrics
    if stock_data is not None:

        # 1) Day to day percent change
        if len(stock_data) >= 2:
            stock_close = np.array(stock_data["Close"], dtype=float)
            stock_pct_change_d2d = list(np.diff(stock_close) / stock_close[:-1] * 100.0)
        else:
            stock_pct_change_d2d = []

        # Check if the first row is ipo day
        try:
            # Market is guaranteed open at least once on a 5 consecutive day period
            previous_close = data.DataReader(
                ticker,
                "yahoo",
                start_date - pd.Timedelta(days=5),
                start_date - pd.Timedelta(days=1),
            )["Close"][-1]
            start_close = stock_data["Close"][0]
            previous_pct_change = [
                (start_close - previous_close) / previous_close * 100.0
            ]

        except KeyError:
            previous_pct_change = [None]

        # Add metric
        stock_pct_change_d2d = previous_pct_change + stock_pct_change_d2d
        stock_data["Pct: Day Over Day"] = stock_pct_change_d2d

        # 2) Within day percent change
        stock_data["Pct: Within Day"] = (
            (np.array(stock_data["Close"]) - np.array(stock_data["Open"]))
            / np.array(stock_data["Open"])
            * 100.0
        )

        # 3) Within day volatility (pct)
        day_range = np.array(stock_data["High"]) - np.array(stock_data["Low"])
        day_median = (np.array(stock_data["High"]) + np.array(stock_data["Low"])) / 2
        stock_data["Pct: Day Volatility"] = day_range / day_median * 100.0

        # 4) Within day volatility (value)
        stock_data["Value: Day Volatility"] = day_range

        # 5) Approximate dollar amount traded
        stock_data["Value: Volume in Dollars"] = day_median * np.array(
            stock_data["Volume"]
        )

    return stock_data
