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
    y_pred : array of shape (n_samples,)
        Returns predicted values of linear predictor.

    """
    None
