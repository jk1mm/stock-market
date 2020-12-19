from pandas_datareader import data
import pandas as pd


# Reference:
# https://towardsdatascience.com/how-to-get-market-data-from-the-nyse-in-less-than-3-lines-python-41791212709c
def get_ticker(ticker: str, start_date: str, end_date: str = None) -> pd.DataFrame:
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
    stock_data: pd.DataFrame
        Stock information, extracted from Yahoo Finance.

    """
    # Convert string dates to DateTime
    start_date = pd.to_datetime(start_date)
    if end_date:
        end_date = pd.to_datetime(end_date)
    else:
        end_date = pd.to_datetime("today")

    # Extract stock data using DataReader
    stock_data = data.DataReader(ticker, "yahoo", start_date, end_date)

    return stock_data
