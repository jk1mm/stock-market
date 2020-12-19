from pandas_datareader import data
import pandas as pd


# Reference:
# https://towardsdatascience.com/how-to-get-market-data-from-the-nyse-in-less-than-3-lines-python-41791212709c
def get_ticker(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Extracts stock prices over a date period from Yahoo Finance.

    Parameters
    ----------
    ticker: str
        Stock ticker symbol.

    start_date: str
        Start date of stock information. (Use format YYYY-MM-DD)

    end_date: str
        End date of stock information. (Use format YYYY-MM-DD)

    Returns
    -------
    stock_data: pd.DataFrame
        Stock information, extracted from Yahoo Finance.

    """
    # Convert string dates to DateTime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Extract stock data using DataReader
    stock_data = data.DataReader(ticker, "yahoo", start_date, end_date)

    return stock_data
