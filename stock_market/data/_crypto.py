from typing import Optional

import pandas as pd
from pandas_datareader import data

from stock_market.data.constants import CRYPTO_CURRENCY


def get_crypto(
    ticker: str,
    start_date: str,
    end_date: str = None,
    currency_type: str = "USD",
) -> Optional[pd.DataFrame]:
    """
    Extracts crypto prices over a date period from Yahoo Finance.

    Parameters
    ----------
    ticker: str
        Crypto ticker symbol.

    start_date: str
        Start date of crypto information. (e.g. 2020-01-01, 2020/01/01, January 1 2020)

    end_date: str, default None
        End date of crypto information. If None, use current date.

    currency_type: str, default "USD"
        Crypto currency type. Currently supported ["USD", "CAD"]

    Returns
    -------
    crypto_data: Optional[pd.DataFrame]
        Crypto information, extracted from Yahoo Finance.

    """
    # Check currency type
    if currency_type.upper() in CRYPTO_CURRENCY:
        ticker += "-" + currency_type.upper()
    else:
        raise Warning(f"Currencies {CRYPTO_CURRENCY} are currently supported.")

    # Convert string dates to DateTime
    start_date = pd.to_datetime(start_date)
    if end_date:
        end_date = pd.to_datetime(end_date)
    else:
        end_date = pd.to_datetime("today")

    # Extract crypto data using DataReader
    try:
        crypto_data = data.DataReader(ticker, "yahoo", start_date, end_date)
    except KeyError:
        return None

    return crypto_data
